---
name: fetch
description: URL 正文提取技能。用于从网页链接提取干净 Markdown 正文、标题和基础元信息；优先使用内置 web_fetch 快速读取，完整正文提取使用 crwl，失败后降级到 browser-use；不负责摘要、观点分析或五维阅读。
---

# Fetch

URL 内容提取技能，只负责把网页转成可阅读、可复用的干净正文。需要摘要、要点或深度分析时，应改用 `read`。

## 触发边界

| 用户意图 | 处理 |
|------|------|
| 只提供 URL | 使用本技能，提取正文 |
| 明确说 fetch、提取、抓取、抽取正文、转 Markdown | 使用本技能 |
| 需要标题、原始 URL、正文和提取工具记录 | 使用本技能 |
| 要读一下、总结、分析链接内容 | 使用 `read` |
| 要搜索相关资料 | 使用 `search` |

## 提取流程

按优先级尝试。前一个工具报错、不可用、返回空内容、正文少于 100 字符或明显只包含导航/错误页时，自动降级。

```bash
web_fetch(url="<url>")
crwl <url> -o md-fit
crwl <url> -o md
crwl <url> -o md-fit -bc
browser-use open <url>
browser-use state
browser-use eval "document.title"
browser-use eval "document.querySelector('article, main')?.innerText || document.body.innerText"
browser-use close
```

工具调用细节见 `references/tool-catalog.md`。

## 输出要求

- 输出页面标题、原始 URL、提取工具和干净 Markdown 正文。
- 尽量保留原文标题层级、列表、表格、代码块、关键数据和引用链接。
- 移除导航、广告、推荐阅读、页脚、重复菜单和 cookie 横幅。
- 不做摘要、评价、五维分析或额外解释。
- 明确标注提取状态：`成功`、`部分成功` 或 `失败`。
- 如果需要登录、反爬或内容不可访问，说明失败原因和已尝试的工具。

## 输出格式

```markdown
## [页面标题](url)

**提取工具**: crwl
**提取状态**: 成功

### 正文

[干净 Markdown 全文]
```

## 委托协议

其他技能可委托 `fetch` 提取 URL 正文。被委托时：

- 返回标题、URL、提取工具、提取状态、干净正文。
- 不主动追问用户。
- 部分成功时返回可用正文，并说明缺失范围或可信度限制。
- 完全失败时返回失败原因和已尝试路径，供调用方决定下一步。
