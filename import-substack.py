#!/usr/bin/env python3
"""
IMPORT SUBSTACK → HUGO
Scarica gli articoli dal feed RSS di Substack e li converte in post Hugo.

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

# Configurazione
SUBSTACK_RSS = "https://smallbreadcrumbs.substack.com/feed"
CONTENT_DIR = Path("content/breadcrumbs")
IMPORTED_FILE = Path("scripts/.imported-substack.txt")


def get_imported_ids():
    """Legge gli ID dei post già importati"""
    if IMPORTED_FILE.exists():
        return set(IMPORTED_FILE.read_text().strip().split('\n'))
    return set()


def save_imported_id(post_id):
    """Salva un ID come importato"""
    IMPORTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(IMPORTED_FILE, 'a') as f:
        f.write(f"{post_id}\n")


def slugify(text):
    """Converte testo in slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def html_to_markdown(html_content):
    """Converte HTML in Markdown (versione semplificata)"""
    content = html_content
    
    # Paragrafi
    content = re.sub(r'<p[^>]*>', '\n\n', content)
    content = re.sub(r'</p>', '', content)
    
    # Headings
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n\n# \1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n\n', content, flags=re.DOTALL)
    
    # Bold e italic
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
    
    # Link
    content = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
    
    # Immagini
    content = re.sub(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', content)
    content = re.sub(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*/?>', r'![](\1)', content)
    
    # Liste
    content = re.sub(r'<ul[^>]*>', '\n', content)
    content = re.sub(r'</ul>', '\n', content)
    content = re.sub(r'<ol[^>]*>', '\n', content)
    content = re.sub(r'</ol>', '\n', content)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
    
    # Blockquote
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n> ' + m.group(1).replace('\n', '\n> ') + '\n', content, flags=re.DOTALL)
    
    # Rimuovi tag rimanenti
    content = re.sub(r'<[^>]+>', '', content)
    
    # Decode HTML entities
    content = html.unescape(content)
    
    # Pulisci spazi
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    return content


def create_post(entry, slug):
    """Crea un post Hugo dal feed entry"""
    
    # Parse data
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        date = datetime(*entry.published_parsed[:6])
    else:
        date = datetime.now()
    
    date_str = date.strftime('%Y-%m-%dT%H:%M:%S+01:00')
    
    # Contenuto
    content_html = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    content_md = html_to_markdown(content_html)
    
    # Frontmatter
    frontmatter = f'''---
title: "{entry.title.replace('"', '\\"')}"
date: {date_str}
draft: false
source: "substack"
original_url: "{entry.link}"
---

'''
    
    # Crea cartella post (page bundle)
    post_dir = CONTENT_DIR / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    
    # Scrivi file
    index_file = post_dir / "index.md"
    index_file.write_text(frontmatter + content_md, encoding='utf-8')
    
    return post_dir


def main():
    print("=" * 60)
    print("IMPORT SUBSTACK → HUGO")
    print("=" * 60)
    print()
    print("NOTA: Solo gli Articles hanno RSS.")
    print("I Notes (post brevi) vanno aggiunti manualmente.")
    print()
    
    # Scarica feed
    print(f"Scarico feed: {SUBSTACK_RSS}")
    feed = feedparser.parse(SUBSTACK_RSS)
    
    if feed.bozo:
        print(f"ERRORE nel parsing del feed: {feed.bozo_exception}")
        return
    
    print(f"Trovati {len(feed.entries)} articoli nel feed")
    print()
    
    # ID già importati
    imported = get_imported_ids()
    print(f"Articoli già importati: {len(imported)}")
    
    # Processa ogni entry
    new_posts = 0
    skipped_existing = 0
    
    for entry in feed.entries:
        # ID univoco basato su URL
        post_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
        
        # Già importato?
        if post_id in imported:
            skipped_existing += 1
            continue
        
        # Crea slug
        slug = slugify(entry.title)
        
        # Crea post
        print(f"  IMPORT: {entry.title[:50]}...")
        post_dir = create_post(entry, slug)
        
        # Segna come importato
        save_imported_id(post_id)
        new_posts += 1
    
    print()
    print("=" * 60)
    print(f"COMPLETATO!")
    print(f"  - Nuovi articoli importati: {new_posts}")
    print(f"  - Già presenti: {skipped_existing}")
    print("=" * 60)


if __name__ == '__main__':
    main()
