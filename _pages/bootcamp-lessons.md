---
layout: page
title: Bootcamp Lessons
permalink: /bootcamp-lessons/
---

<div id="bc-tree-explorer">
  <p class="bct-sub">Subject &rarr; chapter &rarr; lesson, with the number of Anki cards tagged to each.</p>

  <div class="bct-stats">
    <div class="bct-stat"><span class="bct-stat-label">Subjects</span><span class="bct-stat-value" id="bct-stat-subjects">–</span></div>
    <div class="bct-stat"><span class="bct-stat-label">Chapters</span><span class="bct-stat-value" id="bct-stat-chapters">–</span></div>
    <div class="bct-stat"><span class="bct-stat-label">Lessons</span><span class="bct-stat-value" id="bct-stat-lessons">–</span></div>
    <div class="bct-stat"><span class="bct-stat-label">Cards</span><span class="bct-stat-value" id="bct-stat-cards">–</span></div>
  </div>

  <div class="bct-controls">
    <input type="text" id="bct-search" placeholder="Filter by subject, chapter, or lesson…" autocomplete="off">
    <button id="bct-expand-all">Expand all</button>
    <button id="bct-collapse-all">Collapse all</button>
  </div>

  <div id="bct-status" class="bct-status">Loading…</div>
  <div id="bct-tree" hidden></div>
</div>

<style>
#bc-tree-explorer { max-width: 800px; margin: 0 auto; }
#bc-tree-explorer .bct-sub { color: #666; font-size: 0.95em; margin-bottom: 1.2em; }
#bc-tree-explorer .bct-stats { display: flex; gap: 12px; margin-bottom: 1.2em; flex-wrap: wrap; }
#bc-tree-explorer .bct-stat { background: #f6f6f6; border-radius: 6px; padding: 0.6em 1em; flex: 1; min-width: 90px; }
#bc-tree-explorer .bct-stat-label { display: block; font-size: 0.75em; color: #888; text-transform: uppercase; letter-spacing: 0.03em; }
#bc-tree-explorer .bct-stat-value { display: block; font-size: 1.3em; font-weight: 600; }
#bc-tree-explorer .bct-controls { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1em; }
#bc-tree-explorer #bct-search { flex: 1; min-width: 180px; padding: 0.5em 0.7em; border: 1px solid #ddd; border-radius: 6px; font-size: 0.95em; }
#bc-tree-explorer .bct-controls button { padding: 0.5em 0.9em; border: 1px solid #ddd; border-radius: 6px; background: #fff; font-size: 0.85em; cursor: pointer; }
#bc-tree-explorer .bct-controls button:hover { background: #f6f6f6; }
#bc-tree-explorer .bct-status { color: #888; padding: 1em 0; }

#bct-tree details.subject { border-bottom: 1px solid #eee; }
#bct-tree details.subject > summary { padding: 10px 4px; font-size: 15px; font-weight: 600; }
#bct-tree details.chapter > summary { padding: 7px 4px 7px 16px; font-size: 14px; border-left: 1px solid #eee; margin-left: 4px; }
#bct-tree summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; gap: 8px; }
#bct-tree summary::-webkit-details-marker { display: none; }
#bct-tree summary::before { content: "▸"; display: inline-block; margin-right: 8px; font-size: 11px; color: #999; transition: transform 0.15s ease; }
#bct-tree details[open] > summary::before { transform: rotate(90deg); }
#bct-tree .bct-count { color: #999; white-space: nowrap; font-variant-numeric: tabular-nums; font-size: 0.85em; }
#bct-tree ul.bct-lessons { list-style: none; margin: 0; padding: 0 0 6px 20px; }
#bct-tree li.bct-lesson { display: flex; justify-content: space-between; gap: 8px; padding: 5px 4px 5px 16px; border-left: 1px solid #eee; margin-left: 4px; font-size: 13px; color: #555; }
</style>

