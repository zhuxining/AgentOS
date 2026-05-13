# 提取工具手册

## 内置 `web_fetch`

内置 `web_fetch` 用于快速读取 URL 内容，是提取流程的第一步。

```text
web_fetch(url="https://example.com")
```

- 适合快速获取页面标题、摘要和主要正文。
- 如果返回内容足够完整，可直接作为提取结果并标注 `提取工具: web_fetch`。
- 如果内容为空、正文少于 100 字符、只含摘要或明显缺少主体，降级到 `crwl`。

## crwl

首选正文提取工具。

```bash
crwl <url> -o md-fit
crwl <url> -o md
crwl <url> -o md-fit -bc
```

- `md-fit` 输出更适合阅读，优先使用。
- `md` 可在 `md-fit` 过度清洗、遗漏内容时使用。
- `-bc` 用于跳过缓存重新抓取。
- 如果 `md-fit` 失败或内容不足，依次尝试 `md` 和 `md-fit -bc`。
- 如果 `crwl` 命令不可用、页面为空、正文明显缺失或返回内容少于 100 字符，降级到 `browser-use`。

## browser-use

用于 `crwl` 失败后的页面访问和文本提取。

```bash
browser-use open <url>
browser-use state
browser-use eval "document.title"
browser-use eval "document.querySelector('article, main')?.innerText || document.body.innerText"
browser-use get html <index>
browser-use close
```

- 先 `open`，再 `state` 确认页面加载和可交互元素。
- 优先提取 `article` 或 `main`，失败后使用 `document.body.innerText`。
- 默认使用普通浏览器会话；需要登录态时，先询问用户是否使用浏览器配置文件或已连接的浏览器会话。
- 如果会话异常，先 `browser-use close`，再重新打开页面。

## 降级结果判定

- **成功**：获得主体正文，标题和 URL 可确认，正文足以满足用户的提取目的。
- **部分成功**：只获得摘要、片段、受限正文或结构化数据；返回可用内容并说明缺失范围。
- **失败**：所有工具均不可用、需要登录但无法访问、被反爬阻断或页面不存在；返回已尝试工具和失败原因。
