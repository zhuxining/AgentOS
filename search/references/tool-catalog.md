# 搜索工具手册

## 内置 `web_search` Tool

Agent 自带 `web_search` 用于通用网页搜索和结果摘要，是搜索任务的首选工具。

```text
web_search(query="搜索关键词")
```

- 适合快速查找网页、新闻、产品资料、公开文档和背景信息。
- 英文关键词通常覆盖更广；中文主题可以保留中文关键词，并按需要增加英文同义词。
- 对可靠性要求高时，优先使用 `site:` 定向到官方站点、论文库、政府或机构页面。
- 如果 `web_search` 不可用或结果不足，再使用 DDGS 脚本；不要用 `web_fetch` 替代搜索发现。

## 内置 `web_fetch` Tool

Agent 自带 `web_fetch` 用于读取或核验已有候选链接，不用于搜索发现。

```text
web_fetch(url="https://example.com")
```

- 适合确认候选页面的标题、发布日期、作者、关键事实和摘要。
- 深度研究时，先用 `web_search` 或 DDGS 找候选来源，再用 `web_fetch` 读取高价值链接。
- 如果 `web_fetch` 失败、内容不足或需要页面交互，降级到 `browser-use`。
- 如果用户需要完整 Markdown 正文，委托 `fetch`。

## DDGS 脚本

用于可复现的命令行网页搜索，或需要 JSON 结果供其他流程消费时。

```bash
uv run search/scripts/ddgs_search.py "搜索关键词"
uv run search/scripts/ddgs_search.py "搜索关键词" --max-results 5 --output json
uv run search/scripts/ddgs_search.py "搜索关键词" --region cn-zh --safe-search moderate
uv run search/scripts/ddgs_search.py "搜索关键词" --time w
uv run search/scripts/ddgs_search.py "搜索关键词" --timeout 10 --retries 2
uv run search/scripts/ddgs_search.py "搜索关键词" --backend duckduckgo
```

- 脚本使用 PEP 723 元数据声明 `ddgs` 依赖，直接通过 `uv run` 执行。
- 默认输出 Markdown；`--output json` 输出 `title`、`url`、`snippet` 字段。
- `--time` 支持 `d`、`w`、`m`、`y`，分别表示一天、一周、一月、一年。
- 默认使用 `auto` 后端以提高可用性；需要贴近 DuckDuckGo HTML 端点时传 `--backend duckduckgo`。
- 默认每次搜索 15 秒硬超时，失败后重试 1 次；`--timeout` 和 `--retries` 可调整。
- 只在 `web_search` 不可用、需要命令行可复现结果或需要 JSON 输出时使用。
- 搜索失败会输出错误并返回非零退出码。

## Context7

用于编程库、框架、API 和 SDK 的官方文档查询。

```bash
ctx7 library <name> <query>
ctx7 docs <libraryId> <query>
```

- 两步调用有顺序依赖，必须先解析库 ID。
- 每个问题最多尝试 3 次；仍未命中时，使用 `web_search` 定向官方文档。
- 只在技术文档场景使用，不用于普通新闻或网页搜索。

## browser-use

用于需要真实页面交互的公开网页；只在 `web_search`、DDGS 或 `web_fetch` 无法满足时使用。

```bash
browser-use open "https://www.google.com/search?q=搜索词"
browser-use state
browser-use click <index>
browser-use get text <index>
browser-use eval "document.body.innerText"
browser-use close
```

- 先运行 `state` 获取可交互元素索引，再点击或提取文本。
- 当搜索页动态加载、需要翻页、需要进入多个结果页验证时使用。
- 如果会话异常，先 `browser-use close`，再重新打开页面。
