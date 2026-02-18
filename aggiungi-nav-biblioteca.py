#!/usr/bin/env python3
"""
AGGIUNGI NAVIGAZIONE SOTTOSEZIONI BIBLIOTECA
Inserisce un menu di navigazione in ogni sottosezione
"""

from pathlib import Path

# Blocco navigazione HTML da inserire
NAV_BLOCK = '''
<div class="nav-sottosezioni">
  <a href="/biblioteca/nuoviarrivi/">Nuovi Arrivi</a>
  <a href="/biblioteca/vecchieglorie/">Vecchie Glorie</a>
  <a href="/biblioteca/fiordafiore/">Fior da Fiore</a>
  <a href="/biblioteca/oldies/">Oldies</a>
</div>

'''

def fix_sottosezione(filepath, nome_sezione):
    """Aggiunge navigazione al file _index.md"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Controlla se la navigazione è già presente
    if 'nav-sottosezioni' in content:
        print(f"  {nome_sezione}: navigazione già presente")
        return False
    
    # Trova la fine del frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # Inserisci la navigazione all'inizio del body
            new_content = f'---{frontmatter}---\n{NAV_BLOCK}{body.lstrip()}'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✓ {nome_sezione}: navigazione aggiunta")
            return True
    
    print(f"  ✗ {nome_sezione}: errore nel parsing")
    return False

def main():
    print("=" * 60)
    print("AGGIUNGI NAVIGAZIONE SOTTOSEZIONI BIBLIOTECA")
    print("=" * 60)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    biblioteca_dir = content_dir / 'biblioteca'
    
    if not biblioteca_dir.exists():
        print("ERRORE: Cartella 'content/biblioteca' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    sottosezioni = {
        'fiordafiore': 'Fior da Fiore',
        'nuoviarrivi': 'Nuovi Arrivi',
        'oldies': 'Oldies',
        'vecchieglorie': 'Vecchie Glorie',
    }
    
    modificate = 0
    
    for slug, nome in sottosezioni.items():
        index_file = biblioteca_dir / slug / '_index.md'
        if index_file.exists():
            if fix_sottosezione(index_file, nome):
                modificate += 1
        else:
            print(f"  ✗ {nome}: file _index.md non trovato")
    
    print()
    print("=" * 60)
    print(f"COMPLETATO! Modificate {modificate} sottosezioni.")
    print()
    print("IMPORTANTE: Aggiungi anche il CSS al tuo custom.css!")
    print("(vedi file aggiunte-css.txt)")
    print()
    print("Poi fai commit e push con GitHub Desktop")
    print("=" * 60)
    input("\nPremi INVIO per chiudere...")


if __name__ == '__main__':
    main()
