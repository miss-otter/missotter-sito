#!/usr/bin/env python3
"""
RIPRISTINA MENU ORIGINALE
Rimuove l'header.html personalizzato che ha rotto il menu.
Il menu tornerà alla striscia verde orizzontale di Clarity.
"""

from pathlib import Path
import shutil

def main():
    print("=" * 60)
    print("RIPRISTINA MENU ORIGINALE")
    print("=" * 60)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    
    # Cerca e rimuovi header.html
    header_file = script_dir / 'layouts' / 'partials' / 'header.html'
    
    if header_file.exists():
        # Backup
        backup = script_dir / 'header.html.ROTTO'
        shutil.move(header_file, backup)
        print(f"✓ Rimosso: layouts/partials/header.html")
        print(f"  (backup salvato in: header.html.ROTTO)")
        print()
        print("Il menu tornerà alla striscia verde originale di Clarity.")
    else:
        print("layouts/partials/header.html non esiste.")
        print("Il menu dovrebbe già essere quello originale di Clarity.")
    
    # Rimuovi anche la cartella se è vuota
    partials_dir = script_dir / 'layouts' / 'partials'
    if partials_dir.exists() and not any(partials_dir.iterdir()):
        partials_dir.rmdir()
        print("✓ Rimossa cartella vuota: layouts/partials/")
    
    layouts_dir = script_dir / 'layouts'
    if layouts_dir.exists() and not any(layouts_dir.iterdir()):
        layouts_dir.rmdir()
        print("✓ Rimossa cartella vuota: layouts/")
    
    print()
    print("=" * 60)
    print("Ora fai commit e push con GitHub Desktop.")
    print("Il menu tornerà normale.")
    print("=" * 60)
    print()
    print("Per il dropdown e l'immagine header, ci pensiamo domani")
    print("con più calma dopo aver studiato meglio Clarity.")
    print()
    input("Premi INVIO per chiudere...")


if __name__ == '__main__':
    main()
