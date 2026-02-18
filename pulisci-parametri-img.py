#!/usr/bin/env python3
"""
PULISCI PARAMETRI IMMAGINI
Rimuove ?w=xxx e simili dai riferimenti alle immagini
"""

import re
from pathlib import Path

def fix_file(filepath):
    print(f"  {filepath.name}...", end=' ')
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERRORE: {e}")
        return False
    
    original = content
    
    # Rimuovi parametri URL dalle immagini
    # Pattern: .jpg?w=123 o .png?w=456&h=789 ecc
    # Diventa: .jpg o .png
    content = re.sub(
        r'(\.(jpg|jpeg|png|gif|webp))\?[^)\s\]"\']+',
        r'\1',
        content,
        flags=re.IGNORECASE
    )
    
    if content != original:
        # Backup
        backup = filepath.with_suffix('.md.param-bak')
        try:
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(original)
        except:
            pass
        
        # Salva
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("CORRETTO")
        return True
    else:
        print("OK")
        return True

def main():
    print("=" * 50)
    print("PULISCI PARAMETRI IMMAGINI (?w=xxx)")
    print("=" * 50)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"Cartella: {content_dir}")
    print()
    
    md_files = list(content_dir.rglob('*.md'))
    print(f"Trovati {len(md_files)} file .md")
    print()
    
    for f in md_files:
        fix_file(f)
    
    print()
    print("=" * 50)
    print("COMPLETATO!")
    print("Ora riesegui verifica-immagini.py per vedere")
    print("quali immagini mancano davvero.")
    print("=" * 50)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
