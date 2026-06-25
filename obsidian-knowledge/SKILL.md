---
name: obsidian-knowledge
description: Obsidian CLI 操作 MyObsidian vault 的强制协议。每当用户提到 Obsidian、vault、知识库、笔记、Daily、记录、保存到、搜索我的、帮我找一下、记一下、存一下、整理笔记、查看笔记、在我的知识库里，都必须用此 skill。不要用文件工具直接操作 vault——CLI 自动处理 wikilinks、frontmatter、Daily 路径。
---

# Obsidian Knowledge

与用户共享 `MyObsidian` vault。**所有 vault 操作必须通过 `obsidian` CLI**，不要用 Read/Write/Edit 等文件工具直接读写 vault 里的 `.md` 文件。

## 首要规则

**每个会话首次触及 vault 之前**，先读 AGENTS.md 获取当前 vault 的目录、标签、frontmatter 和隐私规范：

```bash
obsidian vault=MyObsidian read file="AGENTS"
```

AGENTS.md 是 vault 规范的唯一来源。本 skill 不重复定义任何目录、标签或 frontmatter 字段。

## 强制使用 CLI

以下操作**必须**用 Obsidian CLI，**禁止**用文件工具替代：

| 操作 | 原因 |
|------|------|
| 读取笔记 | CLI 自动解析 wikilinks 和 file name |
| 搜索 vault | 文件工具无法做全文搜索 |
| 创建/覆写笔记 | CLI 自动处理 frontmatter、触发 Obsidian 索引 |
| 追加内容 | CLI 保证不破坏已有结构 |
| 更新 frontmatter | `property:set` 安全修改单个字段 |
| 移动/重命名 | `move` 自动修复所有 wikilinks |
| Daily 读写 | CLI 自动定位到正确的 Daily 文件路径 |

**错误示例**（不要这样做）：
```bash
# ❌ 用 Read 直接读 vault 文件
cat /Users/zhuxining/MyObsidian/01_Daily/2026/06/2026-06-25.md
# ❌ 用 Write 直接写 vault 文件
```

**正确做法**：
```bash
# ✓ 用 CLI 读
obsidian vault=MyObsidian read file="AGENTS"
# ✓ 用 CLI 追加 Daily
obsidian vault=MyObsidian daily:append content="- 记录了某件事"
```

## 常用命令

`vault=MyObsidian` 必须作为第一个参数。

```bash
# === 查找 ===
obsidian vault=MyObsidian search query="关键词" limit=20
obsidian vault=MyObsidian search:context query="关键词" limit=20

# === 读取 ===
obsidian vault=MyObsidian read file="笔记名"
obsidian vault=MyObsidian read path="目录/笔记.md"

# === 创建 ===
obsidian vault=MyObsidian create path="目录/笔记.md" content="<内容>" silent

# === 覆写 ===
obsidian vault=MyObsidian create path="目录/笔记.md" content="<新内容>" overwrite silent

# === 追加 ===
obsidian vault=MyObsidian append file="笔记名" content="<追加内容>"

# === 属性 ===
obsidian vault=MyObsidian property:set file="笔记名" name="updated_at" value="YYYY-MM-DDTHH:mm:ss"

# === 移动（自动更新所有 wikilinks） ===
obsidian vault=MyObsidian move file="笔记名" to="目标目录/笔记名.md"

# === Daily ===
obsidian vault=MyObsidian daily:read
obsidian vault=MyObsidian daily:append content="<内容>"

# === 浏览 ===
obsidian vault=MyObsidian files folder="目录"
obsidian vault=MyObsidian folders
```

更多命令：`references/obsidian-cli.md` 或 `obsidian help`。

## 回退

如果 CLI 不可用（当前环境无法运行 `obsidian`），先说明原因。用户确认后，才可用文件工具直接操作 vault。
