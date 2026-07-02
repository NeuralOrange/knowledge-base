/**
 * Knowledge Base — Custom JavaScript
 *
 * Client-side enhancements:
 * - Backlink hover previews (future)
 * - Knowledge graph visualization (future)
 * - Active section tracking (future)
 */

document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  // Log that the Knowledge Base custom JS is loaded
  if (window.console && window.console.log) {
    console.log("🌱 Knowledge Base — custom.js loaded");
  }

  // Mark unresolved wikilinks with a click handler that scrolls to them
  // (helps authors find broken links during mkdocs serve)
  document.querySelectorAll(".wikilink-unresolved").forEach(function (el) {
    el.title = el.title || "Unresolved wikilink — page not found";
  });
});
