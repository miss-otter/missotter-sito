#!/usr/bin/env python3
"""
IMPORT SUBSTACK → HUGO (bilingue)
Scarica gli articoli dai feed RSS di entrambi i Substack e li converte in post Hugo.

- smallbreadcrumbs.substack.com (EN) → content/en/breadcrumbs/
- laleneve.substack.com (IT) → content/it/breadcrumbs/

Tutte le immagini vengono scaricate in locale.
La prima immagine viene usata come cover per l'anteprima.
Gli iframe (video embed ecc.) vengono convertiti in link cliccabili.

NOTA: Substack mette nel feed RSS solo gli Articles (articoli lunghi).
I Notes (post brevi) vanno aggiunti manualmente.
"""

import feedparser
import re
import os
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
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
    if imported_file.exists():
        lines = imported_file.read_text().strip().split('\n')
        return set(l for l in lines if l)
    return set()


def save_imported_id(imported_file, post_id):
    imported_file.parent.mkdir(parents=True, exist_ok=True)
    with open(imported_file, 'a') as f:
        f.write(f"{post_id}\n")


def slugify(text):
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


def get_extension_from_response(response, url):
    """Determina l'estensione del file dall'header o dall'URL"""
    content_type = response.headers.get('content-type', '')
    if 'jpeg' in content_type or 'jpg' in content_type:
        return '.jpg'
    elif 'png' in content_type:
        return '.png'
    elif 'gif' in content_type:
        return '.gif'
    elif 'webp' in content_type:
        return '.webp'
    else:
        parsed = urlparse(url)
        path_ext = Path(parsed.path).suffix.lower().split('?')[0]
        return path_ext if path_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'] else '.jpg'


def download_all_images(content_html, post_dir):
    """Scarica tutte le immagini dal contenuto HTML.
    Restituisce un dict {url_originale: nome_file_locale} e il nome della prima immagine."""

    img_urls = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', content_html)

    if not img_urls:
        return {}, None

    url_to_local = {}
    first_image = None

    for i, img_url in enumerate(img_urls):
        # Salta immagini già scaricate (duplicati)
        if img_url in url_to_local:
            continue

        try:
            response = requests.get(img_url, timeout=15)
            response.raise_for_status()

            # Salta file troppo piccoli (tracking pixel < 1KB)
            if len(response.content) < 1024:
                continue

            ext = get_extension_from_response(response, img_url)

            # Nome: img-01, img-02, ecc.
            filename = f"img-{i+1:02d}{ext}"
            filepath = post_dir / filename
            filepath.write_bytes(response.content)

            url_to_local[img_url] = filename
            if first_image is None:
                first_image = filename

            print(f"    Immagine {filename} ({len(response.content) // 1024}KB)")

        except Exception as e:
            print(f"    Errore download immagine {i+1}: {e}")

    return url_to_local, first_image


