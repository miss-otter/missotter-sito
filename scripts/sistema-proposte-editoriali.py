#!/usr/bin/env python3
"""
SISTEMA PAGINA PROPOSTE EDITORIALI
Ricostruisce correttamente le immagini cliccabili che aprono i PDF
"""

from pathlib import Path

def main():
    print("=" * 60)
    print("SISTEMA PAGINA PROPOSTE EDITORIALI")
    print("=" * 60)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    proposte_dir = content_dir / 'proposte-editoriali'
    
    if not proposte_dir.exists():
        print("ERRORE: Cartella content/proposte-editoriali non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Contenuto corretto della pagina
    # Pattern: [![](immagine)](pdf) per immagine cliccabile
    contenuto = '''---
title: "Proposte editoriali"
---

Questa pagina raccoglie le mie più recenti proposte editoriali, clicca sulle copertine per visualizzarle e scaricarle. Se desideri prendere visione di altri materiali o valutare un saggio di traduzione, scrivimi all'indirizzo ale (.) neve [at] gmail (.) com.

---

[![](losmuertos.jpeg)](los_muertos_y_el_periodista_scheda.pdf)

Óscar Martínez, cronista salvadoregno, prende a pretesto una storia dolorosa per riflettere sul suo mestiere di giornalista in un contesto di estrema violenza civile.

---

[![](copertina-1.png)](the-naked-dont-fear-the-water_scheda.pdf)

Matthieu Aikins, giornalista e reporter di guerra, racconta il suo viaggio lungo una delle rotte della migrazione, da Kabul ad Atene, insieme a un gruppo di rifugiati afghani.

---

[![](golden_thread.jpg)](thegoldenthread_proposta_scheda.pdf)

Un libro affascinante ripercorre, sullo sfondo del Congo dei primi anni '60, la storia di un cold case illustre: la morte del segretario delle Nazioni Unite Dag Hammarskjold.

---

[![](owotg.jpg)](owotg_proposta_scheda.pdf)

Diciannove giornaliste arabe raccontano che cosa significa fare informazione sul campo nei loro paesi, spesso in contesti di guerra.

---

[![](otst.jpg)](otst_scheda.pdf)

Una giovane giornalista britannica ci guida in un viaggio avventuroso per più di 5.000 chilometri lungo le ferrovie del Myanmar e attraverso la storia del paese.

---

[![](una_dacha.jpeg)](una_dacha_en_el_golfo_scheda.pdf)

Un giornalista spagnolo che ha vissuto per due anni in Bahrein descrive con sguardo attento e a tratti ironico le mille contraddizioni del piccolo paese del Golfo.

---

[![](image003.jpg)](we_are_bellingcat_proposta_scheda.pdf)

Eliot Higgins, fondatore di Bellingcat, il celebre collettivo internazionale di ricercatori OSINT, investigatori e citizen journalist, ne racconta passato, presente e prospettive future.

---

[![](fentanyl.jpg)](fentanyl_inc_proposta_scheda.pdf)

Un'indagine approfondita sul mercato mondiale delle droghe sintetiche a partire dalla crisi degli oppioidi negli Stati Uniti.
'''
    
    # Scrivi il file
    index_file = proposte_dir / '_index.md'
    
    print(f"Scrivo: {index_file}")
    index_file.write_text(contenuto, encoding='utf-8')
    
    # Lista dei PDF necessari
    pdf_necessari = [
        'los_muertos_y_el_periodista_scheda.pdf',
        'the-naked-dont-fear-the-water_scheda.pdf',
        'thegoldenthread_proposta_scheda.pdf',
        'owotg_proposta_scheda.pdf',
        'otst_scheda.pdf',
        'una_dacha_en_el_golfo_scheda.pdf',
        'we_are_bellingcat_proposta_scheda.pdf',
        'fentanyl_inc_proposta_scheda.pdf',
    ]
    
    print()
    print("PDF NECESSARI nella cartella proposte-editoriali/:")
    print("-" * 50)
    
    for pdf in pdf_necessari:
        pdf_path = proposte_dir / pdf
        if pdf_path.exists():
            print(f"  ✓ {pdf}")
        else:
            print(f"  ✗ {pdf} (MANCANTE)")
    
    # Verifica anche le immagini
    immagini = [
        'losmuertos.jpeg',
        'copertina-1.png',
        'golden_thread.jpg',
        'owotg.jpg',
        'otst.jpg',
        'una_dacha.jpeg',
        'image003.jpg',
        'fentanyl.jpg',
    ]
    
    print()
    print("IMMAGINI nella cartella proposte-editoriali/:")
    print("-" * 50)
    
    for img in immagini:
        img_path = proposte_dir / img
        if img_path.exists():
            print(f"  ✓ {img}")
        else:
            print(f"  ✗ {img} (MANCANTE)")
    
    print()
    print("=" * 60)
    print("COMPLETATO!")
    print()
    print("Se ci sono PDF mancanti, devi estrarli dal file")
    print("media-export-49428766-from-0-to-1030.tar")
    print("e copiarli in content/proposte-editoriali/")
    print("=" * 60)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()
