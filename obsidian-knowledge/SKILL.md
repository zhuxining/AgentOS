---
name: obsidian-knowledge
description: 在共享 MyObsidian vault 中用 Obsidian CLI 检索、创建、更新和整理笔记。适用于记录信息、查找知识、保存资料、维护 _AgentSpace、更新 frontmatter、处理 wikilinks、追加每日笔记和整理 Obsidian 知识库。
---

# Obsidian Knowledge

你与用户共享 `MyObsidian` vault。用户通过 Obsidian UI 使用知识库，你默认通过 Obsidian CLI 操作。

本 skill 只提供通用操作协议。具体目录、标签、frontmatter、隐私边界和输出规则以 vault 根目录 `AGENTS.md` 为准，不在本 skill 中复制维护。

## Core Rules

1. 每个会话首次操作 vault 前，先读取共享规范：

```bash
obsidian vault=MyObsidian read file="AGENTS"
```

2. 默认使用 Obsidian CLI。`vault=MyObsidian` 始终作为第一个参数。
3. 不读取、不修改 `AGENTS.md` 标记为禁止访问的目录或带隐私标签的笔记，特别是 `02_Privacy/`、`99_Plugconfig/`、`#Private`、`#Key`。
4. 新建或更新笔记时遵循 `AGENTS.md` 的 frontmatter 标准，并更新 `updated_at`。
5. Daily 是用户使用知识库的重要入口；所有新进入知识库的内容都必须在 Daily 留下 log。
6. 未指定目录时，新建的独立笔记放入 `00_Inbox/`；简单记录只追加到 Daily。
7. 内部链接使用从 vault 根目录开始的相对路径 wikilinks。
8. `_AgentSpace/` 是 Agent 自主管理区：可在其中增删改文件；把文件移出 `_AgentSpace/` 前必须得到用户确认。

## CLI First

常用命令：

```bash
# 读取
obsidian vault=MyObsidian read file="笔记名"
obsidian vault=MyObsidian read path="目录/笔记.md"

# 搜索
obsidian vault=MyObsidian search query="关键词" limit=20
obsidian vault=MyObsidian search:context query="关键词" limit=20

# 创建或覆写
obsidian vault=MyObsidian create path="00_Inbox/标题.md" content="<完整内容>" silent
obsidian vault=MyObsidian create path="00_Inbox/标题.md" content="<完整内容>" overwrite silent

# 追加
obsidian vault=MyObsidian append file="笔记名" content="<新增内容>"

# Daily
obsidian vault=MyObsidian daily:read
obsidian vault=MyObsidian daily:append content="<内容>"
obsidian vault=MyObsidian daily:prepend content="- [ ] <任务>"

# 属性
obsidian vault=MyObsidian property:set file="笔记名" name="updated_at" value="YYYY-MM-DDTHH:mm:ss"

# 移动
obsidian vault=MyObsidian move file="笔记名" to="目标目录/笔记名.md"
```

需要更多命令细节时再读取 `references/obsidian-cli.md`。

## General Workflow

### Read / Retrieve

1. 先读取 `AGENTS.md`，确认目录和隐私规则。
2. 用 `search` 或 `search:context` 找候选笔记。
3. 排除隐私目录、插件配置目录和明显敏感结果。
4. 读取相关笔记，基于内容回答。
5. 回答中用 `[[路径/笔记]]` 指向相关 vault 笔记。

### Create

1. 按用户指定目录创建；未指定则放 `00_Inbox/`。
2. 根据 `AGENTS.md` 写 frontmatter。`_AgentSpace/` 笔记额外加入 `source: ai-generated` 和 `managed-by: agent`。
3. 正文保持简洁，只有需要结构化组织时使用 H2-H6。
4. 用 `obsidian create ... silent` 创建。
5. 在 Daily 追加 log，包含新笔记 wikilink 和一句话上下文。

