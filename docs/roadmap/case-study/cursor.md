---
title: "Case Study: Cursor"
tags:
  - Level/Advanced
  - Type/Case Study
  - Status/Draft
product: Cursor
company: Anysphere
---

# Case Study: Cursor — AI-Native IDE

## What Is Cursor?

Cursor is a fork of VS Code that deeply integrates AI into the coding
experience — not as a chat sidebar, but as a fundamental part of how
you write, edit, and understand code.

## Key Architecture Decisions

### 1. VS Code Fork vs. Standalone

Cursor chose to fork VS Code rather than build a standalone editor.
This gave them the entire VS Code ecosystem (extensions, themes, LSP)
for free, while allowing deep modifications to the editor core.

### 2. AI as Editor Primitive, Not Add-on

Unlike Copilot (which adds AI on top), Cursor makes AI a first-class
editor action: Tab to accept, Cmd+K to edit, inline diffs for review.
This changes the interaction model from "ask AI" to "AI is part of typing."

### 3. Context Management

Cursor's "Rules for AI" and `.cursorrules` file are essentially prompt
engineering tools embedded in the development workflow. They recognized
that context is the most valuable resource in AI-assisted coding.

## Lessons for Software Architecture

1. **Fork with purpose** — sometimes the fastest path is to fork a
   platform and modify its core, rather than building from scratch
2. **AI changes UX primitives** — AI tools need new interaction models,
   not just new API calls
3. **Context is architecture** — managing what the AI sees is as
   important as managing what the user sees

## Related

- [[agent|AI Agent]]
- [[prompt|Prompt Engineering]]
