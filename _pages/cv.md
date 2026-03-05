---
layout: archive
title: "Curriculum Vitae"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<div style="text-align: right; margin-bottom: 2em;">
  <a href="{{ base_path }}/cv-export/" target="_blank" class="btn btn--primary btn--large"><i class="fas fa-file-pdf"></i> Download CV (PDF)</a>
</div>

Education
======
{% include education.md %}

Work experience
======
{% include work_experience.md %}
  
Research Interests
======
{% include skills.md %}

Publications
======
{% if site.publication_category %}
{% for category in site.publication_category %}
{% assign cat_pubs = site.publications | where: "category", category[0] %}
{% if cat_pubs.size > 0 %}
<h3 style="margin-top: 1em; margin-bottom: 0.5em;">{{ category[1].title }}</h3>
<ol reversed start="{{ cat_pubs.size }}" style="margin-top: 0;">
{% for post in cat_pubs reversed %}
{% include archive-single-cv.html %}
{% endfor %}
</ol>
{% endif %}
{% endfor %}
{% else %}
<ol reversed start="{{ site.publications.size }}">
{% for post in site.publications reversed %}
{% include archive-single-cv.html %}
{% endfor %}
</ol>
{% endif %}
  
Collaborators
======
{% include collaborators.md %}

Personal References
======
{% include references.md %}
