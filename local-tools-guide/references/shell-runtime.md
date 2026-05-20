# Shell 与本地运行环境

## 路由表

| 场景 | 首选 | 何时调整 |
| --- | --- | --- |
| 普通仓库命令 | 直接执行单条命令 | 命令找不到或 PATH/env 不完整时用 `zsh -lc` |
| 依赖用户 PATH 的全局工具 | `zsh -lc '<command>'` | 仍失败时先 `which -a <tool>` 定位 |
| 需要登录 shell 初始化 | `zsh -lc '<command>'` | 命令可能有副作用时先说明目的 |
| 需要多个中间输出 | 分步执行 | 不把长链命令塞到一条里 |

## 使用原则

- 默认保持命令短、单一、可复现。
- 需要读取用户 shell 配置、`~/.local/bin`、`~/.bun/bin`、`uv tool` 或 Homebrew 路径时，优先用 `zsh -lc`。
- 不需要 shell 初始化时，直接执行具体命令，减少 quoting 和环境不确定性。
- 不为了省事使用长链命令；需要解析中间输出时分开执行。
- 涉及写入用户全局目录、安装工具、删除文件或改变配置时，先遵守权限审批流程。

## 常用诊断

```bash
zsh -lc 'print -r -- $PATH'
zsh -lc 'which -a uv uvx bun node npm python3'
zsh -lc 'which -a brew markitdown defuddle browser-use ctx7'
zsh -lc 'ls -1 ~/.local/bin ~/.cargo/bin ~/.opencode/bin ~/.orbstack/bin'
zsh -lc '<tool> --help'
```

如果 sandbox 内无法读取用户缓存或全局包目录，记录失败原因；确实需要该信息时，再按权限流程重新运行同一类只读盘点命令。
