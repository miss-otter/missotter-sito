#!/usr/bin/env python3
"""
DIAGNOSTICA COMPLETA SITO HUGO
Analizza la struttura e identifica tutti i problemi
"""

from pathlib import Path
import re

def main():
    print("=" * 70)
    print("DIAGNOSTICA COMPLETA SITO HUGO")
    print("=" * 70)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"Cartella analizzata: {content_dir}")
    print()
    
    # 1. STRUTTURA CARTELLE
    print("=" * 70)
    print("1. STRUTTURA CARTELLE IN CONTENT")
    print("=" * 70)
    
    for item in sorted(content_dir.iterdir()):
        if item.is_dir():
            files = list(item.glob('*'))
            md_files = [f.name for f in files if f.suffix == '.md']
            img_files = [f.name for f in files if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']]
            pdf_files = [f.name for f in files if f.suffix.lower() == '.pdf']
            subdirs = [f.name for f in files if f.is_dir()]
            
            print(f"\n📁 {item.name}/")
            if md_files:
                print(f"   MD: {', '.join(md_files)}")
            if img_files:
                print(f"   IMG: {len(img_files)} file ({', '.join(img_files[:3])}{'...' if len(img_files) > 3 else ''})")
            if pdf_files:
                print(f"   PDF: {len(pdf_files)} file")
            if subdirs:
                print(f"   Sottocartelle: {', '.join(subdirs)}")
        elif item.suffix == '.md':
            print(f"\n📄 {item.name} (file nella root di content)")
    
    # 2. VERIFICA PAGINE PRINCIPALI
    print()
    print("=" * 70)
    print("2. VERIFICA PAGINE PRINCIPALI")
    print("=" * 70)
    
    pagine = {
        'Homepage': content_dir / '_index.md',
        'Chi sono': content_dir / 'chi-sono' / '_index.md',
        'Biblioteca': content_dir / 'biblioteca' / '_index.md',
        'Traduzioni': content_dir / 'traduzioni' / '_index.md',
        'Proposte editoriali': content_dir / 'proposte-editoriali' / '_index.md',
        'Breadcrumbs': content_dir / 'breadcrumbs' / '_index.md',
        'Tutto': content_dir / 'tutto' / '_index.md',
    }
    
    for nome, path in pagine.items():
        if path.exists():
            size = path.stat().st_size
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            # Conta caratteri di contenuto (escluso frontmatter)
            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
                else:
                    body = content
            else:
                body = content
            
            print(f"\n✓ {nome}")
            print(f"   File: {path.relative_to(content_dir)}")
            print(f"   Dimensione: {size} bytes")
            print(f"   Contenuto: {len(body)} caratteri")
            if len(body) < 50:
                print(f"   ⚠️  CONTENUTO TROPPO CORTO!")
        else:
            # Controlla se esiste index.md invece di _index.md
            alt_path = path.parent / 'index.md' if path.name == '_index.md' else None
            if alt_path and alt_path.exists():
                print(f"\n⚠️  {nome}")
                print(f"   Trovato index.md invece di _index.md")
            else:
                print(f"\n✗ {nome} - FILE MANCANTE")
                print(f"   Atteso: {path.relative_to(content_dir)}")
    
    # 3. VERIFICA IMMAGINI NELLE PAGINE
    print()
    print("=" * 70)
    print("3. VERIFICA IMMAGINI NELLE PAGINE")
    print("=" * 70)
    
    cartelle_con_immagini = [
        ('traduzioni', ['darren_byler-edited-2.png', 'ravi_somaiya-edited.jpg', 
                        'emiliosanchezmediavilla-edited.jpeg', 'zahra_hankir-edited.jpg',
                        'altman_headshot-edited.jpeg', 'clare-edited-1.jpg']),
        ('proposte-editoriali', ['losmuertos.jpeg', 'copertina-1.png', 'golden_thread.jpg',
                                  'owotg.jpg', 'otst.jpg', 'una_dacha.jpeg', 
                                  'image003.jpg', 'fentanyl.jpg']),
        ('biblioteca', ['biblioteca_cesena.jpg']),
    ]
    
    for cartella, immagini_attese in cartelle_con_immagini:
        cart_path = content_dir / cartella
        print(f"\n📁 {cartella}/")
        
        if not cart_path.exists():
            print(f"   ✗ CARTELLA NON ESISTE!")
            continue
        
        # Elenca tutte le immagini presenti
        imgs_presenti = [f.name for f in cart_path.glob('*') 
                        if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']]
        
        print(f"   Immagini presenti: {len(imgs_presenti)}")
        
        for img in immagini_attese:
            img_path = cart_path / img
            if img_path.exists():
                print(f"   ✓ {img}")
            else:
                print(f"   ✗ {img} - MANCANTE!")
    
    # 4. VERIFICA PDF IN PROPOSTE EDITORIALI
    print()
    print("=" * 70)
    print("4. VERIFICA PDF IN PROPOSTE-EDITORIALI")
    print("=" * 70)
    
    proposte_dir = content_dir / 'proposte-editoriali'
    pdf_attesi = [
        'los_muertos_y_el_periodista_scheda.pdf',
        'the-naked-dont-fear-the-water_scheda.pdf',
        'thegoldenthread_proposta_scheda.pdf',
        'owotg_proposta_scheda.pdf',
        'otst_scheda.pdf',
        'una_dacha_en_el_golfo_scheda.pdf',
        'we_are_bellingcat_proposta_scheda.pdf',
        'fentanyl_inc_proposta_scheda.pdf',
    ]
    
    if proposte_dir.exists():
        for pdf in pdf_attesi:
            pdf_path = proposte_dir / pdf
            if pdf_path.exists():
                print(f"✓ {pdf}")
            else:
                print(f"✗ {pdf} - MANCANTE!")
    else:
        print("✗ Cartella proposte-editoriali non esiste!")
    
    # 5. SOTTOSEZIONI BIBLIOTECA
    print()
    print("=" * 70)
    print("5. SOTTOSEZIONI BIBLIOTECA")
    print("=" * 70)
    
    sottosezioni = ['fiordafiore', 'nuoviarrivi', 'oldies', 'vecchieglorie']
    biblioteca_dir = content_dir / 'biblioteca'
    
    if biblioteca_dir.exists():
        for sez in sottosezioni:
            sez_dir = biblioteca_dir / sez
            if sez_dir.exists():
                index = sez_dir / '_index.md'
                post_count = len([f for f in sez_dir.iterdir() if f.is_dir()])
                if index.exists():
                    print(f"✓ {sez}/ - _index.md presente, {post_count} post")
                else:
                    print(f"⚠️  {sez}/ - _index.md MANCANTE, {post_count} post")
            else:
                print(f"✗ {sez}/ - CARTELLA NON ESISTE")
    
    # 6. RIEPILOGO PROBLEMI
    print()
    print("=" * 70)
    print("6. RIEPILOGO")
    print("=" * 70)
    
    problemi = []
    
    # Controlla contenuto pagine
    for nome, path in pagine.items():
        if path.exists():
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if len(content) < 100:
                problemi.append(f"{nome}: contenuto troppo corto")
    
    # Controlla immagini
    for cartella, immagini_attese in cartelle_con_immagini:
        cart_path = content_dir / cartella
        if cart_path.exists():
            for img in immagini_attese:
                if not (cart_path / img).exists():
                    problemi.append(f"Immagine mancante: {cartella}/{img}")
    
    if problemi:
        print(f"\n⚠️  PROBLEMI TROVATI: {len(problemi)}")
        for p in problemi:
            print(f"   - {p}")
    else:
        print("\n✓ Nessun problema evidente trovato!")
        print("\nSe il sito non funziona, il problema potrebbe essere:")
        print("   - Cache del browser (prova Ctrl+Shift+R)")
        print("   - Deploy non completato su Cloudflare")
        print("   - Configurazione tema Clarity")
    
    print()
    print("=" * 70)
    input("\nPremi INVIO per chiudere...")


if __name__ == '__main__':
    main()
