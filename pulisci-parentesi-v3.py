#!/usr/bin/env python3
"""
PULISCI PARENTESI QUADRE ORFANE v3
Ricostruisce i blocchi di link spezzati:
- Prima riga diventa il titolo cliccabile
- Resto diventa testo normale con a capo
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
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Se la riga inizia con [ ma NON e' un link completo
        if stripped.startswith('[') and not ('](' in stripped and stripped.endswith(')')):
            # Potrebbe essere l'inizio di un blocco spezzato
            # Raccogli tutte le righe consecutive che iniziano con [
            block_lines = [stripped[1:]]  # prima riga senza [
            j = i + 1
            url = None
            
            while j < len(lines):
                next_line = lines[j].strip()
                
                if next_line.startswith('['):
                    # Controlla se questa e' l'ultima riga con ](url)
                    match = re.match(r'\[([^\]]*)\]\(([^)]+)\)', next_line)
                    if match:
                        # Trovato! Questa e' l'ultima riga del blocco
                        block_lines.append(match.group(1))  # testo senza [ e ](url)
                        url = match.group(2)
                        j += 1
                        break
                    else:
                        # Riga intermedia, aggiungi senza [
                        block_lines.append(next_line[1:])
                        j += 1
                else:
                    # Non inizia con [, fine del blocco
                    break
            
            if url and len(block_lines) > 1:
                # Abbiamo un blocco completo!
                # Prima riga = titolo linkato
                # Altre righe = testo con a capo
                title = block_lines[0]
                fixed_lines.append(f'[{title}]({url})  ')  # link + doppio spazio
                for info_line in block_lines[1:]:
                    fixed_lines.append(info_line + '  ')  # doppio spazio per a capo
                fixed_lines.append('')  # riga vuota dopo il blocco
                i = j
            else:
                # Non era un blocco valido, rimuovi solo la [
                fixed_lines.append(stripped[1:] + '  ')
                i += 1
        else:
            # Riga normale o link gia' valido
            fixed_lines.append(line)
            i += 1
    
    content = '\n'.join(fixed_lines)
    
    if content != original:
        # Backup
        backup = filepath.with_suffix('.md.bracket-bak')
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
    print("PULISCI PARENTESI QUADRE - v3")
    print("(Ricostruisce link spezzati)")
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
    print("=" * 50)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
