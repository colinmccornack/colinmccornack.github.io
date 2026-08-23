---
layout: page
title: Bootcamp × B&B Overlap
permalink: /bootcamp-bnb-overlap/
---

<div id="overlap-explorer">
  <p class="oe-sub">Every lesson pair that shares at least one Anki card between Bootcamp and Boards &amp; Beyond, sorted by how many cards link them.</p>

  <div class="oe-stats">
    <div class="oe-stat"><span class="oe-stat-label">Pairs</span><span class="oe-stat-value" id="oe-stat-total">–</span></div>
    <div class="oe-stat"><span class="oe-stat-label">Showing</span><span class="oe-stat-value" id="oe-stat-shown">–</span></div>
  </div>

  <div class="oe-controls">
    <input type="text" id="oe-search" placeholder="Search subject, chapter, or lesson…" autocomplete="off">
    <select id="oe-step">
      <option value="">All B&amp;B steps</option>
      <option value="Step 1">Step 1</option>
      <option value="Step 2">Step 2</option>
    </select>
    <select id="oe-min-count">
      <option value="1">1+ shared card</option>
      <option value="2">2+ shared cards</option>
      <option value="5">5+ shared cards</option>
      <option value="10">10+ shared cards</option>
    </select>
  </div>

  <div id="oe-status" class="oe-status">Loading overlap data…</div>

  <table id="oe-table" class="oe-table" hidden>
    <thead>
      <tr>
        <th class="oe-col-bc">Bootcamp</th>
        <th class="oe-col-bnb">Boards &amp; Beyond</th>
        <th class="oe-col-n">Shared</th>
      </tr>
    </thead>
    <tbody id="oe-tbody"></tbody>
  </table>

  <div class="oe-pager">
    <button id="oe-prev">← Prev</button>
    <span id="oe-page-label"></span>
    <button id="oe-next">Next →</button>
  </div>
</div>

<style>
#overlap-explorer { max-width: 900px; margin: 0 auto; }
#overlap-explorer .oe-sub { color: #666; font-size: 0.95em; margin-bottom: 1.2em; }
#overlap-explorer .oe-stats { display: flex; gap: 12px; margin-bottom: 1.2em; }
#overlap-explorer .oe-stat { background: #f6f6f6; border-radius: 6px; padding: 0.6em 1em; }
#overlap-explorer .oe-stat-label { display: block; font-size: 0.75em; color: #888; text-transform: uppercase; letter-spacing: 0.03em; }
#overlap-explorer .oe-stat-value { display: block; font-size: 1.3em; font-weight: 600; }
#overlap-explorer .oe-controls { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1em; }
#overlap-explorer #oe-search { flex: 1; min-width: 180px; padding: 0.5em 0.7em; border: 1px solid #ddd; border-radius: 6px; font-size: 0.95em; }
#overlap-explorer select { padding: 0.5em 0.6em; border: 1px solid #ddd; border-radius: 6px; font-size: 0.9em; background: #fff; }
#overlap-explorer .oe-status { color: #888; padding: 1em 0; }
#overlap-explorer .oe-table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
#overlap-explorer .oe-table th { text-align: left; border-bottom: 2px solid #333; padding: 0.5em 0.6em; font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.02em; }
#overlap-explorer .oe-table td { padding: 0.55em 0.6em; border-bottom: 1px solid #eee; vertical-align: top; }
#overlap-explorer .oe-col-n { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
#overlap-explorer .oe-lesson { display: block; font-weight: 600; }
#overlap-explorer .oe-path { display: block; color: #888; font-size: 0.85em; }
#overlap-explorer .oe-pager { display: flex; align-items: center; justify-content: center; gap: 1em; margin-top: 1.2em; }
#overlap-explorer .oe-pager button { padding: 0.4em 0.9em; border: 1px solid #ddd; border-radius: 6px; background: #fff; cursor: pointer; }
#overlap-explorer .oe-pager button:disabled { opacity: 0.4; cursor: default; }
#overlap-explorer .oe-pager span { color: #888; font-size: 0.9em; }
</style>

