---
layout: page
title: Boards &amp; Beyond Lessons
permalink: /bnb-lessons/
---

<div id="bnbt-explorer">
  <p class="bnbt-sub">Step &rarr; subject &rarr; chapter &rarr; lesson, with the number of Anki cards tagged to each.</p>

  <div class="bnbt-stats">
    <div class="bnbt-stat"><span class="bnbt-stat-label">Steps</span><span class="bnbt-stat-value" id="bnbt-stat-steps">–</span></div>
    <div class="bnbt-stat"><span class="bnbt-stat-label">Subjects</span><span class="bnbt-stat-value" id="bnbt-stat-subjects">–</span></div>
    <div class="bnbt-stat"><span class="bnbt-stat-label">Chapters</span><span class="bnbt-stat-value" id="bnbt-stat-chapters">–</span></div>
    <div class="bnbt-stat"><span class="bnbt-stat-label">Lessons</span><span class="bnbt-stat-value" id="bnbt-stat-lessons">–</span></div>
    <div class="bnbt-stat"><span class="bnbt-stat-label">Cards</span><span class="bnbt-stat-value" id="bnbt-stat-cards">–</span></div>
  </div>

  <div class="bnbt-controls">
    <input type="text" id="bnbt-search" placeholder="Filter by step, subject, chapter, or lesson…" autocomplete="off">
    <button id="bnbt-expand-all">Expand all</button>
    <button id="bnbt-collapse-all">Collapse all</button>
  </div>

  <div id="bnbt-status" class="bnbt-status">Loading…</div>
  <div id="bnbt-tree" hidden></div>
</div>

<style>
#bnbt-explorer { max-width: 800px; margin: 0 auto; }
#bnbt-explorer .bnbt-sub { color: #666; font-size: 0.95em; margin-bottom: 1.2em; }
#bnbt-explorer .bnbt-stats { display: flex; gap: 12px; margin-bottom: 1.2em; flex-wrap: wrap; }
#bnbt-explorer .bnbt-stat { background: #f6f6f6; border-radius: 6px; padding: 0.6em 1em; flex: 1; min-width: 80px; }
#bnbt-explorer .bnbt-stat-label { display: block; font-size: 0.75em; color: #888; text-transform: uppercase; letter-spacing: 0.03em; }
#bnbt-explorer .bnbt-stat-value { display: block; font-size: 1.3em; font-weight: 600; }
#bnbt-explorer .bnbt-controls { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1em; }
#bnbt-explorer #bnbt-search { flex: 1; min-width: 180px; padding: 0.5em 0.7em; border: 1px solid #ddd; border-radius: 6px; font-size: 0.95em; }
#bnbt-explorer .bnbt-controls button { padding: 0.5em 0.9em; border: 1px solid #ddd; border-radius: 6px; background: #fff; font-size: 0.85em; cursor: pointer; }
#bnbt-explorer .bnbt-controls button:hover { background: #f6f6f6; }
#bnbt-explorer .bnbt-status { color: #888; padding: 1em 0; }

#bnbt-tree details.step { background: #f6f6f6; border-radius: 8px; margin-bottom: 12px; overflow: hidden; }
#bnbt-tree details.step > summary { padding: 12px 14px; font-size: 16px; font-weight: 700; }
#bnbt-tree details.step > div { padding: 0 10px 8px; }
#bnbt-tree details.subject { border-bottom: 1px solid #eee; }
#bnbt-tree details.subject:last-child { border-bottom: none; }
#bnbt-tree details.subject > summary { padding: 10px 4px; font-size: 15px; font-weight: 600; }
#bnbt-tree details.chapter > summary { padding: 7px 4px 7px 16px; font-size: 14px; border-left: 1px solid #ddd; margin-left: 4px; }
#bnbt-tree summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; gap: 8px; }
#bnbt-tree summary::-webkit-details-marker { display: none; }
#bnbt-tree summary::before { content: "▸"; display: inline-block; margin-right: 8px; font-size: 11px; color: #999; transition: transform 0.15s ease; }
#bnbt-tree details[open] > summary::before { transform: rotate(90deg); }
#bnbt-tree .bnbt-count { color: #999; white-space: nowrap; font-variant-numeric: tabular-nums; font-size: 0.85em; }
#bnbt-tree ul.bnbt-lessons { list-style: none; margin: 0; padding: 0 0 6px 20px; }
#bnbt-tree li.bnbt-lesson { display: flex; justify-content: space-between; gap: 8px; padding: 5px 4px 5px 16px; border-left: 1px solid #ddd; margin-left: 4px; font-size: 13px; color: #555; }
</style>