<script>
(function () {
  var DATA_URL = "{{ '/assets/data/bootcamp-lessons.json' | relative_url }}";
  var state = { strings: [], subjects: [] };

  var els = {
    status: document.getElementById('bct-status'),
    treeEl: document.getElementById('bct-tree'),
    search: document.getElementById('bct-search'),
    expandAll: document.getElementById('bct-expand-all'),
    collapseAll: document.getElementById('bct-collapse-all'),
    statSubjects: document.getElementById('bct-stat-subjects'),
    statChapters: document.getElementById('bct-stat-chapters'),
    statLessons: document.getElementById('bct-stat-lessons'),
    statCards: document.getElementById('bct-stat-cards'),
  };

  function s(i) { return state.strings[i]; }
  function esc(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function render() {
    var html = state.subjects.map(function (subjEntry) {
      var subjI = subjEntry[0], subjCount = subjEntry[1], chapters = subjEntry[2];
      var subjName = s(subjI);
      var chapHtml = chapters.map(function (chapEntry) {
        var chapI = chapEntry[0], chapTotal = chapEntry[1], lessons = chapEntry[2];
        var chapName = s(chapI);
        var lessonLis = lessons.map(function (le) {
          var lessonName = s(le[0]), cnt = le[1];
          var text = (lessonName + ' ' + chapName + ' ' + subjName).toLowerCase();
          return '<li class="bct-lesson" data-text="' + esc(text) + '"><span>' + esc(lessonName) + '</span><span class="bct-count">' + cnt + '</span></li>';
        }).join('');
        return '<details class="chapter"><summary><span>' + esc(chapName) + '</span>' +
          '<span class="bct-count">' + chapTotal + '</span></summary>' +
          '<ul class="bct-lessons">' + lessonLis + '</ul></details>';
      }).join('');
      return '<details class="subject"><summary><span>' + esc(subjName) + '</span>' +
        '<span class="bct-count">' + subjCount + '</span></summary><div>' + chapHtml + '</div></details>';
    }).join('');
    els.treeEl.innerHTML = html;
  }

  els.search.addEventListener('input', function () {
    var q = els.search.value.trim().toLowerCase();
    if (!q) {
      els.treeEl.querySelectorAll('li.bct-lesson').forEach(function (li) { li.style.display = 'flex'; });
      els.treeEl.querySelectorAll('details').forEach(function (d) { d.style.display = ''; d.open = false; });
      return;
    }
    els.treeEl.querySelectorAll('details.subject').forEach(function (subj) {
      var subjHasVisible = false;
      subj.querySelectorAll('details.chapter').forEach(function (chap) {
        var chapHasVisible = false;
        chap.querySelectorAll('li.bct-lesson').forEach(function (li) {
          var match = li.getAttribute('data-text').indexOf(q) !== -1;
          li.style.display = match ? 'flex' : 'none';
          if (match) chapHasVisible = true;
        });
        chap.style.display = chapHasVisible ? '' : 'none';
        chap.open = chapHasVisible;
        if (chapHasVisible) subjHasVisible = true;
      });
      subj.style.display = subjHasVisible ? '' : 'none';
      subj.open = subjHasVisible;
    });
  });

  els.expandAll.addEventListener('click', function () {
    els.treeEl.querySelectorAll('details').forEach(function (d) { d.open = true; });
  });
  els.collapseAll.addEventListener('click', function () {
    els.treeEl.querySelectorAll('details').forEach(function (d) { d.open = false; });
  });

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      state.strings = data.s;
      state.subjects = data.subjects;

      var chapterCount = 0, lessonCount = 0;
      state.subjects.forEach(function (subj) {
        subj[2].forEach(function (chap) {
          chapterCount++;
          lessonCount += chap[2].length;
        });
      });

      els.statSubjects.textContent = state.subjects.length;
      els.statChapters.textContent = chapterCount.toLocaleString();
      els.statLessons.textContent = lessonCount.toLocaleString();
      els.statCards.textContent = data.total_cards.toLocaleString();

      els.status.hidden = true;
      els.treeEl.hidden = false;
      render();
    })
    .catch(function (err) {
      els.status.textContent = 'Could not load lesson data (' + err.message + '). Check that bootcamp-lessons.json is in /assets/data/.';
    });
})();
</script>
