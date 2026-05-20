# 本地工具盘点

本文件以 `uv`、`bun`、`brew` 三条工具链为安装与执行基准，并额外列出非三工具链来源的已有 CLI。非三工具链 CLI 只能使用现有入口，禁止通过其来源新增安装或升级。执行任务前按需动态刷新，不把版本号当长期事实。

## 动态盘点命令

```bash
uv tool list
bun pm ls -g
brew leaves
brew list --cask --versions
ls -1 ~/.local/bin ~/.cargo/bin ~/.opencode/bin ~/.orbstack/bin
zsh -lc 'which -a <tool>'
```

如果 `uv tool list`、`bun pm ls -g` 或 `brew leaves` 因权限或 sandbox 失败，记录失败原因；只有任务确实依赖完整清单时，按权限流程请求只读盘点。

## 使用优先级

| 任务 | 优先工具链 | 执行 | 安装 |
| --- | --- | --- | --- |
| Python CLI / Python 生态工具 | `uv` | 已安装命令或 `uvx <pkg>` | `uv tool install <pkg>` |
| Node/TS CLI / JS 生态工具 | `bun` | 已安装命令或 `bunx <pkg>` | `bun add -g <pkg>` |
| 系统级 CLI / 原生依赖 / 通用 Unix 工具 | `brew` | 已安装命令 | `brew install <formula>` |
| 非三工具链来源的已有 CLI | 只使用现有入口 | 已安装命令 | 禁止安装；找 `uv` / `bun` / `brew` 等价方案 |

安装、升级、卸载都会改变用户环境；新增安装和升级只允许通过 `uv`、`bun`、`brew` 三条工具链执行，执行前说明目的、影响和命令，安装后用 `which -a <tool>` 与 `<tool> --help` 做最小验证。

## uv tool 可用工具

| 包/工具 | 可调用命令 | Agent 用途 |
| --- | --- | --- |
| `agent-reach` | `agent-reach` | 全网可达性视野、平台 API 输出整理和健康检查；优先交给 Agent Reach 专用 skill |
| `browser-use` | `browser-use` | 真实浏览器交互；需要登录态时先确认可用 profile |
| `ddgs` | `ddgs` | 命令行网页/新闻搜索 fallback |
| `httpx` | `httpx` | HTTP 请求调试 |
| `litert-lm` | `litert-lm` | 本地 LLM 实验，按需使用 |
| `markitdown` | `markitdown` | 本地 Office/PDF/HTML 转 Markdown |
| `nanobot-ai` | `nanobot` | agent/LLM 工作流实验，按需使用 |
| `ruff` | `ruff` | Python lint/format |
| `stk-cli` | `stk` | 项目或用户明确要求时使用 |
| `ty` | `ty` | Python 类型检查 |

## bun global 可用工具

| 包/工具 | 可调用命令 | Agent 用途 |
| --- | --- | --- |
| `ctx7` | `ctx7` | 技术文档查询 |
| `defuddle-cli` | `defuddle` | HTML 转化为 Markdown；不作为 URL 正文提取 fallback |
| `playwright` | `playwright` | 浏览器测试和自动化 |
| `@playwright/mcp` | `playwright-mcp` | Playwright MCP，按需使用 |
| `agent-browser` | `agent-browser` | browser/agent 辅助任务，按需使用 |
| `@jackwener/opencli` | `opencli` | 站点/应用 adapter、把网站当 CLI 调用；优先交给 OpenCLI 专用 skill |
| `@mariozechner/pi-coding-agent` | `pi` | 编码 agent，按需使用 |
| `opencode-ai` | `opencode` | 编码 agent，按需使用 |
| `@openai/codex` | `codex` | 只有用户明确要求调用 Codex CLI 时使用 |
| `@zed-industries/claude-code-acp` | `claude-code-acp` | Zed/Claude Code ACP，按需使用 |
| `clawhub` | `clawhub` / `clawdhub` | ClawHub 相关任务，按需使用 |
| `typescript` | `tsc` / `tsserver` | TypeScript 编译或服务，项目明确需要时 |
| `typescript-language-server` | `typescript-language-server` | TypeScript LSP，项目明确需要时 |
| `@googleworkspace/cli` | 未确认稳定命令 | Google Workspace 相关任务前先 `bun pm ls -g` 和 `ls ~/.bun/bin` 核实 |
| `pptxgenjs` | 无同名 CLI | 作为 Node 库处理，不列为可直接调用 CLI |

