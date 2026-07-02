---
title: "ADR 002: Use Wikilinks for Knowledge Linking"
date: 2026-07-02
status: accepted
tags:
  - Type/Architecture
  - Status/Completed
---

# ADR 002: Use Wikilinks for Knowledge Linking

## Status

**Accepted** (2026-07-02)

## Context

The Knowledge Base should feel like a connected graph, not isolated pages.
Standard Markdown links are one-directional and don't show readers what
other pages reference the current one.

## Decision

Implement a custom Python hook (`overrides/hooks/wikilinks.py`) that:

1. Parses wikilink syntax (double-bracket links) in all Markdown files
2. Converts wikilinks to standard Markdown links at build time
3. Builds a reverse index of backlinks (who links to whom)
4. Injects a "Related Pages" section at the bottom of each page

## Alternatives Considered

| Alternative | Why Rejected |
|---|---|
| Standard Markdown links only | No backlinks; pages feel isolated |
| `mkdocs-wikilinks-plugin` | Third-party, may break with updates |
| `mkdocs-roamlinks-plugin` | Adds extra dependency for simple functionality |
| Manual `links` front matter | Too much manual maintenance; doesn't scale |

## Consequences

- ✅ Wikilink syntax identical to Obsidian
- ✅ Automatic backlinks without manual maintenance
- ✅ Unresolved wikilinks visibly highlighted during authoring
- ✅ No external plugin dependency
- ❌ Hook must be maintained alongside mkdocs-material upgrades
- ❌ Build-time only — no runtime wikilink resolution