**存储位置规则**：
- 原始内容（文章剪藏、网页抓取）→ `10_AgentClips/`
- 领域剖析/知识整理 → `<领域目录>/_AgentSpace/`
- 用户明确要求放在父目录的整理笔记 → `<领域目录>/`（需用户确认）
- 简单想法、待办、一句话记录 → 只追加 Daily，不创建独立笔记

Frontmatter 模板以 `AGENTS.md` 为准，通常形态如下：

```yaml
---
title: Note Title
tags:
  - Domain/Topic
overview:
confidence:
created_at: YYYY-MM-DDTHH:mm:ss
updated_at: YYYY-MM-DDTHH:mm:ss
refs: []
source: ai-generated
managed-by: agent
---
```

**字段说明**：
- `source: ai-generated` — 标识内容由 AI 生成
- `managed-by: agent` — 标识由 Agent 自主管理，可在 `_AgentSpace/` 内自由增删改

### Update

1. 先读取当前笔记，不盲目覆盖。
2. 小追加优先用 `append`。
3. frontmatter 字段优先用 `property:set`。
4. 需要重写正文时，用 `create path=... overwrite silent` 写入完整新内容。
5. 每次更新同步更新 `updated_at`。
6. 如果更新实质新增知识内容，在 Daily 追加 log，说明更新了哪篇笔记。
7. 如果读到内容包含 `#Private` 或 `#Key`，立即停止操作并告知用户。

### Move / Rename

1. 优先使用 `obsidian move`，让 Obsidian 自动更新 wikilinks。
2. 移动 `_AgentSpace/` 内部文件可以直接执行。
3. 将 `_AgentSpace/` 文件移出父目录前，先向用户确认。
4. 不移动 `02_Privacy/`、`99_Plugconfig/` 或其他 `AGENTS.md` 禁止操作的目录。

## Daily Entry

Daily 是用户阅读和回溯知识库的入口。任何新保存、创建或沉淀到 vault 的内容，都要在当天 Daily 留下 log。

### Daily log 的最低要求

- 说明新增了什么内容
- 链接到对应笔记；简单记录没有独立笔记时，记录正文就是 log
- 用一句话说明保存原因或核心上下文

### 格式选择

**简单记录**（一句话、想法、待办）：
```markdown
- 简短记录或待办
- 新增 [[00_Inbox/标题|标题]]：一句话上下文
- 更新 [[领域目录/_AgentSpace/知识标题|知识标题]]：一句话说明
```

**资料沉淀**（文章、报告、深度分析）：使用 Knowledge Capture 中的二级标题块格式（包含"核心要旨""剪切原文""完整领域剖析"）

## Knowledge Capture

职责边界：

- 内容理解、摘要、要点、实体和领域剖析来自 `read`。
- 本技能只负责基于 `read` 的分析结果写入 vault，并建立 Daily、原文、领域剖析之间的链接。
- 如果用户给的是 URL、正文、文章或报告，但尚未分析，先委托 `read`；不要在本技能内重新做文章分析。

先判断保存粒度：

- **简单记录**：用户只是要求记一句话、一个想法、一个待办或一个轻量结论时，只追加到 Daily，不创建独立笔记。
- **资料沉淀**：用户要求保存网页、文章、报告、资料、对话摘录，或内容需要后续领域剖析时，使用三段式存储。

使用 `read` 的分析结果：

- 标题和 URL 用于命名、`refs` 和 Daily 链接上下文。
- 摘要和关键要点写入 Daily 的“核心要旨”。
- 干净 Markdown 正文写入 `10_AgentClips/`；如果不可用，则保存可用正文、URL 和提取失败说明。
- 分析内容写入对应领域 `_AgentSpace/`。
- 领域目录由本技能按 `AGENTS.md` 判断；用户明确指定时优先。
- 保存粒度由用户意图决定；无法判断时按”简单记录”和”资料沉淀”的边界选择

### 简单记录

只追加到 Daily，不创建独立笔记：

```bash
obsidian vault=MyObsidian daily:append content=”- <简短记录内容>”
```

