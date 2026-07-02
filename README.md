# Knowledge Base

> 不是博客，而是**公开版 Obsidian**。
>
> 在 Obsidian 中沉淀知识 → 筛选成熟内容 → 通过 MkDocs 发布 → 形成公开知识网站。

一个公开的数字花园（Digital Garden）—— 知识、项目和思考通过双向链接编织成互联的知识图谱。

## 理念

```
Obsidian Vault（Second Brain）
        │
        │ 知识沉淀、筛选
        ▼
Material for MkDocs
        │
        │ GitHub Pages / Cloudflare Pages
        ▼
公开知识网站
```

- **Obsidian 是工作区**，MkDocs 是发布区
- 内容按**知识领域**组织，不按时间线
- 页面之间通过 `[[wikilink]]` 双向链接，形成类似 Wikipedia 的知识图谱
- 部分页面标记为 **Evergreen** 🌳—— 持续迭代更新，永不"完结"

## 网站栏目

| 栏目 | 说明 |
|------|------|
| 🏠 **Home** | 一句话介绍、当前学习动态、知识地图、项目概览、时间线 |
| 📚 **Knowledge** | 按计算机知识领域组织的知识树：CS 基础、软件工程、系统架构、系统设计、AI 工程、云原生 |
| 🚀 **Projects** | 每个项目一本文档：Vision → Architecture → ADR → API → 开发日志 |
| 💭 **Thinking** | 深度思考文章，形成个人品牌 |
| 🗺️ **Learning Roadmap** | 周学习日志、读书笔记、案例分析、ADR、Prompt 库 |
| 👤 **About** | 关于我和这个站点 |

## 功能特性

| 功能 | 说明 |
|------|------|
| 🔗 **双向链接** | `[[wikilink]]` 语法，自动生成反向链接（"哪些页面链接到了这里"） |
| 🏷️ **三维标签** | Level（难度）/ Type（类型）/ Status（状态）层次化标签系统 |
| 🌱 **数字花园** | 页面成长状态：🌱 Seedling（萌芽中）/ 🌳 Evergreen（持续更新） |
| 📝 **知识模板** | 统一文章结构：一句话理解 → 为什么出现 → 解决什么 → 什么时候不用 → 代码示例 → 我的理解 |
| 📰 **思考文章** | Thinking 栏目使用 Blog 插件，支持分类和分页 |
| 🔍 **中文搜索** | 针对中文优化分词，支持搜索高亮和搜索建议 |
| 🌓 **暗色模式** | 自动跟随系统主题切换亮色/暗色 |
| 📅 **更新日志** | Evergreen 页面展示内容更新历史时间线 |

## 本地开发

### 环境要求

- Python 3.10+
- pip

### 安装与运行

```bash
# 克隆仓库
git clone https://github.com/nuronalorange/knowledge-base.git
cd knowledge-base

# 安装依赖
pip install -r requirements.txt

# 启动本地开发服务器（支持热重载）
mkdocs serve
```

浏览器打开 `http://127.0.0.1:8000` 即可预览。修改 Markdown 文件后页面自动刷新。

### 构建

```bash
mkdocs build --clean
```

构建产物输出到 `site/` 目录。

## 内容编写指南

### 知识页面模板

每篇知识文章遵循固定结构。创建新页面时可使用 `<!-- kb:template -->` 快捷插入模板：

```markdown
---
title: 文章标题
tags:
  - Level/Beginner      # Beginner / Intermediate / Advanced / Expert
  - Type/Concept        # Concept / Pattern / Architecture / Tool / Case Study / Project
  - Status/Draft        # Draft / Learning / Reviewed / Completed
growth: evergreen        # 可选：标记为持续更新
updates:                 # 可选：更新记录
  - date: 2026-07-01
    note: 初版发布
---

## 一句话理解

## 为什么会出现

## 解决什么问题

## 什么时候不要用

## 代码示例

## 实际案例

## 我的理解

## 相关知识

## 推荐阅读
```

### Wikilinks 用法

使用 `[[文件名]]` 创建指向其他页面的链接，文件名即 slug：

```markdown
[[ddd]]                           → 链接到 ddd.md，显示页面标题
[[ddd|Domain-Driven Design]]      → 链接到 ddd.md，自定义显示文本
[[clean|Clean Architecture]]      → 链接到 clean.md
```

### 数字花园状态标记

在页面中插入以下短代码：

```markdown
<!-- kb:seedling -->   → 🌱 萌芽中（内容还在生长）
<!-- kb:evergreen -->  → 🌳 常青笔记（持续迭代更新）
<!-- kb:status Draft --> → 📝 状态徽章
<!-- kb:updates -->    → 渲染 front matter 中的更新日志
```

## 部署

推送到 `master` 分支即自动触发 GitHub Actions 构建部署：

```
git push → GitHub Actions → mkdocs build → GitHub Pages
```

站点地址：`https://nuronalorange.github.io/knowledge-base/`

## 项目结构

```
knowledge-base/
├── mkdocs.yml              # MkDocs 核心配置
├── requirements.txt        # Python 依赖
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Pages 自动部署
├── overrides/              # 主题定制
│   ├── main.html           # 扩展模板（反向链接区块）
│   ├── home.html           # 自定义首页（7 板块布局）
│   └── hooks/
│       ├── wikilinks.py    # 双向链接引擎（核心）
│       └── shortcodes.py   # 数字花园徽章、更新日志
└── docs/                   # 所有 Markdown 内容
    ├── index.md            # 首页
    ├── _snippets/          # 可复用 Markdown 片段
    ├── knowledge/          # 知识树（7 个子域 × 25+ 篇文章）
    ├── projects/           # 项目文档
    ├── thinking/           # 思考文章（Blog 插件驱动）
    ├── roadmap/            # 学习路线
    │   ├── weekly/         # 周学习日志
    │   ├── book-notes/     # 读书笔记
    │   ├── case-study/     # 案例分析
    │   ├── adr/            # 架构决策记录
    │   └── prompt-library/ # AI Prompt 库
    └── about/              # 关于
```

## 技术栈

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) — 静态站点生成器
- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/) — Markdown 扩展生态
- [Mermaid](https://mermaid.js.org/) — 文本驱动图表
- [GitHub Pages](https://pages.github.com) — 静态托管
- [GitHub Actions](https://github.com/features/actions) — CI/CD 自动部署

## 灵感来源

- **Digital Garden** — Joel Hooks, Maggie Appleton
- **Zettelkasten** — Niklas Luhmann
- **Second Brain** — Tiago Forte
- **Evergreen Notes** — Andy Matuschak
- **Obsidian** — 双向链接知识管理工具
