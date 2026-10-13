---
layout: page
title: Surgical Recall Chapters
permalink: /surgical-recall-chapters/
---

{% capture sub %}Chapter &rarr; subsection for the Surgical Recall Anki deck, with the number of cards tagged to each. Chapters are in book order; most are tagged at the chapter level only, so they appear without subsections underneath.{% endcapture %}
{% include anki-tree-explorer.html data="surgical-recall-chapters.json" sub=sub top_label="Chapters" leaf_label="none" placeholder="Filter by chapter or subsection…" %}
