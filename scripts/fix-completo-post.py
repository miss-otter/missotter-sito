#!/usr/bin/env python3
"""
FIX COMPLETO POST
1. Converte [caption]...[/caption] WordPress in Markdown
2. Aggiunge thumbnail al frontmatter per le immagini di anteprima
"""

import re
from pathlib import Path

def fix_captions(content):
    """Converte i caption WordPress in Markdown"""
    
    # Pattern: [caption id="..." align="..." width="..."]contenuto[/caption]
    pattern = r'\[caption[^\]]*\](.*?)\[/caption\]'
    
    def replace_caption(match):
        inner = match.group(1).strip()
        
        # Cerca immagine Markdown ![](...)
        img_match = re.search(r'!\[[^\]]*\]\([^)]+\)', inner)
        if img_match:
            img = img_match.group(0)
            caption_text = inner.replace(img, '').strip()
            if caption_text:
                return f'{img}\n\n*{caption_text}*'
            return img
        
        # Cerca tag <img>
        img_tag_match = re.search(r'<img[^>]+>', inner, re.IGNORECASE)
        if img_tag_match:
            src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag_match.group(0))
            if src_match:
                filename = src_match.group(1).split('/')[-1].split('?')[0]
                caption_text = re.sub(r'<img[^>]+>', '', inner).strip()
                if caption_text:
                    return f'![]({filename})\n\n*{caption_text}*'
                return f'![]({filename})'
        
        return inner
    
    return re.sub(pattern, replace_caption, content, flags=re.DOTALL)


def find_first_image(content):
    """Trova la prima immagine nel contenuto"""
    
    # Cerca pattern ![...](filename.ext)
    match = re.search(r'!\[[^\]]*\]\(([^)]+)\)', content)
    if match:
        img_ref = match.group(1)
        # Prendi solo il nome file
        filename = img_ref.split('/')[-1].split('?')[0]
        # Verifica che sia un'immagine
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return filename
    
    return None


def add_thumbnail_to_frontmatter(content, thumbnail):
    """Aggiunge thumbnail al frontmatter se non presente"""
    
    if not content.startswith('---'):
        return content, False
    
    # Controlla se ha già thumbnail
    if 'thumbnail:' in content or 'image:' in content or 'featuredImage:' in content:
        return content, False
    
    # Trova la fine del frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content, False
    
    frontmatter = parts[1].strip()
    body = parts[2]
    
    # Aggiungi thumbnail
    new_frontmatter = frontmatter + f'\nthumbnail: "{thumbnail}"'
    new_content = f'---\n{new_frontmatter}\n---{body}'
    
    return new_content, True


def process_file(filepath):
    """Processa un singolo file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'error': str(e)}
    
    original = content
    changes = []
    
    # 1. Sistema caption
    if '[caption' in content.lower():
        content = fix_captions(content)
        if content != original:
            changes.append('caption')
    
    # 2. Aggiungi thumbnail se mancante
    first_img = find_first_image(content)
    if first_img:
        content, added = add_thumbnail_to_frontmatter(content, first_img)
        if added:
            changes.append('thumbnail')
    
    # Salva se modificato
    if content != original:
        # Backup
        backup = filepath.with_suffix('.md.fix-bak')
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(original)
        
        # Salva
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {'modified': True, 'changes': changes}
    
    return {'modified': False}


def main():
    print("=" * 60)
    print("FIX COMPLETO POST")
    print("=" * 60)
    print()
    print("Questo script:")
    print("  1. Converte [caption]...[/caption] in Markdown")
    print("  2. Aggiunge thumbnail al frontmatter")
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Trova tutti i file index.md nei page bundles (post)
    # I post sono in cartelle con un proprio index.md
    md_files = []
    for md in content_dir.rglob('index.md'):
        # Escludi _index.md (sezioni) e file nella root
        if md.name == 'index.md':
            md_files.append(md)
    
    print(f"Trovati {len(md_files)} post (index.md)...")
    print()
    
    caption_fixed = 0
    thumb_added = 0
    
    for f in md_files:
        rel_path = f.relative_to(content_dir)
        result = process_file(f)
        
        if 'error' in result:
            print(f"  ✗ {rel_path}: {result['error']}")
        elif result.get('modified'):
            changes = result.get('changes', [])
            print(f"  ✓ {rel_path}: {', '.join(changes)}")
            if 'caption' in changes:
                caption_fixed += 1
            if 'thumbnail' in changes:
                thumb_added += 1
    
    print()
    print("=" * 60)
    print(f"COMPLETATO!")
    print(f"  - Caption sistemati: {caption_fixed}")
    print(f"  - Thumbnail aggiunti: {thumb_added}")
    print()
    print("Ora fai commit e push con GitHub Desktop")
    print("=" * 60)
    input("\nPremi INVIO per chiudere...")


if __name__ == '__main__':
    main()