<script>
(function () {
  var DATA_URL = "{{ '/assets/data/bnb-lessons.json' | relative_url }}";
  var state = { strings: [], steps: [] };

  var els = {
    status: document.getElementById('bnbt-status'),
    treeEl: document.getElementById('bnbt-tree'),
    search: document.getElementById('bnbt-search'),
    expandAll: document.getElementById('bnbt-expand-all'),
    collapseAll: document.getElementById('bnbt-collapse-all'),
    statSteps: document.getElementById('bnbt-stat-steps'),
    statSubjects: document.getElementById('bnbt-stat-subjects'),
    statChapters: document.getElementById('bnbt-stat-chapters'),
    statLessons: document.getElementById('bnbt-stat-lessons'),
    statCards: document.getElementById('bnbt-stat-cards'),
  };

  function s(i) { return state.strings[i]; }
  function esc(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function render() {
    var html = state.steps.map(function (stepEntry) {
      var stepI = stepEntry[0], stepCount = stepEntry[1], subjects = stepEntry[2];
      var stepName = s(stepI);
      var subjHtml = subjects.map(function (subjEntry) {
        var subjI = subjEntry[0], subjCount = subjEntry[1], chapters = subjEntry[2];
        var subjName = s(subjI);
        var chapHtml = chapters.map(function (chapEntry) {
          var chapI = chapEntry[0], chapTotal = chapEntry[1], lessons = chapEntry[2];
          var chapName = s(chapI);
          var lessonLis = lessons.map(function (le) {
            var lessonName = s(le[0]), cnt = le[1];
            var text = (lessonName + ' ' + chapName + ' ' + subjName + ' ' + stepName).toLowerCase();
            return '<li class="bnbt-lesson" data-text="' + esc(text) + '"><span>' + esc(lessonName) + '</span><span class="bnbt-count">' + cnt + '</span></li>';
          }).join('');
          return '<details class="chapter"><summary><span>' + esc(chapName) + '</span>' +
            '<span class="bnbt-count">' + chapTotal + '</span></summary>' +
            '<ul class="bnbt-lessons">' + lessonLis + '</ul></details>';
        }).join('');
        return '<details class="subject"><summary><span>' + esc(subjName) + '</span>' +
          '<span class="bnbt-count">' + subjCount + '</span></summary><div>' + chapHtml + '</div></details>';
      }).join('');
      return '<details class="step" open><summary><span>' + esc(stepName) + '</span>' +
        '<span class="bnbt-count">' + stepCount + '</span></summary><div>' + subjHtml + '</div></details>';
    }).join('');
    els.treeEl.innerHTML = html;
  }

  els.search.addEventListener('input', function () {
    var q = els.search.value.trim().toLowerCase();
    if (!q) {
      els.treeEl.querySelectorAll('li.bnbt-lesson').forEach(function (li) { li.style.display = 'flex'; });
      els.treeEl.querySelectorAll('details.subject, details.chapter').forEach(function (d) { d.style.display = ''; d.open = false; });
      els.treeEl.querySelectorAll('details.step').forEach(function (d) { d.style.display = ''; d.open = true; });
      return;
    }
    els.treeEl.querySelectorAll('details.step').forEach(function (step) {
      var stepHasVisible = false;
      step.querySelectorAll('details.subject').forEach(function (subj) {
        var subjHasVisible = false;
        subj.querySelectorAll('details.chapter').forEach(function (chap) {
          var chapHasVisible = false;
          chap.querySelectorAll('li.bnbt-lesson').forEach(function (li) {
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
        if (subjHasVisible) stepHasVisible = true;
      });
      step.style.display = stepHasVisible ? '' : 'none';
      step.open = stepHasVisible;
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
      state.steps = data.steps;

      var subjectCount = 0, chapterCount = 0, lessonCount = 0, cardCount = 0;
      state.steps.forEach(function (step) {
        cardCount += step[1];
        step[2].forEach(function (subj) {
          subjectCount++;
          subj[2].forEach(function (chap) {
            chapterCount++;
            lessonCount += chap[2].length;
          });
        });
      });

      els.statSteps.textContent = state.steps.length;
      els.statSubjects.textContent = subjectCount.toLocaleString();
      els.statChapters.textContent = chapterCount.toLocaleString();
      els.statLessons.textContent = lessonCount.toLocaleString();
      els.statCards.textContent = cardCount.toLocaleString();

      els.status.hidden = true;
      els.treeEl.hidden = false;
      render();
    })
    .catch(function (err) {
      els.status.textContent = 'Could not load lesson data (' + err.message + '). Check that bnb-lessons.json is in /assets/data/.';
    });
})();
</script>
