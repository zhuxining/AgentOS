---
name: local-tools-guide
description: 当用户需要执行本地命令、安装或使用 CLI 工具、转换 Office/PDF 文档、搜索网页信息、提取 URL 正文、操作浏览器自动化，或询问"用什么工具""怎么安装""如何提取"时，必须立即使用此技能。涵盖 shell 执行、uv/bun/brew 三条工具链选择、文档转换、搜索与正文提取、浏览器操作。这是处理所有本地工具相关任务的首选入口。
---

# Local Tools Guide

本技能是本地与内置工具的总入口。目标是先判断任务类型，再选择最小、可靠、可复现的工具路径。

## 参考文件导航

| 如果你需要了解... | 阅读 |
|---------------|------|
| 搜索、技术文档查询 (ctx7/ddgs) | [`references/search-tools.md`](references/search-tools.md) |
| URL 正文提取策略 (web_fetch/browser-use) | [`references/fetch-tools.md`](references/fetch-tools.md) |
| 浏览器自动化操作 (browser-use) | [`references/browser-use.md`](references/browser-use.md) |
| 文档转换（PDF/Office/网页转 Markdown） | [`references/document-tools.md`](references/document-tools.md) |
| 本地工具盘点 (uv/bun/brew/其他) | [`references/local-inventory.md`](references/local-inventory.md) |
| Python/Node/Brew 包管理 | [`references/package-tools.md`](references/package-tools.md) |
| Shell 执行最佳实践 | [`references/shell-runtime.md`](references/shell-runtime.md) |

## 兼容性

- **环境假设**: macOS（Homebrew）、已安装 `uv` 和 `bun`、用户 shell 为 `zsh`
- **限制**: 非三工具链（uv/bun/brew）来源的 CLI 只能使用已有入口，禁止通过 `curl \| sh`、`pip --user`、`npm -g`、`cargo install` 等方式新增安装

## 触发边界

| 用户意图 | 处理 |
| --- | --- |
| 执行本地命令、依赖用户 PATH/env、排查 CLI 可用性 | 使用 shell/runtime 流程 |
| 使用或安装 Python CLI、一次性运行 Python 工具 | 使用 `uv` / `uvx` / `uv tool` 流程 |
| 使用或安装 Node CLI、全局 Bun 工具 | 使用 `bun` / `bunx` / `bun add -g` 流程 |
| 使用或安装系统级 CLI、Homebrew 工具 | 使用 Homebrew 流程 |
| 使用非 `uv` / `bun` / `brew` 来源的已有 CLI | 仅允许使用，禁止通过该来源安装 |
| 盘点当前机器可用工具 | 使用本地工具盘点流程 |
| 转换本地文档、Office/PDF/网页内容转 Markdown | 使用文档转换流程 |
| 搜索、查找、调研、查最新信息、找资料 | 使用搜索发现流程 |
| 查询编程库、框架、API、SDK、错误信息 | 优先使用技术文档流程 |
| 只提供 URL，或要求提取、抓取、转 Markdown | 使用正文提取流程 |
| 候选链接核验、确认标题/时间/关键事实 | 使用链接核验流程 |
| 需要点击、登录态、截图、表单、动态页面 | 使用浏览器交互流程 |
| 要摘要、观点分析、五维阅读、深度解读 | 本技能只提供来源或正文，后续由当前任务继续分析 |

## 工具路由

| 场景 | 优先链 | 参考 |
| --- | --- | --- |
| shell 执行 | `exec` -> 必要时 `zsh -lc '<command>'` -> 说明环境限制 | `references/shell-runtime.md` |
| Python CLI | 已安装命令 -> `uvx <tool>` -> `uv tool install <pkg>` | `references/package-tools.md` |
| Node CLI | 已安装命令 -> `bunx <pkg>` -> `bun add -g <pkg>` | `references/package-tools.md` |
| Homebrew CLI | 已安装命令 -> `brew list --formula` -> `brew install <formula>` | `references/package-tools.md` |
| 非三工具链来源 CLI | `which -a` / PATH 目录盘点 -> 只使用已有入口，禁止安装 | `references/package-tools.md` |
| 本地工具盘点 | `which -a` -> `uv tool list` -> `bun pm ls -g` -> `brew list` -> PATH 目录盘点 | `references/local-inventory.md` |
| 文档转换 | `markitdown` -> 文件类型专用工具 -> OOXML/XML/PDF fallback | `references/document-tools.md` |
| 搜索发现 | `web_search` -> `ddgs` -> `browser-use` 搜索页 | `references/search-tools.md` |
| 候选链接核验 | `web_fetch` -> `browser-use` | `references/search-tools.md` |
| 正文提取 | `web_fetch` -> `browser-use open <URL>` -> `state/eval` | `references/fetch-tools.md` |
| 页面交互/高级控制 | `browser-use open <URL>` -> `state` -> `click/input/eval/screenshot` -> `--session` / `python` | `references/browser-use.md` |
| 技术文档 | `ctx7 library` -> `ctx7 docs` -> 定向 `web_search` | `references/search-tools.md` |

## 工作流

### 1. 先分类

