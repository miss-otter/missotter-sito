#!/usr/bin/env python3
"""
CORREGGI ENCODING UTF-8 - Versione 3
"""

import os
import sys
from pathlib import Path

def fix_file(filepath):
    """Corregge l'encoding di un file."""
    print(f"  {filepath.name}...", end=' ')
    
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
    except Exception as e:
        print(f"ERRORE lettura: {e}")
        return False
    
    try:
        text = raw.decode('utf-8')
        
        if b'\xc3' in raw and b'\xc2' in raw:
            try:
                text = raw.decode('utf-8').encode('latin-1').decode('utf-8')
                print("CORRETTO (double-encoding)")
                
                backup = filepath.with_suffix('.md.bak')
                with open(backup, 'wb') as f:
                    f.write(raw)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                return True
            except:
                pass
        
        print("OK")
        return True
        
    except UnicodeDecodeError:
        try:
            text = raw.decode('latin-1')
            print("CORRETTO (da latin-1)")
            
            backup = filepath.with_suffix('.md.bak')
            with open(backup, 'wb') as f:
                f.write(raw)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"ERRORE: {e}")
            return False

def main():
    print("=" * 50)
    print("CORREZIONE ENCODING UTF-8")
    print("=" * 50)
    print()
    
    # USA LA CARTELLA DOVE SI TROVA LO SCRIPT
    script_dir = Path(__file__).parent.absolute()
    print(f"Cartella script: {script_dir}")
    
    # Cerca content nella stessa cartella dello script
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print(f"\nERRORE: Cartella 'content' non trovata in:")
        print(f"  {script_dir}")
        print()
        print("Contenuto della cartella:")
        for item in script_dir.iterdir():
            print(f"  {item.name}")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"Cartella content: {content_dir}")
    print()
    
    md_files = list(content_dir.rglob('*.md'))
    print(f"Trovati {len(md_files)} file .md")
    print()
    
    for f in md_files:
        fix_file(f)
    
    print()
    print("=" * 50)
    print("COMPLETATO!")
    print("=" * 50)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
