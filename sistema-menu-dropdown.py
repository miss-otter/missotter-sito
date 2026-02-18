#!/usr/bin/env python3
"""
SISTEMA MENU DROPDOWN
Sostituisce l'header.html rotto con la versione corretta
"""

from pathlib import Path

HEADER_HTML = '''{{- $s := .Site.Params }}
<header class="header">
  <nav class="nav">
    <p class="logo">
      <a href="{{ site.Home.RelPermalink }}">
        {{- $logo := $s.Logo | default "icons/logo.png" }}
        {{- if fileExists (printf "assets/%s" $logo) }}
          {{- $img := resources.Get $logo }}
          {{- $imgWebp := $img.Resize "150x webp" }}
          <img
            decoding="async"
            loading="lazy"
            src="{{ $imgWebp.RelPermalink }}"
            alt="{{ site.Title }}"
            height="{{ $imgWebp.Height }}"
            width="{{ $imgWebp.Width }}"
          >
        {{- else }}
          <span class="logo__mark">{{ substr site.Title 0 1 }}</span>
          <span class="logo__text">{{ substr site.Title 1 }}</span>
        {{- end }}
      </a>
    </p>
    <div class="nav__list">
      <ul class="menu">
        {{- $currentPage := . }}
        {{- range site.Menus.main }}
          {{- if .HasChildren }}
          <li class="menu__item has_dropdown">
            <a class="menu__link{{ if $currentPage.HasMenuCurrent "main" . }} active{{ end }}" href="{{ .URL | absLangURL }}">
              {{ .Name }}
              <svg class="dropdown_icon" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </a>
            <ul class="dropdown_menu">
              {{- range .Children }}
              <li class="dropdown_item">
                <a class="dropdown_link{{ if $currentPage.IsMenuCurrent "main" . }} active{{ end }}" href="{{ .URL | absLangURL }}">
                  {{ .Name }}
                </a>
              </li>
              {{- end }}
            </ul>
          </li>
          {{- else }}
          <li class="menu__item">
            <a class="menu__link{{ if or ($currentPage.IsMenuCurrent "main" .) ($currentPage.HasMenuCurrent "main" .) }} active{{ end }}" href="{{ .URL | absLangURL }}">
              {{ .Name }}
            </a>
          </li>
          {{- end }}
        {{- end }}
      </ul>
    </div>
    {{- if not $s.enforceDarkMode }}
    <button id="mode" class="toggle" type="button" aria-label="{{ T "toggle_dark_mode" }}">
      <span class="toggle_inner">
        <span class="toggle_icon icon-moon"></span>
        <span class="toggle_icon icon-sun"></span>
      </span>
    </button>
    {{- end }}
    <button id="menu_toggle" class="toggle nav_toggle" type="button" aria-label="{{ T "toggle_menu" }}">
      <span class="toggle_inner">
        <span class="toggle_icon icon-menu"></span>
        <span class="toggle_icon icon-close"></span>
      </span>
    </button>
  </nav>
</header>
'''

CSS_DROPDOWN = '''
/* DROPDOWN MENU */
.menu__item.has_dropdown { position: relative; }
.dropdown_icon { margin-left: 4px; vertical-align: middle; transition: transform 0.2s; }
.menu__item.has_dropdown:hover .dropdown_icon { transform: rotate(180deg); }
.dropdown_menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 0.5rem 0;
  margin: 0;
  list-style: none;
  z-index: 1000;
}
.menu__item.has_dropdown:hover .dropdown_menu { display: block; }
.dropdown_item { margin: 0; padding: 0; }
.dropdown_link {
  display: block;
  padding: 0.5rem 1rem;
  color: var(--text);
  text-decoration: none;
  font-size: 0.9rem;
  white-space: nowrap;
}
.dropdown_link:hover { background: var(--theme); color: var(--light); }

/* IMMAGINI TRADUZIONI */
.content img[src*="edited"] {
  width: 200px;
  filter: sepia(100%) hue-rotate(70deg) saturate(60%);
  border-radius: 4px;
}

@media (max-width: 992px) {
  .dropdown_menu { position: static; box-shadow: none; border: none; padding-left: 1rem; background: transparent; }
}
'''

def main():
    print("=" * 60)
    print("SISTEMA MENU DROPDOWN")
    print("=" * 60)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    
    # Crea cartella layouts/partials se non esiste
    layouts_dir = script_dir / 'layouts' / 'partials'
    layouts_dir.mkdir(parents=True, exist_ok=True)
    
    # Scrivi header.html
    header_file = layouts_dir / 'header.html'
    
    # Backup se esiste
    if header_file.exists():
        backup = header_file.with_suffix('.html.bak')
        header_file.rename(backup)
        print(f"✓ Backup creato: {backup.name}")
    
    header_file.write_text(HEADER_HTML, encoding='utf-8')
    print(f"✓ Creato: layouts/partials/header.html")
    
    # Mostra CSS
    print()
    print("=" * 60)
    print("AGGIUNGI QUESTO CSS A static/css/custom.css:")
    print("=" * 60)
    print(CSS_DROPDOWN)
    print("=" * 60)
    
    print()
    print("Poi fai commit e push!")
    print()
    input("Premi INVIO per chiudere...")


if __name__ == '__main__':
    main()
