#!/usr/bin/env python3
"""
RIORGANIZZA PAGINE PER HUGO
Sposta le pagine da content/pages/ alla posizione corretta
"""

import shutil
from pathlib import Path

def main():
    print("=" * 60)
    print("RIORGANIZZA PAGINE PER HUGO")
    print("=" * 60)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    pages_dir = content_dir / 'pages'
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    if not pages_dir.exists():
        print("ERRORE: Cartella 'content/pages' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"Cartella content: {content_dir}")
    print(f"Cartella pages: {pages_dir}")
    print()
    
    # Backup: non spostiamo, copiamo prima
    changes = []
    
    # 1. traduzioni -> content/traduzioni/
    src = pages_dir / 'traduzioni'
    dst = content_dir / 'traduzioni'
    if src.exists() and not dst.exists():
        print(f"Sposto: pages/traduzioni -> traduzioni/")
        shutil.move(str(src), str(dst))
        changes.append("traduzioni")
    elif src.exists() and dst.exists():
        print(f"ATTENZIONE: traduzioni esiste gia, unisco i contenuti...")
        for item in src.iterdir():
            target = dst / item.name
            if not target.exists():
                shutil.move(str(item), str(target))
        shutil.rmtree(str(src))
        changes.append("traduzioni (unito)")
    
    # 2. about -> content/chi-sono/
    src = pages_dir / 'about'
    dst = content_dir / 'chi-sono'
    if src.exists():
        print(f"Sposto: pages/about -> chi-sono/")
        if dst.exists():
            shutil.rmtree(str(dst))
        shutil.move(str(src), str(dst))
        changes.append("about -> chi-sono")
    
    # 3. home -> content/_index.md (per la homepage)
    src = pages_dir / 'home'
    if src.exists():
        print(f"Sposto: pages/home/index.md -> _index.md")
        src_index = src / 'index.md'
        dst_index = content_dir / '_index.md'
        if src_index.exists():
            # Copia le immagini nella cartella static o assets
            for img in src.glob('*.jpg'):
                img_dst = script_dir / 'static' / 'images' / img.name
                img_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(str(img), str(img_dst))
                print(f"  Copiata immagine: {img.name} -> static/images/")
            for img in src.glob('*.jpeg'):
                img_dst = script_dir / 'static' / 'images' / img.name
                img_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(str(img), str(img_dst))
                print(f"  Copiata immagine: {img.name} -> static/images/")
            for img in src.glob('*.png'):
                img_dst = script_dir / 'static' / 'images' / img.name
                img_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(str(img), str(img_dst))
                print(f"  Copiata immagine: {img.name} -> static/images/")
            
            shutil.copy(str(src_index), str(dst_index))
            shutil.rmtree(str(src))
            changes.append("home -> _index.md")
    
    # 4. la-biblioteca -> content/biblioteca/_index.md
    src = pages_dir / 'la-biblioteca'
    dst = content_dir / 'biblioteca'
    if src.exists():
        print(f"Sposto: pages/la-biblioteca -> biblioteca/_index.md")
        src_index = src / 'index.md'
        dst_index = dst / '_index.md'
        if src_index.exists() and dst.exists():
            # Copia immagini
            for img in src.glob('*.jpg'):
                shutil.copy(str(img), str(dst / img.name))
            for img in src.glob('*.jpeg'):
                shutil.copy(str(img), str(dst / img.name))
            for img in src.glob('*.png'):
                shutil.copy(str(img), str(dst / img.name))
            
            shutil.copy(str(src_index), str(dst_index))
            shutil.rmtree(str(src))
            changes.append("la-biblioteca -> biblioteca/_index.md")
    
    # 5. proposte-editoriali -> content/proposte-editoriali/
    src = pages_dir / 'proposte-editoriali'
    dst = content_dir / 'proposte-editoriali'
    if src.exists():
        print(f"Sposto: pages/proposte-editoriali -> proposte-editoriali/")
        shutil.move(str(src), str(dst))
        changes.append("proposte-editoriali")
    
    # 6. tutto -> content/tutto/ (archivio)
    src = pages_dir / 'tutto'
    dst = content_dir / 'tutto'
    if src.exists():
        print(f"Sposto: pages/tutto -> tutto/")
        shutil.move(str(src), str(dst))
        changes.append("tutto")
    
    # 7. Crea content/breadcrumbs/ se non esiste
    breadcrumbs_dir = content_dir / 'breadcrumbs'
    if not breadcrumbs_dir.exists():
        print(f"Creo: breadcrumbs/")
        breadcrumbs_dir.mkdir()
        # Crea un _index.md vuoto
        index_content = """---
title: "Breadcrumbs"
---

Contenuti in arrivo...
"""
        (breadcrumbs_dir / '_index.md').write_text(index_content, encoding='utf-8')
        changes.append("breadcrumbs (creato)")
    
    # 8. Rimuovi la cartella pages se vuota
    if pages_dir.exists():
        remaining = list(pages_dir.iterdir())
        if not remaining:
            print(f"Rimuovo: pages/ (vuota)")
            pages_dir.rmdir()
        else:
            print(f"\nATTENZIONE: In pages/ rimangono: {[x.name for x in remaining]}")
    
    print()
    print("=" * 60)
    print("COMPLETATO!")
    print(f"Modifiche: {len(changes)}")
    for c in changes:
        print(f"  - {c}")
    print()
    print("Ora fai commit e push con GitHub Desktop")
    print("=" * 60)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
