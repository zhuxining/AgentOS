# 包管理与全局 CLI

## Python 工具

| 场景 | 命令 | 说明 |
| --- | --- | --- |
| 查看已安装 Python CLI | `uv tool list` | 盘点 `uv tool install` 管理的工具 |
| 一次性运行工具 | `uvx <tool> ...` | 不长期改变用户环境 |
| 安装可复用 CLI | `uv tool install <pkg>` | 会写入用户工具环境，先说明用途 |
| 运行项目脚本 | `uv run <script-or-command>` | 尊重项目依赖和 PEP 723 脚本元数据 |
| 检查 Python 版本 | `uv python list --only-installed` | 排查工具绑定解释器问题 |

优先级：已安装命令 -> `uvx` 一次性运行 -> `uv tool install` 长期复用。不要用 `pip install --user` 安装 CLI。

## Node/Bun 工具

| 场景 | 命令 | 说明 |
| --- | --- | --- |
| 查看全局 Node CLI | `bun pm ls -g` | 盘点 Bun 全局包 |
| 一次性运行工具 | `bunx <pkg> ...` | 不长期改变用户环境 |
| 安装可复用 CLI | `bun add -g <pkg>` | 会写入 Bun 全局目录，先说明用途 |
| 运行项目命令 | `bun run <script>` | 优先使用项目脚本 |
| 查看运行时 | `bun --version` / `node --version` | 排查兼容性 |

优先级：项目脚本或已安装命令 -> `bunx` 一次性运行 -> `bun add -g` 长期复用。

## Homebrew 工具

| 场景 | 命令 | 说明 |
| --- | --- | --- |
| 确认 Homebrew | `which -a brew` / `brew --prefix` | 当前常见前缀为 `/opt/homebrew` |
| 查看公式 CLI | `brew list --formula --versions` | 盘点 Homebrew formula |
| 查看 cask | `brew list --cask --versions` | 主要用于 GUI app，也可能带 CLI |
| 查找包 | `brew search <name>` | 安装前确认名称 |
| 查看包信息 | `brew info <formula>` | 看依赖、版本、安装后提示 |
| 安装 CLI | `brew install <formula>` | 会改变系统级工具环境，先说明用途 |
| 升级 CLI | `brew upgrade <formula>` | 可能影响已有工作流，谨慎执行 |

优先级：已安装命令 -> `brew list --formula` 确认来源 -> `brew info` 核实 -> `brew install`。Homebrew 更适合需要原生依赖、长期可用、系统级 PATH 管理的工具。

## 非三工具链来源 CLI

这类工具不是通过 `uv`、`bun`、`brew` 管理，常见入口包括 `~/.local/bin`、`~/.cargo/bin`、`~/.opencode/bin`、`~/.orbstack/bin`、Codex app 内置目录或工具自己的隐藏目录。

| 场景 | 命令 | 说明 |
| --- | --- | --- |
| 查入口 | `which -a <tool>` | 判断是否已在 PATH |
| 盘点用户 bin | `ls -1 ~/.local/bin ~/.cargo/bin ~/.opencode/bin ~/.orbstack/bin` | 只看常见用户级入口 |
| 使用前验证 | `<tool> --help` / `<tool> --version` | 确认现有命令可用 |
| 来源判断 | `which -a <tool>` + 目录名 | 判断是否属于非三工具链来源 |

规则：

- 已存在的非三工具链 CLI 可以使用。
- 禁止通过 `curl | sh`、`sh install.sh`、`pip --user`、`npm -g`、`cargo install` 等方式新增安装或升级 CLI。
- 需要安装同类能力时，必须优先找 `uv tool install`、`bun add -g` 或 `brew install` 的等价方案。
- 如果工具同时存在于多个来源，优先使用 `which -a <tool>` 判断当前实际命中的入口；必要时改用三工具链管理的入口。

## 安装前检查

- 先确认工具是否已经存在：`which -a <tool>`、`uv tool list`、`bun pm ls -g`、`brew leaves`、常见用户 bin 目录。
- 能用一次性运行解决时，不做全局安装。
- 全局安装、升级、卸载都属于改变用户环境；安装只允许通过 `uv`、`bun`、`brew` 三条工具链执行，并需说明目的、影响和命令。
- 安装后用 `which -a <tool>` 和 `<tool> --help` 做最小验证。

## 常见陷阱

- `uv tool list` 可能因 sandbox 无法读取 `~/.cache/uv` 失败；需要时用获批的只读盘点命令重试。
- `bun pm ls -g` 可能因 sandbox 无法读取 `~/.bun/install/global/package.json` 失败；需要时用获批的只读盘点命令重试。
- Homebrew 安装可能触发下载、编译或链接变更；只读盘点用 `brew list`，不要用 `brew update` 作为默认检查。
- `curl | sh` 可能修改 shell 配置、PATH、用户 bin 或后台服务；本技能中禁止用它安装 CLI。
- 某些 Python CLI 对解释器版本敏感；异常时查看对应 tool venv 的 `pyvenv.cfg`。
