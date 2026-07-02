---
title: "ADR 001: Use MkDocs Material for Knowledge Base"
date: 2026-07-01
status: accepted
tags:
  - Type/Architecture
  - Status/Completed
---

# ADR 001: Use MkDocs Material for Knowledge Base

## Status

**Accepted** (2026-07-01)

## Context

I need a static site to publish my knowledge, projects, and thinking.
The site should feel like a "public Obsidian" — not a blog, but a knowledge
graph that grows over time.

Key requirements:
1. Bidirectional links (wikilinks with backlinks)
2. Hierarchical navigation and tags
3. Full-text search with Chinese support
4. Markdown-first authoring (compatible with Obsidian)
5. Easy deployment to GitHub Pages

## Decision

Use **Material for MkDocs** as the static site generator.

## Alternatives Considered

| Alternative | Why Rejected |
|---|---|
| WordPress | Too heavy; not Markdown-native; hard to version control |
| Hugo | Good but less polished theme; no built-in wikilinks |
| Docusaurus | React-based; overkill for a personal site |
| Obsidian Publish | Locked into Obsidian ecosystem; limited customization |
| Quartz | Great for digital gardens but less polished |

## Consequences

- ✅ Markdown-first, Obsidian-compatible
- ✅ Beautiful, responsive theme out of the box
- ✅ Built-in blog, tags, search plugins
- ✅ Easy GitHub Pages deployment
- ❌ No built-in wikilinks — need custom Python hook
- ❌ No digital garden maturity tracking — need custom implementation
- ❌ Learning curve for mkdocs configuration and Python hooks
