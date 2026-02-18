#!/usr/bin/env python3
"""
SISTEMA LINK IMMAGINI E PULISCI MARKDOWN
- Sostituisce URL WordPress con nome file locale
- Rimuove parentesi quadre orfane
"""

import os
import re
from pathlib import Path

def fix_markdown_file(filepath):
    """Corregge i link e pulisce il Markdown."""
    print(f"  {filepath.name}...", end=' ')
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"ERRORE lettura: {e}")
        return False
    
    original = content
    
    # 1. SOSTITUISCI URL WORDPRESS CON NOME FILE LOCALE
    # Pattern: qualsiasi URL che contiene missotter.wordpress.com/wp-content/uploads/
    def replace_wp_url(match):
        url = match.group(0)
        # Estrai solo il nome del file dalla fine dell'URL
        filename = url.split('/')[-1]
        # Rimuovi eventuali query string
        if '?' in filename:
            filename = filename.split('?')[0]
        return filename
    
    # Trova e sostituisci URL WordPress
    wp_pattern = r'https?://[^\s\)\]\"\']*missotter\.wordpress\.com/wp-content/uploads/[^\s\)\]\"\']*\.(?:jpg|jpeg|png|gif|webp)'
    content = re.sub(wp_pattern, replace_wp_url, content, flags=re.IGNORECASE)
    
    # 2. PULISCI PARENTESI ORFANE
    
    # Rimuovi righe che iniziano con ]( - sono link spezzati
    content = re.sub(r'^\]\([^\)]*\)\s*$', '', content, flags=re.MULTILINE)
    
    # Rimuovi ]( seguito da URL che ora e' solo un filename, a inizio riga
    content = re.sub(r'^\]\([^\)]+\)', '', content, flags=re.MULTILINE)
    
    # Rimuovi righe vuote multiple (lascia max 2)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Conta modifiche
    if content != original:
        # Backup
        backup = filepath.with_suffix('.md.link-bak')
        try:
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(original)
        except:
            pass
        
        # Salva modificato
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("CORRETTO")
            return True
        except Exception as e:
            print(f"ERRORE scrittura: {e}")
            return False
    else:
        print("OK (nessuna modifica)")
        return True

def main():
    print("=" * 50)
    print("SISTEMA LINK IMMAGINI E PULISCI MARKDOWN")
    print("=" * 50)
    print()
    
    # Usa la cartella dove si trova lo script
    script_dir = Path(__file__).parent.absolute()
    print(f"Cartella script: {script_dir}")
    
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print(f"\nERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"Cartella content: {content_dir}")
    print()
    
    md_files = list(content_dir.rglob('*.md'))
    print(f"Trovati {len(md_files)} file .md")
    print()
    
    corrected = 0
    for f in md_files:
        if fix_markdown_file(f):
            corrected += 1
    
    print()
    print("=" * 50)
    print(f"COMPLETATO! File processati: {corrected}")
    print("=" * 50)
    print()
    print("Ora fai commit e push con GitHub Desktop")
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
