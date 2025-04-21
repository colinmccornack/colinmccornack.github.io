---
layout: page
title: Test Curriculum Vitae
permalink: /cv/
---
<style>
/* CV-specific styles */
.cv-container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2rem;
}

.cv-section {
  margin-bottom: 2rem;
}

.cv-two-column {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.cv-date {
  color: var(--text-light);
  font-size: 0.9em;
}

.cv-skills {
  columns: 2;
  list-style: none;
  padding: 0;
}

@media (max-width: 768px) {
  .cv-two-column { grid-template-columns: 1fr; }
  .cv-skills { columns: 1; }
}
</style>

<div class="cv-container">
  <section class="cv-section">
    <h2>Education</h2>
    <div class="cv-two-column">
      <div>
        <h3>Michigan State University</h3>
        <div class="cv-date">2014-2019</div>
        <p>Bachelor of Arts - Music</p>
        <p>Bachelor of Science - Biochemistry and Molecular Biology<p>
      <div>
        <h3>Washington University School of Medicine</h3>
        <div class="cv-date">2019-Present</div>
        <p>Medical Scientist Training Program</p>
    </div>
  </section>

  <section class="cv-section">
    <h2>Experience</h2>
    <article>
      <h3>Senior Developer</h3>
      <div class="cv-date">2020-Present</div>
      <ul>
        <li>Led team of 5 developers</li>
        <li>Implemented CI/CD pipeline</li>
      </ul>
    </article>
  </section>

  <section class="cv-section">
    <h2>Skills</h2>
    <ul class="cv-skills">
      <li>JavaScript</li>
      <li>Python</li>
      <li>Ruby</li>
      <li>DevOps</li>
    </ul>
  </section>
</div>