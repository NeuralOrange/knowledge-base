# Knowledge Base

> 不是博客，而是**公开版 Obsidian**。
>
> Obsidian（沉淀）→ 筛选 → MkDocs（发布）→ 公开网站

A public digital garden — knowledge, projects, and thinking organized as a connected graph through bidirectional links.

## 理念

```
Obsidian Vault (Second Brain)
        │
        │ 知识沉淀、筛选
        ▼
Material for MkDocs
        │
GitHub Pages / Cloudflare Pages
        │
公开网站
```

- **Obsidian 是工作区**，MkDocs 是发布区
- 内容按**知识领域**组织，不按时间
- 页面之间通过 `[[wikilink]]` 双向链接，形成知识图谱
- 部分页面是 **Evergreen** 🌳 — 持续更新，不会结束

## 目录结构

```
knowledge-base/
├── mkdocs.yml              # MkDocs 核心配置
├── requirements.txt        # Python 依赖
├── overrides/              # 主题定制
│   ├── main.html           # 扩展模板（backlinks 区块）
│   ├── home.html           # 自定义首页
│   └── hooks/
│       ├── wikilinks.py    # 双向链接引擎
│       └── shortcodes.py   # 数字花园徽章、更新日志
└── docs/                   # 所有内容
    ├── index.md            # 首页
    ├── knowledge/          # 知识树（7 个子域）
    ├── projects/           # 项目文档
    ├── thinking/           # 思考文章
    ├── roadmap/            # 学习路线
    │   ├── weekly/         # 周学习日志
    │   ├── book-notes/     # 读书笔记
    │   ├── case-study/     # 案例分析
    │   ├── adr/            # 架构决策记录
    │   └── prompt-library/ # AI Prompt 库
    └── about/              # 关于
```

## 功能

| 功能 | 说明 |
|------|------|
| 🔗 **双向链接** | `[[wikilink]]` 语法，自动生成反向链接 |
| 🏷️ **三维标签** | Level、Type、Status 层次化标签 |
| 🌱 **数字花园** | 页面成长状态：Seedling / Evergreen |
| 📝 **知识模板** | 统一的文章结构：一句话理解 → 为什么 → 什么时候不用 → 代码示例 → 我的理解 |
| 📚 **博客引擎** | Thinking 栏目使用 Blog 插件 |
| 🔍 **中文搜索** | 支持中文分词搜索 |
| 🌓 **暗色模式** | 自动跟随系统主题 |

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

# 启动本地预览
mkdocs serve
```

打开 `http://127.0.0.1:8000` 查看站点。修改 Markdown 文件后自动刷新。

### 构建

```bash
mkdocs build --clean
```

构建产物在 `site/` 目录。

## 内容规范

### 知识页面模板

每篇知识文章遵循固定结构：

```markdown
---
title: 文章标题
tags:
  - Level/Beginner      # Beginner / Intermediate / Advanced / Expert
  - Type/Concept        # Concept / Pattern / Architecture / Tool / Case Study / Project
  - Status/Draft        # Draft / Learning / Reviewed / Completed
growth: evergreen        # 可选：标记为持续更新页面
updates:                 # 可选：更新日志（用于 Evergreen 页面）
  - date: 2026-07-01
    note: 初版
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

### Wikilinks

使用 `[[filename]]` 创建指向其他页面的链接：

```markdown
- [[ddd|Domain-Driven Design]] — 链接到 ddd.md，显示为 "Domain-Driven Design"
- [[solid]] — 链接到 solid.md，显示为页面标题
- [[clean|Clean Architecture]] — 链接到 clean.md，自定义显示文本
```

文件名就是 slug：`ddd.md` → `[[ddd]]`，`clean.md` → `[[clean]]`。

### 数字花园状态

```markdown
<!-- kb:seedling -->   → 🌱 正在成长中
<!-- kb:evergreen -->  → 🌳 持续更新
<!-- kb:status Draft --> → 📝 内容状态徽章
<!-- kb:updates -->    → 渲染 front matter 中的更新日志
```

## 部署

推送到 `master` 分支，GitHub Actions 自动构建并部署到 GitHub Pages：

```
git push → GitHub Actions 触发 → mkdocs build → 部署到 Pages
```

站点地址：`https://nuronalorange.github.io/knowledge-base/`

## 技术栈

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) — 静态站点生成
- [Python Markdown Extensions](https://facelessuser.github.io/pymdown-extensions/) — Markdown 扩展
- [GitHub Pages](https://pages.github.com) — 托管
- [GitHub Actions](https://github.com/features/actions) — CI/CD

## 致谢

受以下概念启发：

- **Digital Garden** — Joel Hooks, Maggie Appleton
- **Zettelkasten** — Niklas Luhmann
- **Second Brain** — Tiago Forte
- **Evergreen Notes** — Andy Matuschak
- **Obsidian** — 双向链接知识管理工具
