#!/usr/bin/env python3
"""
VERIFICA IMMAGINI v2
Mostra percorso completo dei post con immagini mancanti
"""

import re
from pathlib import Path

def check_file(filepath, content_dir):
    post_dir = filepath.parent
    # Percorso relativo dalla cartella content
    rel_path = post_dir.relative_to(content_dir)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    # Trova tutti i riferimenti a immagini
    img_pattern = r'!\[[^\]]*\]\(([^)]+)\)'
    matches = re.findall(img_pattern, content)
    
    missing = []
    for img_ref in matches:
        if img_ref.startswith('http'):
            continue
        
        img_path = post_dir / img_ref
        if not img_path.exists():
            missing.append((str(rel_path), img_ref))
    
    return missing

def main():
    print("=" * 60)
    print("VERIFICA IMMAGINI MANCANTI v2")
    print("=" * 60)
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
        missing = check_file(f, content_dir)
        all_missing.extend(missing)
    
    if all_missing:
        print(f"TROVATE {len(all_missing)} IMMAGINI MANCANTI:")
        print("-" * 60)
        
        # Raggruppa per cartella
        by_folder = {}
        for folder, img in all_missing:
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(img)
        
        for folder in sorted(by_folder.keys()):
            print(f"\n{folder}/")
            for img in by_folder[folder]:
                print(f"    - {img}")
        
        print()
        print("-" * 60)
        print(f"TOTALE: {len(all_missing)} immagini in {len(by_folder)} post")
    else:
        print("Tutte le immagini sono presenti!")
    
    print()
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
