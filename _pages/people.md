---
layout: archive
title: "People & Collaborations"
permalink: /people/
author_profile: true
---

{% include base_path %}

<style>
  .people-intro {
    margin-bottom: 1.4em;
    font-size: 0.95em;
    line-height: 1.55;
  }
  .people-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(265px, 1fr));
    gap: 0.9em;
    margin: 0.8em 0 1.8em 0;
  }
  .person-card {
    padding: 0.95em 1.1em;
    border: 1px solid var(--global-border-color, #e0e0e0);
    border-left: 4px solid var(--global-link-color, #2b6cb0);
    border-radius: 6px;
    background: var(--global-toc-bg-color, rgba(0, 0, 0, 0.02));
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .person-name {
    font-weight: 700;
    font-size: 1em;
    margin: 0 0 0.2em 0;
  }
  .person-role {
    display: inline-block;
    font-size: 0.75em;
    font-weight: 600;
    padding: 0.12em 0.55em;
    border-radius: 999px;
    background: rgba(43, 108, 176, 0.12);
    color: var(--global-link-color, #2b6cb0);
    margin-bottom: 0.45em;
  }
  .person-affil {
    font-size: 0.85em;
    opacity: 0.9;
    margin-bottom: 0.65em;
    line-height: 1.35;
  }
  .person-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45em;
    margin-top: auto;
  }
  .person-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.3em;
    padding: 0.18em 0.55em;
    font-size: 0.76em;
    border-radius: 4px;
    border: 1px solid var(--global-border-color, #ccc);
    background: var(--global-bg-color, #fff);
    color: var(--global-text-color, #333) !important;
    text-decoration: none !important;
  }
  .person-btn:hover {
    border-color: var(--global-link-color, #2b6cb0);
    color: var(--global-link-color, #2b6cb0) !important;
  }
  .student-card {
    padding: 1em 1.15em;
    border: 1px solid var(--global-border-color, #e0e0e0);
    border-top: 3px solid var(--global-link-color, #2b6cb0);
    border-radius: 6px;
    background: var(--global-toc-bg-color, rgba(0, 0, 0, 0.02));
  }
  .student-thesis {
    font-size: 0.86em;
    font-style: italic;
    margin: 0.35em 0;
    line-height: 1.4;
  }
  .country-heading {
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    font-size: 1.1em;
  }
</style>

<p class="people-intro">
  My research in robust control, sampled-data systems, and power electronics is carried out in active collaboration with researchers across <strong>Chile</strong>, <strong>Brazil</strong>, and the <strong>United Kingdom</strong>, alongside co-supervising undergraduate engineering theses.
</p>

Thesis Supervision
======
<div class="people-grid">
  <div class="student-card">
    <div class="person-name">Emilia Leyton Figueroa</div>
    <div><span class="person-role">B.S. Thesis Co-Supervision (2024)</span></div>
    <div class="person-affil">Mechatronics Engineering — University of Talca, Chile</div>
    <div class="student-thesis">"Análisis del Desempeño de un Controlador Estático de Realimentación de Salida Robusto para Convertidores Buck-Boost"</div>
    <div style="font-size: 0.8em; opacity: 0.85;">Co-advised with Prof. Jonathan M. Palma</div>
  </div>

  <div class="student-card">
    <div class="person-name">Jeremy Rojas</div>
    <div><span class="person-role">B.S. Thesis Co-Supervision (2023)</span></div>
    <div class="person-affil">Mechatronics Engineering — University of Talca, Chile</div>
    <div class="student-thesis">"Control LMI para canal de agua"</div>
    <div style="font-size: 0.8em; opacity: 0.85;">Co-advised with Prof. Jonathan M. Palma</div>
  </div>
</div>

International Research Network
======

<h3 class="country-heading">🇨🇱 Chile</h3>
<div class="people-grid">
  <div class="person-card">
    <div>
      <div class="person-name">Dr. Jonathan M. Palma</div>
      <span class="person-role">M.S. &amp; Ph.D. Advisor</span>
      <div class="person-affil">University of Talca, Curicó, Chile<br><small>Laboratory of Automated Systems</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0002-3924-1907" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Palma" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">Dr. Carlos R. Baier</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">University of Talca, Curicó, Chile<br><small>Power Electronics &amp; Energy Conversion</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0002-1752-1625" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Baier" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">M.Sc. Esteban I. Marciel</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">University of Talca, Curicó, Chile<br><small>Power Converters &amp; Microgrids</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0002-7641-0319" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Marciel" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">Dr. Alejandro J. Rojas</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">University of Concepción (UdeC), Concepción, Chile<br><small>Networked &amp; Robust Control</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0002-3867-6909" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
    </div>
  </div>
</div>

<h3 class="country-heading">🇬🇧 United Kingdom</h3>
<div class="people-grid">
  <div class="person-card">
    <div>
      <div class="person-name">Dr. Márcio J. Lacerda</div>
      <span class="person-role">M.S. &amp; Ph.D. Co-Advisor</span>
      <div class="person-affil">London Metropolitan University, London, UK<br><small>Reader in Control Engineering &amp; CPS</small></div>
    </div>
    <div class="person-links">
      <a href="https://lacerdamj.github.io/" target="_blank" rel="noopener" class="person-btn"><i class="fas fa-globe"></i> Website</a>
      <a href="{{ base_path }}/publications/?q=Lacerda" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">Dr. Marco Rivera</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">University of Nottingham, UK<br><small>Power Electronics, Machines &amp; Control</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0002-4353-2088" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Rivera" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>
</div>

<h3 class="country-heading">🇧🇷 Brazil</h3>
<div class="people-grid">
  <div class="person-card">
    <div>
      <div class="person-name">Dr. Ricardo C. L. F. Oliveira</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">University of Campinas (UNICAMP), SP, Brazil<br><small>School of Electrical &amp; Computer Engineering</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0002-8225-7058" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Oliveira" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">Dr. Cecilia F. Morais</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">University of Campinas (UNICAMP), SP, Brazil<br><small>School of Electrical &amp; Computer Engineering</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0002-9994-0339" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Morais" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">Dr. Gabriela W. Gabriel</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">Aeronautics Institute of Technology (ITA), SP, Brazil<br><small>Sampled-Data &amp; Hybrid Control Systems</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0001-5631-9270" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Gabriel" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">Dr. André M. de Oliveira</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">Federal University of São Paulo (UNIFESP), Brazil<br><small>Institute of Science and Technology</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0003-4351-3896" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=de+Oliveira" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">Dr. João M. Gomes da Silva Jr.</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">Federal University of Rio Grande do Sul (UFRGS), Brazil<br><small>Department of Electrical Systems &amp; Control</small></div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0000-0001-9528-6969" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
      <a href="{{ base_path }}/publications/?q=Gomes+da+Silva" class="person-btn"><i class="fas fa-book-open"></i> Joint Papers</a>
    </div>
  </div>

  <div class="person-card">
    <div>
      <div class="person-name">M.Sc. Marcelo Aravena</div>
      <span class="person-role">Research Collaborator</span>
      <div class="person-affil">University of Campinas (UNICAMP), SP, Brazil</div>
    </div>
    <div class="person-links">
      <a href="https://orcid.org/0009-0003-1766-4452" target="_blank" rel="noopener" class="person-btn"><i class="ai ai-orcid"></i> ORCID</a>
    </div>
  </div>
</div>

