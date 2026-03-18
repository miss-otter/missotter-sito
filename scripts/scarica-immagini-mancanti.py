#!/usr/bin/env python3
"""
SCARICA IMMAGINI MANCANTI
Scarica le 49 immagini mancanti da WordPress nelle cartelle corrette
"""

import os
import urllib.request
import ssl
import time
from pathlib import Path

# Mappa: cartella destinazione -> lista di (nome_file, url)
IMMAGINI = {
    'content/biblioteca/oldies/a-day-at-the-radio-ovvero-nel-cuore-dell-alaska': [
        ('pic1.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/10/pic1.jpg'),
        ('pic2.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/10/pic2.jpg'),
        ('pic3.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/10/pic3.jpg'),
        ('pic4.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/10/pic4.jpg'),
        ('pic5.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/10/pic5.jpg'),
        ('pic6.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/10/pic6.jpg'),
    ],
    'content/biblioteca/oldies/gerusalemme-2': [
        ('wpid-foto-3_2-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-3_2-jpg.jpeg'),
        ('wpid-foto-4-jpg2.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-4-jpg2.jpeg'),
    ],
    'content/biblioteca/oldies/gerusalemme-3-ma-in-verita-e-betlemme': [
        ('wpid-foto.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto.jpg'),
        ('wpid-foto-1.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-1.jpg'),
        ('wpid-foto-2-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-2-jpg.jpeg'),
        ('wpid-foto-3_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-3_1-jpg.jpeg'),
        ('wpid-foto-1-1_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-1-1_1-jpg.jpeg'),
        ('wpid-foto-5_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-5_1-jpg.jpeg'),
        ('wpid-foto-3-1_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-3-1_1-jpg.jpeg'),
        ('wpid-foto-5-1_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-5-1_1-jpg.jpeg'),
        ('wpid-foto-1-2_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-1-2_1-jpg.jpeg'),
        ('wpid-foto-4-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-4-jpg.jpeg'),
    ],
    'content/biblioteca/oldies/gerusalemme-4': [
        ('wpid-foto-1_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-1_1-jpg.jpeg'),
        ('wpid-foto-2_1-jpg.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2015/05/wpid-foto-2_1-jpg.jpeg'),
    ],
    'content/biblioteca/oldies/how-it-all-began-1-una-strana-coincidenza': [
        ('pink-floyd-piper-at-the-gates-of-dawn-front.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/pink-floyd-piper-at-the-gates-of-dawn-front.jpg'),
        ('thewindinthewillows.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/thewindinthewillows.jpg'),
        ('ilventoneisalici.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/ilventoneisalici.jpg'),
        ('dscf5167.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/dscf5167.jpg'),
    ],
    'content/biblioteca/oldies/how-it-all-began-2-le-americane-e-lo-scozzese': [
        ('otter-rosa.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/otter-rosa.jpg'),
        ('otter-kit.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/otter-kit.jpg'),
        ('otter-ivy.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/otter-ivy.jpg'),
        ('otter-gidget.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/otter-gidget.jpg'),
        ('otter-abby.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/otter-abby.jpg'),
        ('ring_bright_water.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/ring_bright_water.jpg'),
        ('maxwell_gavin_edal.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2013/05/maxwell_gavin_edal.jpg'),
    ],
    'content/pages/home': [
        ('img_4597.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2020/09/img_4597.jpg'),
        ('img_4579.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2020/09/img_4579.jpg'),
        ('5-img_0668.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2020/09/5-img_0668.jpg'),
    ],
    'content/pages/la-biblioteca': [
        ('biblioteca_cesena.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2020/09/biblioteca_cesena.jpg'),
    ],
    'content/pages/proposte-editoriali': [
        ('losmuertos.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2022/12/losmuertos.jpeg'),
        ('copertina-1.png', 'https://missotter.wordpress.com/wp-content/uploads/2022/03/copertina-1.png'),
        ('golden_thread.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2021/12/golden_thread.jpg'),
        ('owotg.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2021/12/owotg.jpg'),
        ('otst.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2024/12/otst.jpg'),
        ('una_dacha.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2022/12/una_dacha.jpeg'),
        ('image003.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2021/12/image003.jpg'),
        ('fentanyl.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2020/10/fentanyl.jpg'),
    ],
    'content/pages/traduzioni': [
        ('darren_byler-edited-2.png', 'https://missotter.wordpress.com/wp-content/uploads/2023/12/darren_byler-edited-2.png'),
        ('ravi_somaiya-edited.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2023/12/ravi_somaiya-edited.jpg'),
        ('emiliosanchezmediavilla-edited.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2023/12/emiliosanchezmediavilla-edited.jpeg'),
        ('zahra_hankir-edited.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2023/12/zahra_hankir-edited.jpg'),
        ('altman_headshot-edited.jpeg', 'https://missotter.wordpress.com/wp-content/uploads/2023/12/altman_headshot-edited.jpeg'),
        ('clare-edited-1.jpg', 'https://missotter.wordpress.com/wp-content/uploads/2025/04/clare-edited-1.jpg'),
    ],
}

def download_image(url, dest_path):
    """Scarica un'immagine."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        request = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(request, context=ctx, timeout=30) as response:
            with open(dest_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"    ERRORE: {str(e)[:50]}")
        return False

def main():
    print("=" * 60)
    print("SCARICA IMMAGINI MANCANTI DA WORDPRESS")
    print("=" * 60)
    print()
    
    # Trova la cartella del sito
    script_dir = Path(__file__).parent.absolute()
    
    # Verifica che content esista
    if not (script_dir / 'content').exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"Cartella sito: {script_dir}")
    print()
    
    total = sum(len(imgs) for imgs in IMMAGINI.values())
    print(f"Immagini da scaricare: {total}")
    print()
    
    downloaded = 0
    failed = 0
    
    for folder, images in IMMAGINI.items():
        folder_path = script_dir / folder
        
        # Verifica che la cartella esista
        if not folder_path.exists():
            print(f"ATTENZIONE: Cartella non trovata: {folder}")
            print(f"  Creo la cartella...")
            folder_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{folder}/")
        
        for filename, url in images:
            dest_path = folder_path / filename
            
            # Salta se esiste gia
            if dest_path.exists():
                print(f"  {filename} - gia presente")
                downloaded += 1
                continue
            
            print(f"  {filename}...", end=' ')
            
            if download_image(url, dest_path):
                print("OK")
                downloaded += 1
            else:
                failed += 1
            
            time.sleep(0.3)  # Pausa tra download
    
    print()
    print("=" * 60)
    print(f"COMPLETATO!")
    print(f"  Scaricate: {downloaded}")
    print(f"  Fallite: {failed}")
    print()
    print("Ora fai commit e push con GitHub Desktop")
    print("=" * 60)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
