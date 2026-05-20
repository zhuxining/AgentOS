# 正文提取工具

## 路由表

| 工具 | 适用场景 | 成功判定 | 失败或降级 |
| --- | --- | --- | --- |
| `web_fetch` | 快速读取 URL 标题、摘要和主要正文 | 内容足够完整，可满足提取目的 | 空内容、少于 100 字符、只含摘要或缺主体时直接用 `browser-use` |
| `browser-use eval` | 动态页面、微信文章、需要登录态、反爬或 `web_fetch` 失败 | 能读取 `article`、`main` 或 `body` 文本 | 返回部分内容或说明失败原因 |

## 提取流程

按优先级尝试。`web_fetch` 失败、返回空内容、少于 100 字符或明显只包含导航/错误页时，直接降级到 `browser-use`。

```bash
web_fetch(url="<url>")
browser-use open <url>
browser-use state
browser-use eval "document.title"
browser-use eval "document.querySelector('article, main')?.innerText || document.body.innerText"
browser-use close
```

## 输出要求

- 输出页面标题、原始 URL、提取工具和干净 Markdown 正文。
- 尽量保留标题层级、列表、表格、代码块、关键数据和引用链接。
- 移除导航、广告、推荐阅读、页脚、重复菜单和 cookie 横幅。
- 不做摘要、评价、五维分析或额外解释。
- 标注提取状态：`成功`、`部分成功` 或 `失败`。

## 输出格式

```markdown
## [页面标题](url)

**提取工具**: browser-use
**提取状态**: 成功

### 正文

[干净 Markdown 全文]
```
