#!/usr/bin/env python3
"""
CORREGGI FRONTMATTER PAGINE
Aggiunge layout: single alle pagine che devono mostrare contenuto
invece di liste di post
"""

from pathlib import Path
import re

def fix_frontmatter(filepath, add_layout=True):
    """Aggiunge layout: single al frontmatter se mancante"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Controlla se ha già layout nel frontmatter
    if 'layout:' in content:
        print(f"  {filepath.name}: layout già presente")
        return False
    
    # Trova il frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        print(f"  {filepath.name}: frontmatter non trovato!")
        return False
    
    frontmatter = match.group(1)
    
    # Aggiungi layout: single
    if add_layout:
        new_frontmatter = frontmatter + '\nlayout: "single"'
        new_content = content.replace(f'---\n{frontmatter}\n---', f'---\n{new_frontmatter}\n---', 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ {filepath.name}: aggiunto layout: single")
        return True
    
    return False

def main():
    print("=" * 60)
    print("CORREGGI FRONTMATTER PAGINE")
    print("=" * 60)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Pagine che devono mostrare CONTENUTO (non liste)
    # Queste hanno bisogno di layout: single
    pagine_contenuto = [
        content_dir / '_index.md',                    # Homepage
        content_dir / 'chi-sono' / '_index.md',       # Chi sono
        content_dir / 'traduzioni' / '_index.md',    # Traduzioni
        content_dir / 'proposte-editoriali' / '_index.md',  # Proposte
        content_dir / 'biblioteca' / '_index.md',    # La biblioteca (testo introduttivo)
    ]
    
    # Pagine che devono mostrare LISTE (non serve layout: single)
    # Le sottosezioni di biblioteca mostrano la lista dei post
    pagine_lista = [
        content_dir / 'biblioteca' / 'fiordafiore' / '_index.md',
        content_dir / 'biblioteca' / 'nuoviarrivi' / '_index.md',
        content_dir / 'biblioteca' / 'oldies' / '_index.md',
        content_dir / 'biblioteca' / 'vecchieglorie' / '_index.md',
        content_dir / 'breadcrumbs' / '_index.md',
        content_dir / 'tutto' / '_index.md',
    ]
    
    print("Pagine che mostrano CONTENUTO (aggiungo layout: single):")
    print("-" * 60)
    
    modificate = 0
    for pagina in pagine_contenuto:
        if pagina.exists():
            if fix_frontmatter(pagina, add_layout=True):
                modificate += 1
        else:
            print(f"  ✗ {pagina.relative_to(content_dir)}: file non esiste")
    
    print()
    print("Pagine che mostrano LISTE (lascio invariate):")
    print("-" * 60)
    for pagina in pagine_lista:
        if pagina.exists():
            print(f"  - {pagina.relative_to(content_dir)}")
        else:
            print(f"  ✗ {pagina.relative_to(content_dir)}: file non esiste")
    
    print()
    print("=" * 60)
    print(f"COMPLETATO! Modificate {modificate} pagine.")
    print()
    print("Ora fai commit e push con GitHub Desktop")
    print("=" * 60)
    input("\nPremi INVIO per chiudere...")


if __name__ == '__main__':
    main()
