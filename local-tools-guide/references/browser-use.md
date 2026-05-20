# browser-use 常用操作

`browser-use` 用于真实页面交互、动态内容、截图、表单和登录态页面。

## 基本流程

```bash
browser-use doctor
browser-use open <url>
browser-use state
browser-use click <index>
browser-use input <index> "text"
browser-use eval "document.body.innerText"
browser-use screenshot path.png
browser-use close
```

- 先运行 `state`，拿到可交互元素索引后再点击或输入。
- 默认先直接打开页面；需要登录态、cookies 或内部权限时，先列出可用 profile，再按任务需要选择。
- 命令失败或会话异常时，先 `browser-use close`，再重新打开页面。
- 只在不需要中间输出时链式执行；需要解析 `state` 时分步执行。

## 浏览器模式

```bash
browser-use open <url>
browser-use --headed open <url>
browser-use connect
browser-use --profile <profile-name> open <url>
```

- 普通 headless Chromium 只在明确不需要登录态、cookies 或用户环境时使用。
- `--headed` 用于调试可见窗口。
- `connect` 连接用户当前 Chrome，保留 cookies 和登录态。
- `--profile` 使用指定 Chrome profile 启动独立 Chromium。

如果默认打开无法满足任务，或任务明确需要当前可见 Chrome，再询问用户选择：

- 使用真实 Chrome：用户先开启 remote debugging，再重试 `browser-use connect`。
- 使用托管 Chromium + Chrome profile：先 `browser-use profile list`，再让用户选择 profile。

## 常用命令

```bash
browser-use open <url>
browser-use back
browser-use scroll down
browser-use scroll up
browser-use tab list
browser-use tab new [url]
browser-use tab switch <index>
browser-use tab close <index>
browser-use state
browser-use screenshot [path.png]
browser-use click <index>
browser-use click <x> <y>
browser-use type "text"
browser-use input <index> "text"
browser-use keys "Enter"
browser-use select <index> "option"
browser-use upload <index> <path>
browser-use hover <index>
browser-use eval "js code"
browser-use get title
browser-use get html [--selector "h1"]
browser-use get text <index>
browser-use get value <index>
browser-use wait selector "css"
browser-use wait text "text"
browser-use cookies get [--url <url>]
browser-use cookies export <file>
browser-use cookies import <file>
browser-use sessions
browser-use close --all
```

## 数据提取

```bash
browser-use eval "document.title"
browser-use eval "document.querySelector('article, main')?.innerText || document.body.innerText"
browser-use get html --selector "main"
browser-use get text <index>
```

优先提取 `article` 或 `main`，失败后再使用 `document.body.innerText`。

## 多 session

需要多个浏览器同时运行时使用 `--session NAME`。

```bash
browser-use --session work open <url>
browser-use --session work state
browser-use --session debug --headed open <url>
browser-use sessions
browser-use --session work close
browser-use close --all
```

每个 session 有独立 daemon、socket、PID、浏览器实例和标签状态。忘记传 `--session` 会落到默认 session，这是最常见错误。

可用环境变量固定 session：

```bash
export BROWSER_USE_SESSION=work
browser-use open <url>
```

## 原始 CDP 与 Python

CLI 覆盖不了的浏览器级控制，可以用 `browser-use python`。适合激活用户可见标签、拦截网络、模拟设备或直接操作 Chrome target。

```bash
browser-use python "cdp = browser._run(browser._session.get_or_create_cdp_session())"
browser-use python "result = browser._run(cdp.cdp_client.send.Runtime.evaluate(params={'expression': 'document.title', 'returnByValue': True}, session_id=cdp.session_id))"
browser-use python "print(result['result']['value'])"
```

### 激活用户可见标签

```bash
browser-use python "targets = browser._session.session_manager.get_all_page_targets()"
browser-use python "print([(i, t.url) for i, t in enumerate(targets)])"
browser-use python "cdp = browser._run(browser._session.get_or_create_cdp_session(target_id=None, focus=False))"
browser-use python "browser._run(cdp.cdp_client.send.Target.activateTarget(params={'targetId': targets[1].target_id}))"
```

### 模拟移动设备

```bash
browser-use python "cdp = browser._run(browser._session.get_or_create_cdp_session())"
browser-use python "browser._run(cdp.cdp_client.send.Emulation.setDeviceMetricsOverride(params={'width': 375, 'height': 812, 'deviceScaleFactor': 3, 'mobile': True}, session_id=cdp.session_id))"
```

`browser-use python` 每次执行一条语句，变量会跨调用保留。复杂逻辑优先拆成多次命令，避免难以调试。
