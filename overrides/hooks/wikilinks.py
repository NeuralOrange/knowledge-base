"""
Wikilinks Hook — Bidirectional Links Engine for Knowledge Base.

Provides [[wikilink]] syntax support with automatic backlink resolution.
This is the core feature that makes the Knowledge Base feel like a
connected knowledge graph rather than isolated pages.

Architecture:
    1. on_files      — Build a page index (slug → {title, url, src_uri})
    2. on_page_markdown — Replace [[target]] and [[target|display]] with links,
                           recording forward and back references
    3. on_page_context  — Inject backlinks into template context

Wikilink Syntax:
    [[page-slug]]           → Link to page, display = page title
    [[page-slug|My Text]]   → Link to page, custom display text
    [[page-slug#heading]]   → Link to anchor within a page

Module-level state is used to persist data across hook invocations
during a single build — required because on_files, on_page_markdown,
and on_page_context are separate callbacks.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import Optional

from jinja2 import pass_environment
from markdown import Markdown
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page

log = logging.getLogger("mkdocs.material.knowledge.wikilinks")

# -----------------------------------------------------------------------------
# Module-level build state (persists across hook calls during one build)
# -----------------------------------------------------------------------------

# slug → {title, url, src_uri}
# Example: "knowledge/software-architecture/ddd" → {title: "DDD", url: "...", ...}
_page_index: dict[str, dict] = {}

# source page url → [target url, ...]
_forward_links: dict[str, list[str]] = defaultdict(list)

# target url → [(source url, source title), ...]
# Each tuple is unique — duplicates from multiple wikilinks to the same target
# from the same source are deduplicated.
_backlinks: dict[str, list[tuple[str, str]]] = defaultdict(list)

# -----------------------------------------------------------------------------
# Regex pattern for wikilinks
# -----------------------------------------------------------------------------
# Matches:
#   [[target]]              — group(1)=target, group(2)=anchor(None), group(3)=display(None)
#   [[target#heading]]       — group(1)=target, group(2)=anchor, group(3)=display(None)
#   [[target|display]]       — group(1)=target, group(2)=anchor(None), group(3)=display
#   [[target#heading|text]]  — group(1)=target, group(2)=anchor, group(3)=display
_WIKILINK_PATTERN = re.compile(
    r"\[\["
    r"([^\]|#]+)"          # target slug (no ], |, or #)
    r"(?:#([^\]|]+))?"     # optional anchor
    r"(?:\|([^\]]+))?"     # optional display text
    r"\]\]"
)

# Characters to strip from wikilink slugs for normalization
_SLUG_NORMALIZE_PATTERN = re.compile(r"[^\w\-/]+")


# -----------------------------------------------------------------------------
# Markdown filter for templates (e.g., home page sections)
# -----------------------------------------------------------------------------

# Reusable Markdown instance for the template filter
_md = Markdown(
    extensions=[
        "admonition",
        "attr_list",
        "def_list",
        "footnotes",
        "md_in_html",
        "pymdownx.details",
        "pymdownx.emoji",
        "pymdownx.highlight",
        "pymdownx.inlinehilite",
        "pymdownx.keys",
        "pymdownx.mark",
        "pymdownx.superfences",
        "pymdownx.tasklist",
        "pymdownx.tilde",
    ]
)


def on_env(env, *, config: MkDocsConfig, **kwargs):
    """
    Register custom Jinja2 filters.

    Adds a 'markdown' filter that converts Markdown text to HTML,
    used by the home page template to render front matter sections.
    """

    @pass_environment
    def markdown_filter(ctx, text: str) -> str:
        """Convert Markdown text to HTML."""
        if not text:
            return ""
        # Reset the Markdown instance for each conversion
        _md.reset()
        return _md.convert(text)

    env.filters["markdown"] = markdown_filter


# -----------------------------------------------------------------------------
# Hook: on_files
# -----------------------------------------------------------------------------

def on_files(files: Files, *, config: MkDocsConfig):
    """
    Build the page index from all documentation pages.

    Called once at the start of the build. For every .md file in the site,
    we derive a canonical slug from its source URI and pre-compute the URL.

    We register both the full-path slug and the short (filename-only) slug
    for convenient linking: [[ddd]] instead of [[knowledge/software-architecture/ddd]].

    URLs are pre-computed from dest_uri so that wikilinks resolve even when
    the target page hasn't been processed yet.
    """
    global _page_index, _forward_links, _backlinks

    # Reset state for each build
    _page_index.clear()
    _forward_links.clear()
    _backlinks.clear()

    page_count = 0
    for file in files.documentation_pages():
        slug = _slug_from_path(file.src_uri)
        if not slug:
            continue

        # Pre-compute URL from the destination URI
        # dest_uri: "knowledge/computer-science/algorithm/index.html"
        # url:      "knowledge/computer-science/algorithm/"
        url = _url_from_dest(file.dest_uri)

        # Store full slug (e.g., "knowledge/software-architecture/ddd")
        # The title is populated later in on_page_markdown (we use
        # the title from the last segment as fallback for display)
        fallback_title = slug.rsplit("/", 1)[-1].replace("-", " ").title() if slug else ""
        _page_index[slug] = {
            "title": fallback_title,
            "url": url,
            "src_uri": file.src_uri,
        }
        page_count += 1

        # Also register short slug (just the filename stem, e.g., "ddd")
        # This allows [[ddd]] instead of [[knowledge/software-architecture/ddd]]
        # Only register if not already taken (full path wins over short slug)
        short = slug.rsplit("/", 1)[-1]
        if short and short not in _page_index:
            _page_index[short] = _page_index[slug]

    log.info(f"Wikilinks: indexed {page_count} pages ({len(_page_index)} slugs)")


# -----------------------------------------------------------------------------
# Hook: on_page_markdown
# -----------------------------------------------------------------------------

def on_page_markdown(
    markdown: str, *, page: Page, config: MkDocsConfig, files: Files
) -> str:
    """
    Replace [[wikilinks]] with proper Markdown links.

    For each wikilink found:
    1. Resolve the target slug against the page index
    2. Convert to a standard Markdown link: [display](url)
    3. Record the forward link (source → target)
    4. Record the backlink (target → source)

    Unresolved wikilinks are wrapped in a <span> with CSS class
    'wikilink-unresolved' for visibility during authoring.
    """
    global _page_index, _forward_links, _backlinks

    # Update this page's entry in the index with its resolved title and URL
    slug = _slug_from_path(page.file.src_uri)
    if slug and slug in _page_index:
        _page_index[slug]["title"] = page.title
        _page_index[slug]["url"] = page.url

    # Track links FROM this page (reset per page — each page processed once)
    seen_targets: set[str] = set()

    def replace_wikilink(match: re.Match) -> str:
        target_raw = match.group(1).strip()
        anchor = match.group(2).strip() if match.group(2) else None
        display = match.group(3).strip() if match.group(3) else None

        # Normalize the target slug
        target_slug = _normalize_slug(target_raw)

        # Resolve target in page index
        info = _resolve_target(target_slug)

        if info and info.get("url"):
            target_url = info["url"]
            if anchor:
                # Slugify the anchor to match the auto-generated heading ID
                anchor_slug = _slugify_anchor(anchor)
                target_url = f"{target_url}#{anchor_slug}"

            resolved_display = display if display else info.get("title", target_raw)

            # Record links for backlink resolution (deduplicated per page)
            source_url = page.url
            link_key = f"{source_url}→{target_url}"
            if link_key not in seen_targets:
                seen_targets.add(link_key)
                _forward_links[source_url].append(target_url)

                entry = (source_url, page.title or source_url)
                if entry not in _backlinks[target_url]:
                    _backlinks[target_url].append(entry)

            return f"[{resolved_display}]({target_url})"

        else:
            # Unresolved wikilink — surface it visibly so the author can fix it
            resolved_display = display if display else target_raw
            log.warning(
                f"Wikilinks: unresolved [[{target_raw}]] in "
                f"'{page.file.src_uri}'"
            )
            return (
                f'<span class="wikilink-unresolved" '
                f'title="Unresolved wikilink: {target_raw}">'
                f'[[{resolved_display}]]'
                f'</span>'
            )

    return _WIKILINK_PATTERN.sub(replace_wikilink, markdown)


# -----------------------------------------------------------------------------
# Hook: on_page_context
# -----------------------------------------------------------------------------

def on_page_context(
    context: dict, *, page: Page, config: MkDocsConfig, nav
) -> None:
    """
    Inject backlinks into the page context for template rendering.

    The 'wikilinks_backlinks' variable contains:
        [(source_url, source_title), ...]

    It is rendered by the template (main.html) at the bottom of each page.
    """
    global _backlinks

    backlinks = _backlinks.get(page.url, [])

    if backlinks:
        context["wikilinks_backlinks"] = backlinks
        log.debug(
            f"Wikilinks: {len(backlinks)} backlink(s) for '{page.url}': "
            f"{[t for _, t in backlinks]}"
        )


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def _slug_from_path(src_uri: str) -> str:
    """
    Derive a wikilink slug from a file's source URI.

    Examples:
        "knowledge/software-architecture/ddd.md" → "knowledge/software-architecture/ddd"
        "knowledge/cloud/index.md"              → "knowledge/cloud"
        "index.md"                              → ""
        "thinking/posts/why-ddd-matters.md"    → "thinking/posts/why-ddd-matters"
    """
    if not src_uri:
        return ""

    # Remove file extension
    if "." in src_uri:
        slug = src_uri.rsplit(".", 1)[0]
    else:
        slug = src_uri

    # Strip trailing "/index"
    if slug.endswith("/index"):
        slug = slug[:-6]

    # Normalize to lowercase
    slug = slug.lower()

    return slug


def _normalize_slug(raw: str) -> str:
    """
    Normalize a wikilink target for matching against the page index.

    Handles:
    - Chinese characters in display text (when used as target)
    - Spaces and punctuation
    - Case normalization

    For filename-based linking, users should use hyphenated English slugs
    that match their filenames: [[clean-architecture]], [[ddd]], etc.
    """
    # Lowercase and strip whitespace
    slug = raw.lower().strip()

    # Replace spaces with hyphens
    slug = slug.replace(" ", "-")

    # Remove characters that wouldn't appear in file paths
    slug = _SLUG_NORMALIZE_PATTERN.sub("", slug)

    # Strip trailing "/index" — matches how _slug_from_path handles index.md
    # [[knowledge/index]] → "knowledge" (same as knowledge/index.md → "knowledge")
    if slug.endswith("/index") and slug != "index":
        slug = slug[:-6]

    return slug


def _resolve_target(target_slug: str) -> Optional[dict]:
    """
    Resolve a wikilink target slug against the page index.

    Resolution order:
    1. Exact match on normalized slug
    2. Short slug match (filename only, e.g., "ddd" → "knowledge/.../ddd")
    3. Contains match (e.g., "clean-architecture" → "knowledge/.../clean")
    4. Endswith match (file is named after the slug, e.g., "algorithm" → ".../algorithm")
    """
    # 1. Exact match (full slug or registered short slug)
    if target_slug in _page_index:
        return _page_index[target_slug]

    # 2. Suffix match: any slug ending with "/target_slug"
    suffix = f"/{target_slug}"
    for slug, info in _page_index.items():
        if slug.endswith(suffix):
            return info

    # 3. Last-segment match: target matches the filename part of a slug
    #    e.g., "ddd" matches "knowledge/software-architecture/ddd"
    for slug, info in _page_index.items():
        if slug.rsplit("/", 1)[-1] == target_slug:
            return info

    return None


def _url_from_dest(dest_uri: str) -> str:
    """
    Compute the page URL from its destination URI.

    MkDocs uses directory URLs by default, so:
        "index.html"                         → ""
        "knowledge/index.html"               → "knowledge/"
        "knowledge/computer-science/algo/index.html" → "knowledge/computer-science/algo/"
    """
    if not dest_uri:
        return ""

    url = dest_uri

    # Remove "index.html" suffix
    if url.endswith("/index.html"):
        url = url[:-10]  # strip "/index.html", keep trailing "/"
    elif url.endswith("index.html"):
        url = ""  # root index

    return url


def _slugify_anchor(text: str) -> str:
    """
    Convert heading text to the slug format used by MkDocs/Python-Markdown.

    This should match the toc extension's slugify function.
    We use a simplified version that works for ASCII text and common cases.
    """
    # Lowercase
    slug = text.lower().strip()

    # Replace spaces with hyphens
    slug = re.sub(r"\s+", "-", slug)

    # Remove non-word characters (except hyphens)
    slug = re.sub(r"[^\w\-]", "", slug)

    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)

    # Strip leading/trailing hyphens
    slug = slug.strip("-")

    return slug
