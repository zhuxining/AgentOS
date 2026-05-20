# 文档转换与本地文件提取

## 路由表

| 输入 | 首选 | fallback |
| --- | --- | --- |
| 本地 Office/PDF/HTML 等文档转 Markdown | `markitdown` | 文件类型专用库、OOXML/XML、PDF 文本提取 |
| 网页 URL 转正文 | `web_fetch` | `browser-use eval` |
| PPTX 文本检查或轻量编辑 | OOXML/XML 直接读取 | `pptxgenjs` 仅用于生成类任务 |
| PDF 文本抽取失败 | 渲染/视觉检查 | 手工核对关键页 |

## markitdown

`markitdown` 适合把本地文档转换成 Markdown 供后续阅读、检查或总结。

```bash
zsh -lc 'which -a markitdown'
markitdown input.docx -o output.md
markitdown input.pdf -o output.md
markitdown input.pptx -o output.md
```

使用规则：

- 先确认输入文件路径和目标输出路径。
- 转换后抽样检查标题、表格、页码、脚注和中文标点是否明显丢失。
- 不把转换结果视为排版真相；排版问题仍需用原文件或渲染图核验。

## Office / OOXML fallback

当库缺失或转换不可靠时，Office 文件可以直接读取压缩包内 XML：

- `.docx`：`word/document.xml`
- `.pptx`：`ppt/slides/slide*.xml`
- `.xlsx`：`xl/worksheets/*.xml` 和 `xl/sharedStrings.xml`

适合文本提取、错别字检查和轻量替换；涉及版式、图片、动画和复杂表格时，要回到原文件或渲染结果验证。

## 网页与 URL

URL 内容不走 `markitdown` 作为首选，继续使用网页提取链：

```bash
web_fetch(url="<url>")
browser-use open <url>
browser-use state
browser-use eval "document.querySelector('article, main')?.innerText || document.body.innerText"
```
