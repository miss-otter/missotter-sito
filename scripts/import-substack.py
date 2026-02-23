#!/usr/bin/env python3
"""
IMPORT SUBSTACK → HUGO (con immagini)

Cosa fa questo script:
1. Legge il feed RSS di Substack
2. Per ogni nuovo articolo:
   - Crea una cartella in content/breadcrumbs/
   - Scarica la prima immagine trovata come cover.jpg
   - Converte il contenuto HTML in Markdown
   - Genera index.md con frontmatter (incluso image: se trovata)
3. Tiene traccia degli articoli già importati per non duplicarli

NOTA: Substack mette nel feed RSS solo gli Articles (articoli lunghi).
I Notes (post brevi tipo social) NON hanno RSS, quindi non vengono importati.
Per i Notes, aggiungili manualmente nella sezione Breadcrumbs.

Uso:
  python scripts/import-substack.py
"""

import feedparser
import re
import os
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
import hashlib
import html
import ssl

SUBSTACK_RSS = "https://smallbreadcrumbs.substack.com/feed"
CONTENT_DIR = Path("content/breadcrumbs")
IMPORTED_FILE = Path("scripts/.imported-substack.txt")

def get_imported_ids():
    """Legge gli ID degli articoli già importati"""
    if IMPORTED_FILE.exists():
        return set(IMPORTED_FILE.read_text().strip().split('\n'))
    return set()

def save_imported_id(post_id):
    """Salva l'ID di un articolo importato"""
    IMPORTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(IMPORTED_FILE, 'a') as f:
        f.write(f"{post_id}\n")

def slugify(text):
    """Converte un titolo in slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def extract_first_image(html_content):
    """Estrae l'URL della prima immagine dal contenuto HTML"""
    # Pattern per tag img
    img_patterns = [
        r'<img[^>]*src=["\']([^"\']+)["\']',
        r'<img[^>]*srcset=["\']([^\s"\']+)',
    ]
    
    for pattern in img_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            url = match.group(1)
            # Decodifica URL encoded
            url = urllib.parse.unquote(url)
            # Rimuovi parametri Substack CDN se presenti
            if 'substackcdn.com' in url:
                # Estrai l'URL originale dopo il fetch/
                inner_match = re.search(r'https%3A%2F%2F[^&\s"\']+|https://[^&\s"\']+s3\.amazonaws[^&\s"\']+', url)
                if inner_match:
                    url = urllib.parse.unquote(inner_match.group(0))
            return url
    
    return None

def download_image(url, save_path):
    """Scarica un'immagine da URL e la salva localmente"""
    try:
        # Ignora errori SSL (alcuni CDN hanno certificati problematici)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        # Headers per sembrare un browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            content_type = response.headers.get('Content-Type', '')
            
            # Determina estensione dal content-type
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            else:
                # Prova a dedurre dall'URL
                if '.png' in url.lower():
                    ext = '.png'
                elif '.gif' in url.lower():
                    ext = '.gif'
                elif '.webp' in url.lower():
                    ext = '.webp'
                else:
                    ext = '.jpg'
            
            # Aggiorna il path con l'estensione corretta
            save_path = save_path.with_suffix(ext)
            
            with open(save_path, 'wb') as f:
                f.write(response.read())
            
            return save_path.name
            
    except Exception as e:
        print(f"    ⚠ Errore download immagine: {e}")
        return None

def html_to_markdown(content):
    """Converte HTML in Markdown"""
    # Rimuovi le immagini (le mettiamo come cover, non nel contenuto)
    # content = re.sub(r'<img[^>]*>', '', content)
    
    # Paragrafi
    content = re.sub(r'<p[^>]*>', '\n\n', content)
    content = re.sub(r'</p>', '', content)
    
    # Headers
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n\n# \1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n\n', content, flags=re.DOTALL)
    
    # Formattazione testo
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
    
    # Link
    content = re.sub(r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
    
    # Liste
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
    content = re.sub(r'</?[uo]l[^>]*>', '\n', content)
    
    # Blockquote
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n> ' + m.group(1).strip().replace('\n', '\n> ') + '\n', content, flags=re.DOTALL)
    
    # Line breaks
    content = re.sub(r'<br\s*/?>', '\n', content)
    
    # Rimuovi tag rimanenti
    content = re.sub(r'<[^>]+>', '', content)
    
    # Decodifica entità HTML
    content = html.unescape(content)
    
    # Pulisci spazi multipli
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def main():
    print("=" * 50)
    print("IMPORT SUBSTACK → HUGO")
    print("=" * 50)
    print("(Solo Articles - i Notes vanno aggiunti manualmente)")
    print()
    
    feed = feedparser.parse(SUBSTACK_RSS)
    imported = get_imported_ids()
    
    if not feed.entries:
        print("⚠ Nessun articolo trovato nel feed RSS")
        return
    
    print(f"Trovati {len(feed.entries)} articoli nel feed")
    
    new_count = 0
    for entry in feed.entries:
        post_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
        
        if post_id in imported:
            print(f"  ⏭ Già importato: {entry.title[:40]}...")
            continue
        
        print(f"\n📝 Importo: {entry.title[:50]}...")
        
        slug = slugify(entry.title)
        date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
        content_html = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
        
        # Crea cartella
        post_dir = CONTENT_DIR / slug
        post_dir.mkdir(parents=True, exist_ok=True)
        
        # Estrai e scarica immagine
        image_filename = None
        image_url = extract_first_image(content_html)
        if image_url:
            print(f"    🖼 Scarico immagine...")
            image_filename = download_image(image_url, post_dir / "cover")
            if image_filename:
                print(f"    ✓ Salvata come {image_filename}")
        
        # Prepara frontmatter
        safe_title = entry.title.replace('"', "'")
        
        frontmatter_lines = [
            '---',
            f'title: "{safe_title}"',
            f'date: {date.strftime("%Y-%m-%dT%H:%M:%S+01:00")}',
            'draft: false',
            'source: "substack"',
            f'original_url: "{entry.link}"',
        ]
        
        if image_filename:
            frontmatter_lines.append(f'image: "{image_filename}"')
        
        frontmatter_lines.append('---')
        
        # Genera contenuto
        content = '\n'.join(frontmatter_lines) + '\n\n' + html_to_markdown(content_html)
        
        # Salva
        (post_dir / "index.md").write_text(content, encoding='utf-8')
        save_imported_id(post_id)
        print(f"    ✓ Creato: {post_dir}/index.md")
        new_count += 1
    
    print()
    print("=" * 50)
    print(f"Completato! {new_count} nuovi articoli importati.")
    if new_count > 0:
        print("\nRicorda di fare commit e push delle modifiche!")
    print("=" * 50)

if __name__ == '__main__':
    main()
