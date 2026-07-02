"""
Shortcodes Hook — Digital Garden Status Badges and Update Logs.

Provides HTML-comment-based shortcodes for page content enrichment:

    <!-- kb:seedling -->     → Renders a "Seedling" growth stage badge
    <!-- kb:evergreen -->    → Renders an "Evergreen" growth stage badge
    <!-- kb:status Draft --> → Renders a custom status badge (any status text)
    <!-- kb:updates -->      → Renders the update history timeline from front matter
    <!-- kb:template -->     → Inserts a knowledge article template guide

These shortcodes are inspired by the Material for MkDocs documentation's
own shortcode system (material/overrides/hooks/shortcodes.py).
"""

from __future__ import annotations

import re
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


# -----------------------------------------------------------------------------
# Hook: on_page_markdown
# -----------------------------------------------------------------------------

def on_page_markdown(
    markdown: str, *, page: Page, config: MkDocsConfig, files: Files
) -> str:
    """
    Process <!-- kb:* --> shortcodes in page Markdown.
    """

    def replace(match: re.Match) -> str:
        shortcode = match.group(1).strip()
        args = match.group(2).strip() if match.group(2) else ""

        if shortcode == "seedling":
            return _badge_growth("🌱 Seedling", "seedling",
                                "This note is young and still growing.")
        elif shortcode == "evergreen":
            return _badge_growth("🌳 Evergreen", "evergreen",
                                "This page is continuously updated as I learn and apply.")
        elif shortcode == "status":
            return _badge_status(args, args.lower())
        elif shortcode == "updates":
            return _render_updates(page)
        elif shortcode == "template":
            return _render_knowledge_template()

        # Unknown shortcode
        return match.group(0)

    return re.sub(
        r"<!-- kb:(\w+)(?:\s+(.*?))?\s*-->",
        replace,
        markdown,
        flags=re.IGNORECASE,
    )


# -----------------------------------------------------------------------------
# Badge Generators
# -----------------------------------------------------------------------------

def _badge_growth(
    text: str, css_class: str, tooltip: str = ""
) -> str:
    """
    Render a growth-stage badge (seedling, evergreen).

    Args:
        text: Display text (e.g., "🌱 Seedling")
        css_class: CSS class suffix (e.g., "seedling")
        tooltip: Optional tooltip text
    """
    title_attr = f' title="{tooltip}"' if tooltip else ""
    return (
        f'<span class="kb-badge kb-badge--growth kb-badge--{css_class}"'
        f'{title_attr}>'
        f'{text}'
        f'</span>'
    )


def _badge_status(
    text: str, css_class: str
) -> str:
    """
    Render a content status badge.

    Args:
        text: Display text (e.g., "Draft")
        css_class: CSS class suffix (e.g., "draft")
    """
    return (
        f'<span class="kb-badge kb-badge--status kb-badge--{css_class}">'
        f'📝 {text}'
        f'</span>'
    )


# -----------------------------------------------------------------------------
# Update Log Renderer
# -----------------------------------------------------------------------------

def _render_updates(page: Page) -> str:
    """
    Render the update history from front matter 'updates' list.

    Front matter format:
        updates:
          - date: 2026-07-01
            note: Initial draft
          - date: 2026-08-15
            note: Added practical examples

    Returns HTML for an update history section, or empty string if no updates.
    """
    updates = page.meta.get("updates", [])
    if not updates:
        return ""

    lines = [
        '<div class="kb-updates">',
        '<h3>📅 Update History</h3>',
        '<ul class="kb-updates__list">',
    ]

    for update in updates:
        date = update.get("date", "")
        note = update.get("note", "")
        lines.append(
            f'<li class="kb-updates__item">'
            f'<span class="kb-updates__date">{date}</span>'
            f'<span class="kb-updates__note">{note}</span>'
            f'</li>'
        )

    lines.append("</ul>")
    lines.append("</div>")

    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Knowledge Template Guide
# -----------------------------------------------------------------------------

def _render_knowledge_template() -> str:
    """
    Insert the knowledge article template structure as a guide.

    This provides a visual checklist of the standard sections for a knowledge
    article, following the Knowledge Base content template.
    """
    sections = [
        ("一句话理解", "A single sentence that captures the essence"),
        ("为什么会出现", "Historical context — what problem motivated this?"),
        ("解决什么问题", "What concrete problems does this solve?"),
        ("什么时候不要用", "Anti-patterns, trade-offs, when this is the wrong choice"),
        ("代码示例", "Runnable code that demonstrates the concept"),
        ("实际案例", "Real-world examples from well-known systems"),
        ("我的理解", "Personal insight — what you learned that's not in textbooks"),
        ("相关知识", "[[wikilinks]] to related concepts"),
        ("推荐阅读", "Books, articles, talks that go deeper"),
    ]

    lines = [
        '<details class="kb-template-guide">',
        '<summary>📋 Knowledge Article Template</summary>',
        '<div class="kb-template-guide__body">',
        '<ol>',
    ]

    for title, desc in sections:
        lines.append(
            f'<li><strong>{title}</strong><br><small>{desc}</small></li>'
        )

    lines.append('</ol>')
    lines.append('</div>')
    lines.append('</details>')

    return "\n".join(lines)
