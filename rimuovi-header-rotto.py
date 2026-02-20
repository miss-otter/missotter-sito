#!/usr/bin/env python3
"""
RIMUOVI HEADER ROTTO - Versione diretta
"""

from pathlib import Path
import os

def main():
    print("=" * 60)
    print("RIMUOVI HEADER.HTML ROTTO")
    print("=" * 60)
    print()
    
    # Trova la cartella del sito
    script_dir = Path(__file__).parent.absolute()
    
    # Possibili posizioni del file
    possibili = [
        script_dir / 'layouts' / 'partials' / 'header.html',
        script_dir / 'layouts' / 'partials' / 'header.html.bak',
    ]
    
    trovato = False
    for filepath in possibili:
        if filepath.exists():
            print(f"TROVATO: {filepath}")
            
            # Rinomina invece di cancellare (più sicuro)
            nuovo_nome = filepath.with_suffix('.html.RIMOSSO')
            filepath.rename(nuovo_nome)
            print(f"  → Rinominato in: {nuovo_nome.name}")
            trovato = True
    
    # Cerca anche ricorsivamente
    layouts_dir = script_dir / 'layouts'
    if layouts_dir.exists():
        for f in layouts_dir.rglob('header.html'):
            print(f"TROVATO: {f}")
            nuovo_nome = f.with_suffix('.html.RIMOSSO')
            f.rename(nuovo_nome)
            print(f"  → Rinominato in: {nuovo_nome.name}")
            trovato = True
    
    print()
    if trovato:
        print("✅ File rimosso/rinominato!")
        print()
        print("ORA FAI:")
        print("1. Apri GitHub Desktop")
        print("2. Vedrai i file modificati")
        print("3. Scrivi un messaggio: 'Rimuovo header rotto'")
        print("4. Clicca 'Commit to main'")
        print("5. Clicca 'Push origin'")
        print()
        print("Aspetta 1-2 minuti e ricarica il sito.")
    else:
        print("❌ File header.html NON trovato in layouts/partials/")
        print()
        print("Il problema potrebbe essere:")
        print("- Non hai ancora fatto push dopo l'ultimo script")
        print("- Il file è in una posizione diversa")
        print()
        print("Controlla GitHub Desktop - ci sono modifiche da pushare?")
    
    print()
    print("=" * 60)
    input("Premi INVIO per chiudere...")

if __name__ == '__main__':
    main()
