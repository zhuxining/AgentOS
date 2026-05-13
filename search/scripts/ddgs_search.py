#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "ddgs>=9.14.2",
# ]
# ///
"""Search the web with ddgs and print Markdown or JSON results."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException, TimeoutException

SafeSearch = Literal["off", "moderate", "strict"]


@dataclass(frozen=True, slots=True)
class SearchResult:
    title: str
    url: str
    snippet: str


class SearchExecutionError(RuntimeError):
    """Raised when the supervised search worker fails."""


class SearchTimedOutError(RuntimeError):
    """Raised when the supervised search worker exceeds the timeout."""


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as err:
        raise argparse.ArgumentTypeError("must be an integer") from err
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def non_negative_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as err:
        raise argparse.ArgumentTypeError("must be an integer") from err
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be greater than or equal to 0")
    return parsed


def positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as err:
        raise argparse.ArgumentTypeError("must be a number") from err
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def non_negative_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as err:
        raise argparse.ArgumentTypeError("must be a number") from err
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be greater than or equal to 0")
    return parsed


def text_value(item: Mapping[str, object], keys: Sequence[str]) -> str:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def normalize_results(
    raw_results: Iterable[Mapping[str, object]],
) -> list[SearchResult]:
    results: list[SearchResult] = []
    seen_urls: set[str] = set()

    for raw in raw_results:
        url = text_value(raw, ("href", "url"))
        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        title = text_value(raw, ("title",)) or url
        snippet = text_value(raw, ("body", "snippet", "description"))
        results.append(SearchResult(title=title, url=url, snippet=snippet))

    return results


def run_search(
    *,
    query: str,
    max_results: int,
    region: str,
    safe_search: SafeSearch,
    time_limit: str | None,
    request_timeout: float,
    backend: str,
) -> list[SearchResult]:
    kwargs: dict[str, object] = {
        "max_results": max_results,
        "region": region,
        "safesearch": safe_search,
        "backend": backend,
    }
    if time_limit is not None:
        kwargs["timelimit"] = time_limit

    raw_results = DDGS(timeout=request_timeout).text(query, **kwargs)
    return normalize_results(raw_results)


def parse_worker_results(payload: str) -> list[SearchResult]:
    try:
        raw_results = json.loads(payload)
    except json.JSONDecodeError as err:
        raise SearchExecutionError("search worker returned invalid JSON") from err

    if not isinstance(raw_results, list):
        raise SearchExecutionError("search worker returned a non-list payload")

    results: list[SearchResult] = []
    for item in raw_results:
        if not isinstance(item, dict):
            raise SearchExecutionError("search worker returned an invalid result item")
        title = text_value(item, ("title",))
        url = text_value(item, ("url",))
        snippet = text_value(item, ("snippet",))
        if not title or not url:
            raise SearchExecutionError(
                "search worker returned a result without title or URL"
            )
        results.append(SearchResult(title=title, url=url, snippet=snippet))
    return results


def worker_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        args.query,
        "--max-results",
        str(args.max_results),
        "--region",
        args.region,
        "--safe-search",
        args.safe_search,
        "--timeout",
        str(args.timeout),
        "--backend",
        args.backend,
    ]
    if args.time is not None:
        command.extend(("--time", args.time))
    return command


async def run_worker_once(args: argparse.Namespace) -> list[SearchResult]:
    process = await asyncio.create_subprocess_exec(
        *worker_command(args),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=args.timeout,
        )
    except TimeoutError as err:
        process.kill()
        await process.communicate()
        raise SearchTimedOutError(
            f"search timed out after {args.timeout:g} seconds"
        ) from err

    if process.returncode != 0:
        error = stderr.decode().strip() or stdout.decode().strip()
        raise SearchExecutionError(error or "search worker failed")

    return parse_worker_results(stdout.decode())


async def run_search_async(args: argparse.Namespace) -> list[SearchResult]:
    attempts = args.retries + 1
    last_error: SearchExecutionError | SearchTimedOutError | None = None

    for attempt in range(1, attempts + 1):
        try:
            return await run_worker_once(args)
        except (SearchExecutionError, SearchTimedOutError) as err:
            last_error = err
            if attempt == attempts:
                break
            if args.retry_delay > 0:
                await asyncio.sleep(args.retry_delay)

    if last_error is None:
        raise SearchExecutionError("search failed before starting")
    raise last_error


def markdown_output(query: str, results: Sequence[SearchResult]) -> str:
    if not results:
        return f"## Search results: {query}\n\nNo results found."

    lines = [f"## Search results: {query}", ""]
    for index, result in enumerate(results, start=1):
        lines.append(f"{index}. [{result.title}]({result.url})")
        if result.snippet:
            lines.append(f"   - {result.snippet}")
    return "\n".join(lines)


def json_output(results: Sequence[SearchResult]) -> str:
    return json.dumps(
        [asdict(result) for result in results], ensure_ascii=False, indent=2
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search the web with ddgs and print normalized results.",
    )
    parser.add_argument("query", help="Search query.")
    parser.add_argument(
        "-n",
        "--max-results",
        type=positive_int,
        default=10,
        help="Maximum number of results to return. Default: 10.",
    )
    parser.add_argument(
        "--region",
        default="cn-zh",
        help='Search region, such as "us-en","cn-zh". Default: cn-zh.',
    )
    parser.add_argument(
        "--safe-search",
        choices=("off", "moderate", "strict"),
        default="off",
        help="Safe search level. Default: off.",
    )
    parser.add_argument(
        "--time",
        choices=("d", "w", "m", "y"),
        help="Limit results to day, week, month, or year.",
    )
    parser.add_argument(
        "--output",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Default: markdown.",
    )
    parser.add_argument(
        "--timeout",
        type=positive_float,
        default=15.0,
        help="Hard timeout per search attempt in seconds. Default: 15.",
    )
    parser.add_argument(
        "--backend",
        default="auto",
        help='DDGS backend, such as "auto", "duckduckgo", "brave", or "bing". Default: auto.',
    )
    parser.add_argument(
        "--retries",
        type=non_negative_int,
        default=1,
        help="Number of retries after the initial attempt. Default: 1.",
    )
    parser.add_argument(
        "--retry-delay",
        type=non_negative_float,
        default=0.5,
        help="Delay between retries in seconds. Default: 0.5.",
    )
    parser.add_argument(
        "--worker",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    return parser


def worker_main(args: argparse.Namespace) -> int:
    try:
        results = run_search(
            query=args.query,
            max_results=args.max_results,
            region=args.region,
            safe_search=args.safe_search,
            time_limit=args.time,
            request_timeout=args.timeout,
            backend=args.backend,
        )
    except (DDGSException, RatelimitException, TimeoutException, OSError) as err:
        print(f"Search failed: {err}", file=sys.stderr)
        return 1

    print(json_output(results))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.worker:
        return worker_main(args)

    try:
        results = asyncio.run(run_search_async(args))
    except (SearchExecutionError, SearchTimedOutError) as err:
        print(f"Search failed: {err}", file=sys.stderr)
        return 1

    if args.output == "json":
        print(json_output(results))
    else:
        print(markdown_output(args.query, results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
