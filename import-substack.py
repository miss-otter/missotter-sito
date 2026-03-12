#!/usr/bin/env python3
"""
IMPORT SUBSTACK → HUGO (bilingue)
Scarica gli articoli dai feed RSS di entrambi i Substack e li converte in post Hugo.

- smallbreadcrumbs.substack.com (EN) → content/en/breadcrumbs/
- laleneve.substack.com (IT) → content/it/breadcrumbs/

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

# Configurazione feed
FEEDS = [
    {
        "name": "Breadcrumbs (EN)",
        "url": "https://smallbreadcrumbs.substack.com/feed",
        "content_dir": Path("content/en/breadcrumbs"),
        "imported_file": Path("scripts/.imported-substack-en.txt"),
    },
    {
        "name": "Miss Otter (IT)",
        "url": "https://laleneve.substack.com/feed",
        "content_dir": Path("content/it/breadcrumbs"),
        "imported_file": Path("scripts/.imported-substack-it.txt"),
    },
]


def get_imported_ids(imported_file):
    """Legge gli ID dei post già importati"""
    if imported_file.exists():
        lines = imported_file.read_text().strip().split('\n')
        return set(l for l in lines if l)
    return set()


def save_imported_id(imported_file, post_id):
    """Salva un ID come importato"""
    imported_file.parent.mkdir(parents=True, exist_ok=True)
    with open(imported_file, 'a') as f:
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


def create_post(entry, slug, content_dir):
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
    post_dir = content_dir / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    
    # Scrivi file
    index_file = post_dir / "index.md"
    index_file.write_text(frontmatter + content_md, encoding='utf-8')
    
    return post_dir


def import_feed(feed_config):
    """Importa un singolo feed"""
    name = feed_config["name"]
    url = feed_config["url"]
    content_dir = feed_config["content_dir"]
    imported_file = feed_config["imported_file"]
    
    print(f"\n--- {name} ---")
    print(f"Feed: {url}")
    print(f"Destinazione: {content_dir}")
    
    # Scarica feed
    feed = feedparser.parse(url)
    
    if feed.bozo:
        print(f"ERRORE nel parsing del feed: {feed.bozo_exception}")
        return 0, 0
    
    print(f"Trovati {len(feed.entries)} articoli nel feed")
    
    # ID già importati
    imported = get_imported_ids(imported_file)
    print(f"Articoli già importati: {len(imported)}")
    
    # Processa ogni entry
    new_posts = 0
    skipped_existing = 0
    
    for entry in feed.entries:
        post_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
        
        if post_id in imported:
            skipped_existing += 1
            continue
        
        slug = slugify(entry.title)
        
        print(f"  IMPORT: {entry.title[:50]}...")
        create_post(entry, slug, content_dir)
        
        save_imported_id(imported_file, post_id)
        new_posts += 1
    
    return new_posts, skipped_existing


def main():
    print("=" * 60)
    print("IMPORT SUBSTACK → HUGO (bilingue)")
    print("=" * 60)
    print()
    print("NOTA: Solo gli Articles hanno RSS.")
    print("I Notes (post brevi) vanno aggiunti manualmente.")
    
    total_new = 0
    total_skipped = 0
    
    for feed_config in FEEDS:
        new, skipped = import_feed(feed_config)
        total_new += new
        total_skipped += skipped
    
    print()
    print("=" * 60)
    print(f"COMPLETATO!")
    print(f"  - Nuovi articoli importati: {total_new}")
    print(f"  - Già presenti: {total_skipped}")
    print("=" * 60)


if __name__ == '__main__':
    main()