- 本地命令先确认工具是否已存在；不要为了试探而安装新包。
- 需要用户 shell 环境、全局工具或 PATH 时，优先使用 `zsh -lc` 或明确记录 shell 假设。
- 一次性 Python/Node 工具优先用 `uvx` / `bunx`，长期复用才考虑全局安装。
- 安装工具只能走 `uv tool install`、`bun add -g` 或 `brew install`；禁止用 `curl | sh`、`npm -g`、`pip --user`、`cargo install` 等方式绕过这三条工具链。
- 非 `uv` / `bun` / `brew` 来源的已有 CLI 可以使用，但只能按现有入口调用，不负责安装、升级或迁移。
- 本地文档先用可复现转换工具，不要手工复制粘贴内容作为提取结果。
- 信息发现先搜索，不用 `web_fetch` 代替搜索。
- 已有 URL 先核验或提取，不重新搜索，除非用户要求找更多来源。
- 需要登录态、点击、截图、动态加载或真实页面状态时，用 `browser-use`。
- 编程库/API 文档先走 `ctx7`，找不到再用定向网页搜索。

### 2. 再执行

- 独立搜索或多个 URL 核验可以并行。
- 每次降级都要有原因：工具不可用、返回空内容、少于 100 字符、明显是导航/错误页、需要交互或登录态。
- 本地工具命令尽量短、可单独复现；需要中间输出时分步执行。
- 使用浏览器打开网页时，先用 `browser-use open <URL>`，再读取 `state`；需要登录态、cookies 或指定 Chrome profile 时，先用 `browser-use profile list` 确认可用 profile，必要时询问用户选择。
- URL 正文提取中，`web_fetch` 失败、内容不足或主体缺失后直接使用 `browser-use`；不要再插入本地 HTML 清洗 CLI 作为中间降级。
- 不把搜索结果伪装成正文；完整正文提取必须走正文提取流程。

## 工具降级决策树

### 正文提取降级链

```
用户提供一个 URL
│
├─→ 步骤 1: web_fetch(url)
│   ├─ 成功（内容完整 ≥100 字符）→ 输出结果 ✓
│   └─ 失败或内容不足 ───────────────┐
│                                    │
└─→ 步骤 2: browser-use eval        │
    ├─ 成功 → 输出结果 ✓
    └─ 失败 → 报告失败原因及已尝试工具 ✗
```

### 搜索降级链

```
用户需要搜索信息
│
├─→ 步骤 1: web_search(query) [Agent 内置]
│   ├─ 成功 → 输出结果 ✓
│   └─ 不可用或结果不足 ──────────────┐
│                                    │
├─→ 步骤 2: ddgs text -q <query>     │
│   ├─ 成功 → 输出结果 ✓
│   └─ 超时/限流/结果不足 ───────────┤
│                                    │
└─→ 步骤 3: browser-use 打开搜索页    │
    ├─ 成功 → 输出结果 ✓
    └─ 失败 → 报告失败原因 ✗
```

### 技术文档查询降级链

```
用户查询编程库/框架/API 文档
│
├─→ 步骤 1: ctx7 library <name> <query>
│   ├─ 成功 → 输出结果 ✓
│   └─ 未找到库或文档 ────────────────┐
│                                    │
├─→ 步骤 2: ctx7 docs <libraryId>    │
│   ├─ 成功 → 输出结果 ✓
│   └─ 失败（最多 3 次尝试）──────────┤
│                                    │
└─→ 步骤 3: web_search 定向官方文档   │
    ├─ 成功 → 提取正文并输出 ✓
    └─ 失败 → 报告失败原因 ✗
```

### 3. 最后输出

- 搜索任务：按主题合并结果，标注来源链接和可靠性限制。
- 正文提取：输出标题、URL、提取工具、状态和干净 Markdown 正文。
- 浏览器任务：输出页面状态、完成的交互、截图路径或提取到的数据。
- 失败时：列出已尝试工具、失败原因和下一步可选路径。
- 使用过工具时，最终回复末尾追加工具使用记录。

## 工具使用记录

如果本轮使用了工具，最终回复末尾按调用顺序追加：

```markdown
**工具使用记录**

| 顺序 | 工具 | 用途 | 结果 |
| --- | --- | --- | --- |
| 1 | `exec` | 盘点 uv tools | 成功，列出 12 个工具 |
| 2 | `exec` | 检查 Bun 全局包 | 失败：sandbox 限制无法读取 ~/.bun |
| 3 | `web_fetch` | 提取文章正文 | 部分成功：返回 1500 字符，可能缺失代码块 |
| 4 | `browser-use` | 重新提取完整内容 | 成功：返回完整正文 |
```

**结果列填写规范**:

- **成功**：简要概括获得的结果（如"列出 12 个工具""返回 3200 字符"）
- **部分成功**：说明获取到什么，以及缺失什么（如"返回 1500 字符，可能缺失代码块"）
- **失败**：说明失败原因（如"sandbox 限制无法读取 ~/.bun""页面返回 403""超时"）

**规则**:

- 只记录真实调用过的工具。
- 不粘贴冗长输出；必要时概括关键结果。
- 失败要写明失败原因。
- 没有调用工具时，不输出该区块。

## 可扩展规则

新增工具时优先更新参考文件中的路由表，记录：

- 适用场景
- 优先级位置
- 示例命令或调用方式
- 成功/失败判定
- 降级目标

只有触发边界、核心优先链或输出职责变化时，才修改本文件。
