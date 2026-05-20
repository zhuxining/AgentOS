# 搜索与核验工具

## 路由表

| 工具 | 适用场景 | 成功判定 | 失败或降级 |
| --- | --- | --- | --- |
| `web_search` | 通用网页搜索、新闻、公开资料、来源发现 | 返回相关候选来源和摘要 | 不可用、结果不足或需要可复现输出时用 DDGS |
| `web_fetch` | 已有候选链接的标题、时间、作者、关键事实核验 | 能读取页面核心信息 | 内容不足、受限或需要交互时用 `browser-use` |
| `ddgs` | 命令行可复现搜索、内置搜索不可用、需要本地 DuckDuckGo/多后端搜索 | 返回标题、URL 和摘要 | 超时、限流、结果不足时换查询或用浏览器 |
| `ctx7` | 编程库、框架、API、SDK 官方文档查询 | 找到库 ID 并返回相关文档片段 | 每个问题最多 3 次，失败后定向搜索官方文档 |
| `browser-use` | 搜索页动态加载、翻页、点击结果、真实页面核验 | 能打开页面并读取状态或内容 | 会话异常时先 close 再重试 |

## 通用搜索

优先使用 Agent 自带 `web_search`。对可靠性要求高时，用 `site:` 限定到官方站点、论文库、政府或机构页面。

```text
web_search(query="搜索关键词")
```

候选链接需要核验时使用 `web_fetch`，不要把它当作搜索发现工具。

```text
web_fetch(url="https://example.com")
```

## DDGS fallback

需要可复现命令行搜索或内置搜索不可用时，直接使用 `uv tool` 中已安装的 `ddgs` CLI。

```bash
ddgs text -q "搜索关键词"
ddgs text -q "搜索关键词" -m 5
ddgs text -q "搜索关键词" -r cn-zh
ddgs text -q "搜索关键词" -s moderate
ddgs text -q "搜索关键词" -t w
ddgs text -q "搜索关键词" -b duckduckgo
ddgs text -q "搜索关键词" -o json
```

- 使用前可用 `which -a ddgs` 或 `uv tool list` 确认入口。
- `-m` 控制结果数量，`-r` 控制区域，`-s` 控制安全搜索，`-t` 控制时间范围。
- `-b` 控制搜索后端，可选 `auto`、`all`、`bing`、`brave`、`duckduckgo`、`google`、`grokipedia`、`mojeek`、`startpage`、`yandex`、`yahoo`、`wikipedia`；默认优先用 `auto`，需要贴近某个来源时再指定。
- `-o json` 会保存 JSON 文件；如果只需要快速查看结果，不要加 `-o`。
- 如果命令行参数随版本变化，先运行 `ddgs --help` 或 `ddgs text --help` 确认。
- 输出质量重要时，和真实浏览器里的搜索结果抽样对照。

## DDGS news

查新闻、近期事件或按时间范围检索新闻来源时，使用 `ddgs news`。

```bash
ddgs news -q "新闻关键词"
ddgs news -q "新闻关键词" -m 5
ddgs news -q "新闻关键词" -r cn-zh
ddgs news -q "新闻关键词" -s moderate
ddgs news -q "新闻关键词" -t d
ddgs news -q "新闻关键词" -b duckduckgo
ddgs news -q "新闻关键词" -o json
```

- `-t` 支持 `d`、`w`、`m`、`y`，新闻检索优先按用户时间要求设置。
- `-b` 可选 `auto`、`all`、`bing`、`duckduckgo`、`yahoo`。
- `-o json` 同样会保存 JSON 文件；如果只需要快速查看结果，不要加 `-o`。
- 新闻类结果更容易时效性漂移，关键事实要继续用 `web_fetch` 或浏览器打开原文核验。

## 技术文档

涉及编程库、框架、API、SDK、配置项或错误信息时，先用 `ctx7`。

```bash
ctx7 library <name> <query>
ctx7 docs <libraryId> <query>
```

先解析库 ID，再查文档。仍未命中时，用 `web_search` 定向官方文档。

## 浏览器搜索页

只有搜索结果动态加载、需要翻页、要点击多个结果页验证，或前面工具无法满足时，才用浏览器。

```bash
browser-use open "https://www.google.com/search?q=搜索词"
browser-use state
browser-use click <index>
browser-use get text <index>
browser-use close
```