## brew 可用工具

`brew leaves` 只列顶层安装项，比 `brew list --formula` 更适合 Agent 盘点。

| formula/cask | 常用命令 | Agent 用途 |
| --- | --- | --- |
| `uv` | `uv` / `uvx` | Python package/tool manager |
| `oven-sh/bun/bun` | `bun` / `bunx` | JS runtime/package manager |
| `ripgrep` | `rg` | 文本搜索；优先使用 |
| `fd` | `fd` | 文件查找；需要可读性时可替代 `find` |
| `gh` | `gh` | GitHub 仓库、PR、issue 操作 |
| `biome` | `biome` | JS/TS lint/format |
| `markdownlint-cli2` | `markdownlint-cli2` | Markdown lint |
| `pandoc` | `pandoc` | 文档格式转换 |
| `ffmpeg` | `ffmpeg` | 音视频处理 |
| `tesseract` | `tesseract` | OCR |
| `yt-dlp` | `yt-dlp` | 视频/媒体下载 |
| `pnpm` | `pnpm` | 项目明确依赖 pnpm 时使用 |
| `bat` | `bat` | 人类阅读友好；Agent 默认不用 |
| `eza` | `eza` | 人类阅读友好；Agent 默认不用 |
| `fzf` | `fzf` | 交互式工具；Agent 默认不用 |
| `tmux` | `tmux` | 交互式会话管理 |
| `gws` | `gws` | Google Workspace 任务明确需要时 |
| `rtk` | `rtk` | 本机 RTK 工作流明确需要时 |
| `llmfit` / `hysteria` / `mole` / `remindctl` / `sonoscli` / `ta-lib` | 对应命令 | 特定任务明确需要时再用 |
| `starship` / `zoxide` / `zsh-*` | 对应命令 | shell 体验工具，不作为 Agent 调用工具 |
| `gcloud-cli` cask | `gcloud` | Google Cloud 任务明确需要时 |

## 非三工具链来源的已有工具

这些工具当前可在 PATH 中发现，但不属于 `uv tool list`、`bun pm ls -g` 或 `brew leaves` 管理。只能使用已有入口；如需新增安装、升级或替换，必须改走 `uv` / `bun` / `brew`。

| 来源 | 可调用命令 | 使用限制 |
| --- | --- | --- |
| `~/.local/bin` | `claude` | 只有用户明确要求 Claude CLI 时使用；禁止通过脚本安装/升级 |
| `~/.orbstack/bin` | `docker` / `docker-compose` / `docker-credential-osxkeychain` | OrbStack 提供的现有入口；容器任务需要时使用 |
| `~/.orbstack/bin` | `kubectl` / `orb` / `orbctl` | Kubernetes/OrbStack 任务需要时使用 |
| `~/.cargo/bin` | `cargo` / `rustc` / `rustup` / `rustfmt` / `rust-analyzer` 等 | Rust 项目明确需要时使用；禁止用 `cargo install` 新装 CLI |

## 使用规则

- 安装和升级限定在 `uv`、`bun`、`brew` 三条工具链内。
- 非三工具链来源的工具只能使用已有入口，禁止用该来源新增安装或升级。
- 执行前用 `which -a <tool>` 确认实际命中的入口。
- 优先记录可调用命令，不把包名误写成命令。
- 交互式 TUI、shell 美化、重复别名、维护命令只在明确任务需要时使用。
- 对输出质量敏感的工具，先跑 `--help` 或低风险 smoke test。