示例：
```markdown
- 想法：应该重新考虑项目的技术方案
- 待办：周三前完成 SEA 财报分析
- 记录：用户提到需要关注 Q3 的电商数据
```

资料沉淀：

1. **原始内容**：保存到 `10_AgentClips/`，尽量保留原文、来源 URL、抓取时间和必要上下文。
2. **每日记录**：在 Daily 中追加一个二级标题块，聚合”文章核心要旨、剪切原文 wikilink、完整领域剖析 wikilink”。
3. **领域剖析**：将完整分析写入对应领域的 `_AgentSpace/`，正文必须链接回 `10_AgentClips/` 原文。

**存储位置确认**：
- 领域剖析笔记**必须**放入 `_AgentSpace/` 子目录，不是父目录
- 只有用户明确要求时，才将整理后的笔记放在领域根目录

完整资料沉淀时，三者必须互相关联：

- `10_AgentClips/` 原始笔记的 `refs` 记录外部来源；正文**结尾必须添加**链接到领域剖析笔记的”## 领域剖析”章节
- Daily 二级标题块同时包含原文 wikilink 和领域剖析 wikilink，后续阅读时可从这里跳转
- `_AgentSpace/` 领域剖析笔记的 `refs` 指向 `10_AgentClips/` 原始笔记，正文开头链接原文，并可链接相关领域笔记

Daily 追加内容格式（资料沉淀完整版）：

```markdown
## 文章标题

### 核心要旨
- 要点 1：关键判断或数据
- 要点 2：重要结论
- 要点 3：行动建议或关注点

### 剪切原文
- [[10_AgentClips/标题|标题]]

### 完整领域剖析
- [[<领域目录>/_AgentSpace/知识标题|知识标题]]
```

Daily 追加内容格式（仅保存原文）：

```markdown
## 文章标题

### 核心要旨
- 要点 1：关键判断
- 要点 2：重要结论

### 剪切原文
- [[10_AgentClips/标题|标题]]
```

CLI 操作顺序：

```bash
# 1. 创建原始内容笔记
obsidian vault=MyObsidian create path=”10_AgentClips/标题.md” content=”<原始内容笔记>” silent

# 2. 创建领域剖析笔记（放入 _AgentSpace/）
obsidian vault=MyObsidian create path=”<领域目录>/_AgentSpace/知识标题.md” content=”<分析知识笔记>” silent

# 3. 在 Daily 追加二级标题块
obsidian vault=MyObsidian daily:append content=”<Daily 二级标题块>”

# 4. 在原始笔记追加领域剖析链接（必须在创建领域剖析之后）
obsidian vault=MyObsidian append path=”10_AgentClips/标题.md” content=”\n\n## 领域剖析\n- [[<领域目录>/_AgentSpace/知识标题|知识标题]]”
```

**关键顺序**：先创建领域剖析笔记，再追加链接到原始笔记，确保链接目标已存在。

如果用户只要求保存原文，不强制生成领域剖析笔记；此时 Daily 二级标题块保留”核心要旨”和”剪切原文”，省略”完整领域剖析”。

## Delegation

保持本 skill 简单。只有在任务需要专门格式或复杂内容生产时，才使用其他 skill：

- 阅读、摘要、文章分析、实体提取：`read`
- URL 正文提取：`fetch`
- 外部资料搜索：`search`
- 复杂 Obsidian Markdown：`obsidian-markdown`
- `.base`：`obsidian-bases`
- `.canvas`：`json-canvas`
- 结构化文档/方案：`doc-coauthoring`
- 内部沟通稿：`internal-comms`

普通 vault CRUD、搜索、追加、移动、frontmatter 更新，直接使用 Obsidian CLI 完成。

## Fallback

如果当前环境无法运行 Obsidian CLI：

1. 不要在已确认会崩溃的宿主环境中反复调用桌面 App 入口。
2. 先说明 CLI 不可用的原因。
3. 对只读任务，可请用户导出命令输出到当前工作目录后继续。
4. 只有在用户确认且权限允许时，才用文件工具直接编辑 vault 文件。