<script>
(function () {
  var DATA_URL = "{{ '/assets/data/bootcamp-bnb-overlap.json' | relative_url }}";
  var PAGE_SIZE = 50;

  var state = { rows: [], strings: [], filtered: [], page: 0 };

  var els = {
    status: document.getElementById('oe-status'),
    table: document.getElementById('oe-table'),
    tbody: document.getElementById('oe-tbody'),
    search: document.getElementById('oe-search'),
    step: document.getElementById('oe-step'),
    minCount: document.getElementById('oe-min-count'),
    prev: document.getElementById('oe-prev'),
    next: document.getElementById('oe-next'),
    pageLabel: document.getElementById('oe-page-label'),
    statTotal: document.getElementById('oe-stat-total'),
    statShown: document.getElementById('oe-stat-shown'),
  };

  function s(i) { return state.strings[i]; }

  function rowText(r) {
    return [s(r[0]), s(r[1]), s(r[2]), s(r[3]), s(r[4]), s(r[5]), s(r[6])].join(' ').toLowerCase();
  }

  function applyFilters() {
    var q = els.search.value.trim().toLowerCase();
    var step = els.step.value;
    var minCount = parseInt(els.minCount.value, 10);

    state.filtered = state.rows.filter(function (r) {
      if (r[7] < minCount) return false;
      if (step && s(r[3]) !== step) return false;
      if (q && rowText(r).indexOf(q) === -1) return false;
      return true;
    });
    state.page = 0;
    render();
  }

  function render() {
    var start = state.page * PAGE_SIZE;
    var pageRows = state.filtered.slice(start, start + PAGE_SIZE);

    els.tbody.innerHTML = pageRows.map(function (r) {
      var bcSubj = s(r[0]), bcChap = s(r[1]), bcLesson = s(r[2]);
      var step = s(r[3]), nSubj = s(r[4]), nChap = s(r[5]), nLesson = s(r[6]);
      var count = r[7];
      return '<tr>' +
        '<td><span class="oe-lesson">' + escapeHtml(bcLesson) + '</span>' +
        '<span class="oe-path">' + escapeHtml(bcSubj) + ' / ' + escapeHtml(bcChap) + '</span></td>' +
        '<td><span class="oe-lesson">' + escapeHtml(nLesson) + '</span>' +
        '<span class="oe-path">' + escapeHtml(step) + ' / ' + escapeHtml(nSubj) + ' / ' + escapeHtml(nChap) + '</span></td>' +
        '<td class="oe-col-n">' + count + '</td>' +
        '</tr>';
    }).join('');

    var totalPages = Math.max(1, Math.ceil(state.filtered.length / PAGE_SIZE));
    els.pageLabel.textContent = 'Page ' + (state.page + 1) + ' of ' + totalPages;
    els.prev.disabled = state.page === 0;
    els.next.disabled = state.page >= totalPages - 1;
    els.statShown.textContent = state.filtered.length.toLocaleString();
  }

  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  els.search.addEventListener('input', applyFilters);
  els.step.addEventListener('change', applyFilters);
  els.minCount.addEventListener('change', applyFilters);
  els.prev.addEventListener('click', function () { if (state.page > 0) { state.page--; render(); } });
  els.next.addEventListener('click', function () {
    var totalPages = Math.ceil(state.filtered.length / PAGE_SIZE);
    if (state.page < totalPages - 1) { state.page++; render(); }
  });

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      state.strings = data.s;
      state.rows = data.r;
      state.filtered = state.rows;
      els.statTotal.textContent = state.rows.length.toLocaleString();
      els.status.hidden = true;
      els.table.hidden = false;
      render();
    })
    .catch(function (err) {
      els.status.textContent = 'Could not load overlap data (' + err.message + '). Check that bootcamp-bnb-overlap.json is in /assets/data/.';
    });
})();
</script>
