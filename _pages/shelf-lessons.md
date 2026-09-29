---
layout: page
title: Shelf Exam Lessons
permalink: /shelf-lessons/
---

<div id="shelf-explorer">
  <p class="sx-sub">Cards with a Step 2 <code>!Shelf</code> tag, grouped by shelf exam and then by lesson in Boards &amp; Beyond or OnlineMedEd, with the number of Anki cards tagged to each.</p>

  <div class="sx-stats" id="sx-stats">
    <div class="sx-stat"><span class="sx-stat-label">All</span><span class="sx-stat-value" id="sx-stat-total">–</span></div>
  </div>
  <p class="sx-note">Many cards are tagged to more than one shelf, so the shelf totals add up to more than "All". Counts are unique cards: a card tagged to two lessons in the same chapter counts once for the chapter.</p>

  <div class="sx-toggle" role="tablist" aria-label="Resource">
    <button type="button" role="tab" data-tree="bnb" aria-selected="true">Boards &amp; Beyond</button>
    <button type="button" role="tab" data-tree="ome" aria-selected="false">OnlineMedEd</button>
  </div>
  <p class="sx-coverage" id="sx-coverage"></p>

  <div class="sx-controls">
    <input type="text" id="sx-search" placeholder="Filter by shelf, subject, chapter, or lesson…" autocomplete="off">
    <button id="sx-expand-all">Expand all</button>
    <button id="sx-collapse-all">Collapse all</button>
  </div>

  <div id="sx-status" class="sx-status">Loading…</div>
  <div id="sx-tree" hidden></div>
</div>

<style>
#shelf-explorer { max-width: 800px; margin: 0 auto; }
#shelf-explorer .sx-sub { color: #666; font-size: 0.95em; margin-bottom: 1.2em; }
#shelf-explorer .sx-stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 10px; margin-bottom: 1.2em; }
#shelf-explorer .sx-stat { background: #f6f6f6; border-radius: 6px; padding: 0.6em 1em; }
#shelf-explorer .sx-stat-label { display: block; font-size: 0.75em; color: #888; text-transform: uppercase; letter-spacing: 0.03em; }
#shelf-explorer .sx-stat-value { display: block; font-size: 1.3em; font-weight: 600; font-variant-numeric: tabular-nums; }
#shelf-explorer .sx-note { color: #999; font-size: 0.8em; margin: -0.8em 0 1.2em; }
#shelf-explorer .sx-toggle { display: inline-flex; border: 1px solid #ddd; border-radius: 6px; overflow: hidden; margin-bottom: 0.4em; }
#shelf-explorer .sx-toggle button { padding: 0.5em 1em; border: none; background: #fff; font-size: 0.9em; cursor: pointer; }
#shelf-explorer .sx-toggle button + button { border-left: 1px solid #ddd; }
#shelf-explorer .sx-toggle button[aria-selected="true"] { background: #404040; color: #fff; }
#shelf-explorer .sx-coverage { color: #999; font-size: 0.8em; margin: 0 0 1em; }
#shelf-explorer .sx-controls { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1em; }
#shelf-explorer #sx-search { flex: 1; min-width: 180px; padding: 0.5em 0.7em; border: 1px solid #ddd; border-radius: 6px; font-size: 0.95em; }
#shelf-explorer .sx-controls button { padding: 0.5em 0.9em; border: 1px solid #ddd; border-radius: 6px; background: #fff; font-size: 0.85em; cursor: pointer; }
#shelf-explorer .sx-controls button:hover { background: #f6f6f6; }
#shelf-explorer .sx-status { color: #888; padding: 1em 0; }

#sx-tree details.lvl0 { background: #f6f6f6; border-radius: 8px; margin-bottom: 12px; overflow: hidden; }
#sx-tree details.lvl0 > summary { padding: 12px 14px; font-size: 16px; font-weight: 700; }
#sx-tree details.lvl0 > div { padding: 0 10px 8px; }
#sx-tree details.lvl1 { border-bottom: 1px solid #eee; }
#sx-tree details.lvl1:last-child { border-bottom: none; }
#sx-tree details.lvl1 > summary { padding: 10px 4px; font-size: 15px; font-weight: 600; }
#sx-tree details.deep > summary { padding: 7px 4px 7px 16px; font-size: 14px; border-left: 1px solid #ddd; margin-left: 4px; }
#sx-tree details.deep > div { padding-left: 16px; }
#sx-tree summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; gap: 8px; }
#sx-tree summary::-webkit-details-marker { display: none; }
#sx-tree summary > span:first-child::before { content: "▸"; display: inline-block; margin-right: 8px; font-size: 11px; color: #999; transition: transform 0.15s ease; }
#sx-tree details[open] > summary > span:first-child::before { transform: rotate(90deg); }
#sx-tree .sx-count { color: #999; white-space: nowrap; font-variant-numeric: tabular-nums; font-size: 0.85em; }
#sx-tree .sx-of { color: #bbb; font-weight: 400; }
#sx-tree .sx-leaf { display: flex; justify-content: space-between; gap: 8px; padding: 5px 4px 5px 16px; border-left: 1px solid #ddd; margin-left: 4px; font-size: 13px; color: #555; }
</style>

