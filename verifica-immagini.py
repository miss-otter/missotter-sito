#!/usr/bin/env python3
"""
VERIFICA IMMAGINI
Controlla se le immagini referenziate nei file .md esistono davvero
"""

import re
from pathlib import Path

def check_file(filepath):
    post_dir = filepath.parent
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    # Trova tutti i riferimenti a immagini
    # Pattern: ![testo](immagine.jpg) oppure ![](immagine.jpg)
    img_pattern = r'!\[[^\]]*\]\(([^)]+)\)'
    matches = re.findall(img_pattern, content)
    
    missing = []
    for img_ref in matches:
        # Salta URL esterni
        if img_ref.startswith('http'):
            continue
        
        # Controlla se il file esiste
        img_path = post_dir / img_ref
        if not img_path.exists():
            missing.append((filepath.name, img_ref))
    
    return missing

def main():
    print("=" * 50)
    print("VERIFICA IMMAGINI MANCANTI")
    print("=" * 50)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    md_files = list(content_dir.rglob('*.md'))
    print(f"Controllo {len(md_files)} file .md...")
    print()
    
    all_missing = []
    for f in md_files:
        missing = check_file(f)
        all_missing.extend(missing)
    
    if all_missing:
        print(f"TROVATE {len(all_missing)} IMMAGINI MANCANTI:")
        print("-" * 50)
        for md_file, img in all_missing:
            print(f"  {md_file}: {img}")
    else:
        print("Tutte le immagini sono presenti!")
    
    print()
    print("=" * 50)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
