#!/usr/bin/env python3
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
        return set(IMPORTED_FILE.read_text().strip().split('\n'))
    return set()

def save_imported_id(post_id):
    IMPORTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(IMPORTED_FILE, 'a') as f:
        f.write(f"{post_id}\n")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def html_to_markdown(content):
    content = re.sub(r'<p[^>]*>', '\n\n', content)
    content = re.sub(r'</p>', '', content)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
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
title: "{entry.title.replace('"', '\\"')}"
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
