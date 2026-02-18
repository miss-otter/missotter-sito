#!/usr/bin/env python3
"""
INSTALLA NUOVE FUNZIONALITÀ
- Menu dropdown per Biblioteca
- Import automatico Substack
- Configurazione multilingua
"""

from pathlib import Path
import shutil

def main():
    print("=" * 60)
    print("INSTALLA NUOVE FUNZIONALITÀ")
    print("=" * 60)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    
    # Verifica che siamo nella cartella giusta
    hugo_toml = script_dir / 'hugo.toml'
    if not hugo_toml.exists():
        print("ERRORE: hugo.toml non trovato!")
        print("Assicurati di eseguire questo script dalla cartella del sito.")
        input("\nPremi INVIO per chiudere...")
        return
    
    changes = []
    
    # 1. CREA CARTELLA layouts/partials
    print("1. Creo struttura per override template...")
    layouts_dir = script_dir / 'layouts' / 'partials'
    layouts_dir.mkdir(parents=True, exist_ok=True)
    changes.append("layouts/partials/ creata")
    
    # 2. CREA HEADER.HTML PER DROPDOWN
    header_content = '''{{- $defined := false }}
{{- $defined := $.Site.Params.enforceDarkMode }}
<header class="header">
  <nav class="nav" id="nav">
    <p class="logo">
      {{- $customLogo := ($.Site.Params.Logo | default "icons/logo.png") }}
      <a href="{{ absLangURL `` }}">
        {{- if fileExists (print "assets/" $customLogo) }}
        {{- $img := resources.Get $customLogo }}
        {{- $imgWebp := $img.Resize "150x webp" }}
        <img 
          decoding="async"
          src="{{ $imgWebp.RelPermalink }}"
          width="{{ $imgWebp.Width }}"
          height="{{ $imgWebp.Height }}"
          alt="{{ $.Site.Title }}"
        >
        {{- else }}
        <span class="logo_text">{{ $.Site.Title }}</span>
        {{- end }}
      </a>
    </p>
    <ul class="menu" id="menu">
      {{- $currentPage := . }}
      {{- range .Site.Menus.main }}
        {{- if .HasChildren }}
        <li class="menu_item has-children">
          <a href="{{ .URL | absLangURL }}" class="menu_link">
            {{ .Name }}
            <svg class="dropdown-icon" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </a>
          <ul class="submenu">
            {{- range .Children }}
            <li class="submenu_item">
              <a href="{{ .URL | absLangURL }}" class="submenu_link{{ if $currentPage.IsMenuCurrent `main` . }} active{{ end }}">
                {{ .Name }}
              </a>
            </li>
            {{- end }}
          </ul>
        </li>
        {{- else }}
        <li class="menu_item">
          <a href="{{ .URL | absLangURL }}" class="{{ if or ($currentPage.IsMenuCurrent `main` .) ($currentPage.HasMenuCurrent `main` .) }}active{{ end }} menu_link">
            {{ .Name }}
          </a>
        </li>
        {{- end }}
      {{- end }}
    </ul>
    {{- if not $defined }}
    <button id="mode" class="mode" type="button" aria-label="toggle dark/light mode">
      <span class="icon lit">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
      </span>
      <span class="icon dim">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      </span>
    </button>
    {{- end }}
    <button id="menu_toggle" class="menu_toggle" type="button" aria-label="toggle menu">
      <span class="icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </span>
    </button>
  </nav>
</header>
'''
    
    header_file = layouts_dir / 'header.html'
    header_file.write_text(header_content, encoding='utf-8')
    changes.append("layouts/partials/header.html creato")
    print("   ✓ Header con dropdown creato")
    
    # 3. CREA WORKFLOW GITHUB ACTIONS
    print("\n2. Creo workflow GitHub Actions per Substack...")
    workflows_dir = script_dir / '.github' / 'workflows'
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = '''name: Import Substack

on:
  schedule:
    - cron: '0 8 * * *'
  workflow_dispatch:

jobs:
  import:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install feedparser requests python-dateutil
      
      - name: Run import script
        run: python scripts/import-substack.py
      
      - name: Check for changes
        id: check
        run: |
          if [[ -n $(git status --porcelain) ]]; then
            echo "changes=true" >> $GITHUB_OUTPUT
          else
            echo "changes=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Commit and push
        if: steps.check.outputs.changes == 'true'
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add -A
          git commit -m "Import nuovi post da Substack [auto]"
          git push
'''
    
    workflow_file = workflows_dir / 'import-substack.yml'
    workflow_file.write_text(workflow_content, encoding='utf-8')
    changes.append(".github/workflows/import-substack.yml creato")
    print("   ✓ Workflow creato")
    
    # 4. CREA SCRIPT IMPORT SUBSTACK
    print("\n3. Creo script import Substack...")
    scripts_dir = script_dir / 'scripts'
    scripts_dir.mkdir(parents=True, exist_ok=True)
    
    import_script = '''#!/usr/bin/env python3
"""
IMPORT SUBSTACK → HUGO

NOTA: Substack mette nel feed RSS solo gli Articles (articoli lunghi).
I Notes (post brevi tipo social) NON hanno RSS, quindi non vengono importati.
Per i Notes, aggiungili manualmente nella sezione Breadcrumbs.
"""

import feedparser
import re
import os
from pathlib import Path
from datetime import datetime
import hashlib
import html

SUBSTACK_RSS = "https://smallbreadcrumbs.substack.com/feed"
CONTENT_DIR = Path("content/breadcrumbs")
IMPORTED_FILE = Path("scripts/.imported-substack.txt")

def get_imported_ids():
    if IMPORTED_FILE.exists():
        return set(IMPORTED_FILE.read_text().strip().split('\\n'))
    return set()

def save_imported_id(post_id):
    IMPORTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(IMPORTED_FILE, 'a') as f:
        f.write(f"{post_id}\\n")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[^a-z0-9\\s-]', '', text)
    text = re.sub(r'[\\s_]+', '-', text)
    return text.strip('-')

def html_to_markdown(content):
    content = re.sub(r'<p[^>]*>', '\\n\\n', content)
    content = re.sub(r'</p>', '', content)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\\n\\n## \\1\\n\\n', content, flags=re.DOTALL)
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\\1*', content, flags=re.DOTALL)
    content = re.sub(r'<a[^>]*href=["\\'](.*?)["\\'][^>]*>(.*?)</a>', r'[\\2](\\1)', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', '', content)
    content = html.unescape(content)
    return content.strip()

def main():
    print("Import Substack...")
    print("(Solo Articles - i Notes vanno aggiunti manualmente)")
    feed = feedparser.parse(SUBSTACK_RSS)
    imported = get_imported_ids()
    
    new_count = 0
    for entry in feed.entries:
        post_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
        if post_id in imported:
            continue
        
        slug = slugify(entry.title)
        date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
        content_html = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
        
        post_dir = CONTENT_DIR / slug
        post_dir.mkdir(parents=True, exist_ok=True)
        
        content = f"""---
title: "{entry.title.replace('"', '\\\\"')}"
date: {date.strftime('%Y-%m-%dT%H:%M:%S+01:00')}
source: "substack"
original_url: "{entry.link}"
---

{html_to_markdown(content_html)}
"""
        (post_dir / "index.md").write_text(content, encoding='utf-8')
        save_imported_id(post_id)
        print(f"  Importato: {entry.title[:50]}...")
        new_count += 1
    
    print(f"Completato! {new_count} nuovi articoli.")

if __name__ == '__main__':
    main()
'''
    
    import_file = scripts_dir / 'import-substack.py'
    import_file.write_text(import_script, encoding='utf-8')
    changes.append("scripts/import-substack.py creato")
    print("   ✓ Script import creato")
    
    # 5. AGGIORNA HUGO.TOML
    print("\n4. Aggiorno hugo.toml con menu dropdown e multilingua...")
    
    new_config = '''baseURL = '/'
defaultContentLanguage = 'it'
defaultContentLanguageInSubdir = false
title = 'Miss Otter'
theme = 'clarity'

disableKinds = ["taxonomy", "term"]

[taxonomies]

[languages]
  [languages.it]
    languageName = "Italiano"
    weight = 1
    title = "Miss Otter"
    
  [languages.en]
    languageName = "English"
    weight = 2
    title = "Miss Otter"

[params]
  author = 'Miss Otter'
  description = 'Un viaggio nella narrazione del reale'
  mainSections = ['breadcrumbs', 'biblioteca', 'traduzioni']
  customCSS = ["css/custom.css"]
  showShare = false
  numberOfTagsShown = 0
  usePageBundles = true
  since = 2020

[params.social]
  twitter = ""
  github = ""

[menu]
  [[menu.main]]
    identifier = "home"
    name = "Miss Otter"
    url = "/"
    weight = 1
    
  [[menu.main]]
    identifier = "breadcrumbs"
    name = "Breadcrumbs"
    url = "/breadcrumbs/"
    weight = 2
    
  [[menu.main]]
    identifier = "traduzioni"
    name = "Traduzioni"
    url = "/traduzioni/"
    weight = 3
    
  [[menu.main]]
    identifier = "biblioteca"
    name = "La biblioteca"
    url = "/biblioteca/"
    weight = 4
    
  [[menu.main]]
    identifier = "nuoviarrivi"
    name = "Nuovi Arrivi"
    url = "/biblioteca/nuoviarrivi/"
    parent = "biblioteca"
    weight = 1
    
  [[menu.main]]
    identifier = "vecchieglorie"
    name = "Vecchie Glorie"
    url = "/biblioteca/vecchieglorie/"
    parent = "biblioteca"
    weight = 2
    
  [[menu.main]]
    identifier = "fiordafiore"
    name = "Fior da Fiore"
    url = "/biblioteca/fiordafiore/"
    parent = "biblioteca"
    weight = 3
    
  [[menu.main]]
    identifier = "oldies"
    name = "Oldies"
    url = "/biblioteca/oldies/"
    parent = "biblioteca"
    weight = 4
    
  [[menu.main]]
    identifier = "chi-sono"
    name = "Chi sono"
    url = "/chi-sono/"
    weight = 5

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
'''
    
    # Backup
    shutil.copy(hugo_toml, script_dir / 'hugo.toml.backup')
    hugo_toml.write_text(new_config, encoding='utf-8')
    changes.append("hugo.toml aggiornato (backup in hugo.toml.backup)")
    print("   ✓ hugo.toml aggiornato")
    
    # 6. MOSTRA CSS DA AGGIUNGERE
    print("\n5. CSS da aggiungere a static/css/custom.css:")
    print("-" * 60)
    
    css_to_add = '''
/* MENU DROPDOWN */
.menu_item.has-children { position: relative; }
.dropdown-icon { margin-left: 4px; transition: transform 0.2s; }
.menu_item.has-children:hover .dropdown-icon { transform: rotate(180deg); }
.submenu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  background: var(--bg, #fff);
  border: 1px solid var(--border, #ddd);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 8px 0;
  z-index: 1000;
  list-style: none;
}
.menu_item.has-children:hover .submenu { display: block; }
.submenu_link {
  display: block;
  padding: 8px 16px;
  color: var(--text, #333);
  text-decoration: none;
}
.submenu_link:hover {
  background: var(--accent-color, #556b58);
  color: #fff;
}

/* IMMAGINI TRADUZIONI */
.content img[src*="edited"] {
  width: 200px;
  filter: sepia(100%) hue-rotate(70deg) saturate(60%);
  border-radius: 4px;
}
'''
    
    print(css_to_add)
    print("-" * 60)
    print("\nCopia e incolla questo CSS in static/css/custom.css")
    
    # Riepilogo
    print()
    print("=" * 60)
    print("COMPLETATO!")
    print("=" * 60)
    print("\nModifiche effettuate:")
    for c in changes:
        print(f"  ✓ {c}")
    
    print("\n⚠️  AZIONE MANUALE RICHIESTA:")
    print("   Aggiungi il CSS mostrato sopra a static/css/custom.css")
    print()
    print("Poi fai commit e push con GitHub Desktop")
    print("=" * 60)
    input("\nPremi INVIO per chiudere...")


if __name__ == '__main__':
    main()