<script>
(function () {
  var DATA_URL = "{{ '/assets/data/shelf-lessons.json' | relative_url }}";
  var data = null, current = 'bnb', shelfTotals = {};

  var els = {
    status: document.getElementById('sx-status'),
    treeEl: document.getElementById('sx-tree'),
    stats: document.getElementById('sx-stats'),
    statTotal: document.getElementById('sx-stat-total'),
    coverage: document.getElementById('sx-coverage'),
    search: document.getElementById('sx-search'),
    expandAll: document.getElementById('sx-expand-all'),
    collapseAll: document.getElementById('sx-collapse-all'),
    tabs: document.querySelectorAll('#shelf-explorer .sx-toggle button'),
  };

  function s(i) { return data.s[i]; }
  function esc(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function fmt(n) { return n.toLocaleString(); }

  // node = [nameIndex, count, children?]; leaves carry the full path so filtering matches ancestors too
  function renderNode(node, depth, path) {
    var name = s(node[0]), cnt = node[1], kids = node[2];
    var text = path.concat(name);
    if (!kids) {
      return '<div class="sx-leaf" data-text="' + esc(text.join(' ').toLowerCase()) + '"><span>' + esc(name) + '</span><span class="sx-count">' + fmt(cnt) + '</span></div>';
    }
    var cls = depth === 0 ? 'lvl0' : depth === 1 ? 'lvl1' : 'deep';
    var countHtml = fmt(cnt);
    if (depth === 0) countHtml += ' <span class="sx-of">of ' + fmt(shelfTotals[name]) + '</span>';
    return '<details class="' + cls + '"' + (depth === 0 ? ' open' : '') + '><summary><span>' + esc(name) + '</span>' +
      '<span class="sx-count">' + countHtml + '</span></summary><div>' +
      kids.map(function (k) { return renderNode(k, depth + 1, text); }).join('') + '</div></details>';
  }

  function render() {
    var tree = data.trees[current];
    els.coverage.textContent = fmt(tree.tagged_cards) + ' of ' + fmt(data.total_cards) +
      ' shelf cards have a Step 2 ' + tree.label + ' tag. Each shelf shows its ' + tree.label + '-tagged cards out of its total.';
    els.treeEl.innerHTML = tree.shelves.map(function (sh) { return renderNode(sh, 0, []); }).join('');
    if (els.search.value.trim()) applyFilter();
  }

  // Returns true if anything under el is visible
  function filterEl(el, q) {
    if (el.classList.contains('sx-leaf')) {
      var match = el.getAttribute('data-text').indexOf(q) !== -1;
      el.style.display = match ? 'flex' : 'none';
      return match;
    }
    var any = false;
    Array.prototype.forEach.call(el.querySelector(':scope > div').children, function (child) {
      if (filterEl(child, q)) any = true;
    });
    el.style.display = any ? '' : 'none';
    el.open = any;
    return any;
  }

  function applyFilter() {
    var q = els.search.value.trim().toLowerCase();
    if (!q) {
      els.treeEl.querySelectorAll('.sx-leaf').forEach(function (li) { li.style.display = 'flex'; });
      els.treeEl.querySelectorAll('details').forEach(function (d) {
        d.style.display = '';
        d.open = d.classList.contains('lvl0');
      });
      return;
    }
    Array.prototype.forEach.call(els.treeEl.children, function (shelf) { filterEl(shelf, q); });
  }

  els.search.addEventListener('input', applyFilter);
  els.expandAll.addEventListener('click', function () {
    els.treeEl.querySelectorAll('details').forEach(function (d) { d.open = true; });
  });
  els.collapseAll.addEventListener('click', function () {
    els.treeEl.querySelectorAll('details').forEach(function (d) { d.open = false; });
  });
  els.tabs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      current = btn.getAttribute('data-tree');
      els.tabs.forEach(function (b) { b.setAttribute('aria-selected', b === btn ? 'true' : 'false'); });
      if (data) render();
    });
  });

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (d) {
      data = d;
      els.statTotal.textContent = fmt(data.total_cards);
      els.stats.insertAdjacentHTML('beforeend', data.shelves.map(function (sh) {
        shelfTotals[s(sh[0])] = sh[1];
        return '<div class="sx-stat"><span class="sx-stat-label">' + esc(s(sh[0])) + '</span><span class="sx-stat-value">' + fmt(sh[1]) + '</span></div>';
      }).join(''));
      els.status.hidden = true;
      els.treeEl.hidden = false;
      render();
    })
    .catch(function (err) {
      els.status.textContent = 'Could not load shelf data (' + err.message + '). Check that shelf-lessons.json is in /assets/data/.';
    });
})();
</script>
