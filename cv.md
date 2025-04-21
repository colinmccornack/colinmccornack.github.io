---
layout: page
title: Curriculum Vitae
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
## Education
{: .cv-heading}

<div class="cv-two-column">
<div>
### University Name
{: .cv-item-title}
<div class="cv-date">2015-2019</div>
Degree in Computer Science
</div>

<div>
### Professional Certification
{: .cv-item-title}
<div class="cv-date">2020-2021</div>
Advanced Web Development
</div>
</div>
</section>

<section class="cv-section">
## Experience
{: .cv-heading}

<article>
### Senior Developer
{: .cv-item-title}
<div class="cv-date">2020-Present</div>
<ul>
<li>Led team of 5 developers</li>
<li>Implemented CI/CD pipeline</li>
</ul>
</article>
</section>

<section class="cv-section">
## Skills
{: .cv-heading}

<ul class="cv-skills">
<li>JavaScript</li>
<li>Python</li>
<li>Ruby</li>
<li>DevOps</li>
</ul>
</section>

</div>