def html_to_markdown(content_html, image_map):
    """Converte HTML in Markdown, sostituendo gli URL delle immagini con i file locali
    e gestendo gli iframe."""
    content = content_html

    # Converti iframe in link (video embed, ecc.) — PRIMA di rimuovere i tag
    def iframe_to_link(match):
        src = re.search(r'src=["\']([^"\']+)["\']', match.group(0))
        if src:
            url = src.group(1)
            # Pulisci URL embed di YouTube
            if 'youtube.com/embed/' in url:
                video_id = url.split('/embed/')[-1].split('?')[0]
                url = f"https://www.youtube.com/watch?v={video_id}"
                return f'\n\n[Video YouTube]({url})\n\n'
            return f'\n\n[Contenuto incorporato]({url})\n\n'
        return ''

    content = re.sub(r'<iframe[^>]*>.*?</iframe>', iframe_to_link, content, flags=re.DOTALL)
    content = re.sub(r'<iframe[^>]*/>', iframe_to_link, content)

    # --- FIX 1a: Link che puntano direttamente a un'immagine (CDN Substack) ---
    # <a href="...cdn-url-immagine..."> ...qualsiasi contenuto... </a>
    # → sostituito con solo il contenuto interno (di solito l'<img> stessa).
    # Riconoscerli dall'href: contiene "/image/" o estensione immagine.
    def strip_image_link(match):
        return match.group(2)  # solo il contenuto interno

    content = re.sub(
        r'<a[^>]*href=["\']([^"\']*(?:substackcdn\.com/image|/image/fetch|\.(?:jpg|jpeg|png|gif|webp))[^"\']*)["\'][^>]*>(.*?)</a>',
        strip_image_link,
        content, flags=re.DOTALL | re.IGNORECASE
    )

    # --- FIX 1b: Link che contengono solo un'immagine (anche dentro picture/div) ---
    # <a href="..."><picture>...<img></picture></a> o simili → solo l'<img>
    def unwrap_img_link(match):
        inner = match.group(2)
        img_match = re.search(r'<img[^>]*>', inner)
        if img_match:
            # Se l'<a> contiene solo tag wrapper + img (niente testo), lasciamo solo img
            text_only = re.sub(r'<img[^>]*>', '', inner)
            text_only = re.sub(r'<[^>]+>', '', text_only).strip()
            if not text_only:
                return img_match.group(0)
        return match.group(0)

    content = re.sub(
        r'<a[^>]*href=["\'][^"\']*["\'][^>]*>(\s*(?:<(?:picture|source|div|span|figure)[^>]*>\s*)*<img[^>]*>(?:\s*</(?:picture|source|div|span|figure)>)*\s*)</a>',
        lambda m: re.search(r'<img[^>]*>', m.group(1)).group(0),
        content, flags=re.DOTALL
    )

    # --- FIX 2: Embed Substack (card con anteprima, titolo, descrizione) ---
    # Questi sono <a> con dentro molto contenuto (immagini + testo della card).
    # Li convertiamo in un semplice link con il testo visibile come etichetta.
    def simplify_embed_link(match):
        href = match.group(1)
        inner = match.group(2)
        # Rimuovi eventuali tag img interni (la card ha un'anteprima che non ci serve)
        inner_clean = re.sub(r'<img[^>]*/?>', '', inner)
        # Rimuovi tutti i tag HTML rimasti
        inner_clean = re.sub(r'<[^>]+>', ' ', inner_clean)
        # Pulisci spazi e prendi solo la prima riga significativa come titolo
        lines = [l.strip() for l in inner_clean.strip().split('\n') if l.strip()]
        if lines:
            title = lines[0][:120]  # Prima riga, max 120 char
        else:
            # Nessun testo: è solo un wrapper inutile, rimuovi tutto
            return ''
        return f'\n\n[{title}]({href})\n\n'

    # Cattura <a> che contengono più di un semplice testo (hanno tag interni)
    content = re.sub(
        r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>((?:(?!</a>).)*<(?:img|div|p|span)[^>]*>.*?)</a>',
        simplify_embed_link,
        content, flags=re.DOTALL
    )

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

    # Immagini — sostituisci URL con file locali
    def replace_img(match):
        full_tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', full_tag)
        if src_match:
            src = src_match.group(1)
            alt = alt_match.group(1) if alt_match else ''
            local = image_map.get(src, src)
            return f'![{alt}]({local})'
        return ''

    content = re.sub(r'<img[^>]*/?>', replace_img, content)

    # Liste
    content = re.sub(r'<ul[^>]*>', '\n', content)
    content = re.sub(r'</ul>', '\n', content)
    content = re.sub(r'<ol[^>]*>', '\n', content)
    content = re.sub(r'</ol>', '\n', content)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)

    # Blockquote
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>',
                     lambda m: '\n> ' + m.group(1).replace('\n', '\n> ') + '\n',
                     content, flags=re.DOTALL)

    # Rimuovi div e altri tag wrapper vuoti
    content = re.sub(r'<div[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)

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

    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        date = datetime(*entry.published_parsed[:6])
    else:
        date = datetime.now()

    date_str = date.strftime('%Y-%m-%dT%H:%M:%S+01:00')

    content_html = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')

    # Crea cartella post (page bundle)
    post_dir = content_dir / slug
    post_dir.mkdir(parents=True, exist_ok=True)

    # Scarica tutte le immagini
    image_map, first_image = download_all_images(content_html, post_dir)

    # Converti HTML in Markdown con immagini locali
    content_md = html_to_markdown(content_html, image_map)

    # --- FIX 3: Rimuovi la prima immagine dal corpo se è già nel front matter ---
    # Evita duplicazione: l'immagine di anteprima viene mostrata dai layout Hugo,
    # non serve ripeterla nel corpo del post.
    if first_image:
        # Rimuovi ![...](first_image) dall'inizio del contenuto
        pattern = re.compile(
            r'^\s*!\[[^\]]*\]\(' + re.escape(first_image) + r'\)\s*',
            re.MULTILINE
        )
        content_md = pattern.sub('', content_md, count=1).lstrip()

    # Frontmatter
    image_line = f'\nimage: "{first_image}"' if first_image else ''
    frontmatter = f'''---
title: "{entry.title.replace('"', '\\"')}"
date: {date_str}
draft: false
source: "substack"
original_url: "{entry.link}"{image_line}
---

'''

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

    feed = feedparser.parse(url)

    if feed.bozo:
        print(f"ERRORE nel parsing del feed: {feed.bozo_exception}")
        return 0, 0

    print(f"Trovati {len(feed.entries)} articoli nel feed")

    imported = get_imported_ids(imported_file)
    print(f"Articoli già importati: {len(imported)}")

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
