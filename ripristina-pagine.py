#!/usr/bin/env python3
"""
RIPRISTINA PAGINE WORDPRESS IN HUGO
Estrae il contenuto delle pagine dall'XML e crea i file _index.md corretti
"""

import xml.etree.ElementTree as ET
import re
import html
from pathlib import Path

def clean_wordpress_content(content):
    """Converte contenuto WordPress/HTML in Markdown pulito"""
    if not content:
        return ""
    
    text = content
    
    # Rimuovi commenti WordPress (<!-- wp:xxx -->)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    # Converti heading HTML
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Converti paragrafi
    text = re.sub(r'<p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
    
    # Converti line break
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # Converti bold/strong
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Converti italic/em
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Converti link
    def convert_link(match):
        href = match.group(1)
        text_content = match.group(2)
        # Rimuovi tag interni
        text_content = re.sub(r'<[^>]+>', '', text_content)
        return f'[{text_content}]({href})'
    
    text = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', convert_link, text, flags=re.DOTALL|re.IGNORECASE)
    
    # Converti immagini - estrai URL e converti a nome file locale
    def convert_image(match):
        src = match.group(1)
        alt = match.group(2) if match.group(2) else ''
        # Estrai nome file da URL WordPress
        if 'missotter.wordpress.com' in src:
            filename = src.split('/')[-1].split('?')[0]
            return f'![{alt}]({filename})'
        return f'![{alt}]({src})'
    
    text = re.sub(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', convert_image, text, flags=re.IGNORECASE)
    text = re.sub(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*/?>', r'![](\1)', text, flags=re.IGNORECASE)
    
    # Converti figure (WordPress)
    text = re.sub(r'<figure[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</figure>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<figcaption[^>]*>(.*?)</figcaption>', r'*\1*', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Converti liste
    text = re.sub(r'<ul[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</ul>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<ol[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</ol>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<li[^>]*>', '- ', text, flags=re.IGNORECASE)
    text = re.sub(r'</li>', '\n', text, flags=re.IGNORECASE)
    
    # Rimuovi div, span e altri contenitori
    text = re.sub(r'<div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</div>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<span[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</span>', '', text, flags=re.IGNORECASE)
    
    # Rimuovi qualsiasi tag HTML residuo
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decodifica entità HTML
    text = html.unescape(text)
    
    # Pulisci spazi multipli e righe vuote eccessive
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = text.strip()
    
    # Sistema URL immagini WordPress rimaste (sia completi che relativi)
    def fix_image_url(match):
        alt = match.group(1)
        url = match.group(2)
        # URL completo WordPress
        if 'missotter.wordpress.com' in url:
            filename = url.split('/')[-1].split('?')[0]
            return f'![{alt}]({filename})'
        # Path relativo /wp-content/uploads/...
        if '/wp-content/uploads/' in url:
            filename = url.split('/')[-1].split('?')[0]
            return f'![{alt}]({filename})'
        return f'![{alt}]({url})'
    
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_url, text)
    
    # Sistema anche i link che contengono solo path immagine (senza !)
    def fix_link_to_image(match):
        text_content = match.group(1)
        url = match.group(2)
        # Se è un link a un'immagine WordPress
        if '/wp-content/uploads/' in url and any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            filename = url.split('/')[-1].split('?')[0]
            # Converti in immagine Markdown
            return f'![]({filename})'
        return f'[{text_content}]({url})'
    
    text = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', fix_link_to_image, text)
    
    # Converti link interni WordPress in link relativi
    text = re.sub(r'https?://missotter\.wordpress\.com/?', '/', text)
    
    return text


def create_frontmatter(title, description=''):
    """Crea il frontmatter YAML per Hugo"""
    fm = f'---\ntitle: "{title}"\n'
    if description:
        fm += f'description: "{description}"\n'
    fm += '---\n\n'
    return fm


def main():
    print("=" * 70)
    print("RIPRISTINA PAGINE WORDPRESS IN HUGO")
    print("=" * 70)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    
    # Cerca il file XML
    xml_file = None
    for f in script_dir.glob('*.xml'):
        xml_file = f
        break
    
    if not xml_file:
        # Prova nella cartella uploads o parent
        for search_dir in [script_dir.parent, script_dir / 'Export_da_Wordpress']:
            for f in search_dir.glob('*.xml'):
                xml_file = f
                break
    
    if not xml_file:
        print("ERRORE: File XML WordPress non trovato!")
        print("Copia il file .xml nella cartella missotter-sito")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"File XML: {xml_file.name}")
    print(f"Cartella content: {content_dir}")
    print()
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
    }
    
    # Mappa: slug WordPress -> percorso Hugo
    page_mapping = {
        'about': 'chi-sono',
        'home': '_home',  # Speciale: diventa content/_index.md
        'tutto': 'tutto',
        'la-biblioteca': 'biblioteca',
        'proposte-editoriali': 'proposte-editoriali',
        'traduzioni': 'traduzioni',
    }
    
    changes = []
    
    for item in root.findall('.//item'):
        post_type = item.find('wp:post_type', ns)
        status = item.find('wp:status', ns)
        
        if post_type is None or status is None:
            continue
        if post_type.text != 'page' or status.text != 'publish':
            continue
        
        title_elem = item.find('title')
        title = title_elem.text if title_elem is not None else 'Senza titolo'
        
        slug_elem = item.find('wp:post_name', ns)
        slug = slug_elem.text if slug_elem is not None else ''
        
        content_elem = item.find('content:encoded', ns)
        raw_content = content_elem.text if content_elem is not None else ''
        
        if slug not in page_mapping:
            print(f"SKIP: {title} (slug '{slug}' non mappato)")
            continue
        
        if not raw_content or len(raw_content) < 10:
            print(f"SKIP: {title} (contenuto vuoto)")
            continue
        
        hugo_path = page_mapping[slug]
        
        # Converti contenuto
        md_content = clean_wordpress_content(raw_content)
        
        # Determina percorso file
        if hugo_path == '_home':
            # Homepage: content/_index.md
            target_file = content_dir / '_index.md'
            display_title = "La biblioteca di Miss Otter"
        else:
            # Altre pagine: content/sezione/_index.md
            target_dir = content_dir / hugo_path
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / '_index.md'
            display_title = title
        
        # Crea contenuto completo
        full_content = create_frontmatter(display_title)
        full_content += md_content
        
        # Scrivi file
        print(f"Scrivo: {target_file.relative_to(script_dir)}")
        print(f"   Titolo: {display_title}")
        print(f"   Contenuto: {len(md_content)} caratteri")
        
        # Backup se esiste
        if target_file.exists():
            backup = target_file.with_suffix('.md.bak-old')
            target_file.rename(backup)
        
        target_file.write_text(full_content, encoding='utf-8')
        changes.append(f"{slug} -> {target_file.relative_to(script_dir)}")
        print()
    
    # Crea _index.md per le sottosezioni di biblioteca (se non esistono)
    sottosezioni = ['fiordafiore', 'nuoviarrivi', 'oldies', 'vecchieglorie']
    titoli_sottosezioni = {
        'fiordafiore': 'Fior da Fiore',
        'nuoviarrivi': 'Nuovi Arrivi', 
        'oldies': 'Oldies',
        'vecchieglorie': 'Vecchie Glorie'
    }
    
    print("Verifico sottosezioni biblioteca...")
    for sez in sottosezioni:
        sez_dir = content_dir / 'biblioteca' / sez
        sez_index = sez_dir / '_index.md'
        
        if sez_dir.exists() and not sez_index.exists():
            print(f"   Creo: biblioteca/{sez}/_index.md")
            sez_content = create_frontmatter(titoli_sottosezioni.get(sez, sez.title()))
            sez_index.write_text(sez_content, encoding='utf-8')
            changes.append(f"biblioteca/{sez}/_index.md (creato)")
    
    print()
    print("=" * 70)
    print("COMPLETATO!")
    print(f"Modifiche: {len(changes)}")
    for c in changes:
        print(f"  ✓ {c}")
    print()
    print("Ora fai commit e push con GitHub Desktop")
    print("=" * 70)
    input("\nPremi INVIO per chiudere...")


if __name__ == '__main__':
    main()
