#!/usr/bin/env python3
"""
SISTEMA TUTTE LE PAGINE
Ricostruisce correttamente tutte le pagine del sito Hugo
"""

from pathlib import Path

def sistema_home(content_dir):
    """Sistema la homepage"""
    contenuto = '''---
title: "La biblioteca di Miss Otter"
---

La biblioteca di Miss Otter è una raccolta di recensioni, un resoconto di viaggio, un percorso di esplorazione di quella realtà proteiforme che per comodità chiamerò la *narrazione del reale*, in tutte le sue varianti e declinazioni. Ho provato a spiegarlo un po' meglio [qui](/biblioteca/).

---

## Le sezioni

### [Nuovi Arrivi](/biblioteca/nuoviarrivi/)

Nuoviarrivi è la sezione dedicata alle novità o alle letture recenti che meritano una segnalazione. Tenetela d'occhio!

### [Vecchie Glorie](/biblioteca/vecchieglorie/)

Vecchieglorie è la sezione dedicata ai classici, testi che hanno contribuito a definire la natura stessa del genere.

### [Fior da Fiore](/biblioteca/fiordafiore/)

Fiordafiore è la sezione dedicata alle segnalazioni varie. Vi parlerò di articoli, longform, podcast o documentari degni di nota.

### [Oldies](/biblioteca/oldies/)

Oldies raccoglie i post più vecchi del blog, quelli degli inizi.

---

L'immagine che ho scelto come intestazione di questo sito è una mia fotografia della biblioteca malatestiana antica di Cesena, l'unico esempio al mondo di biblioteca umanistica di cui si sono perfettamente e fortunosamente conservati, a dispetto di tutto, l'edificio, gli arredi e la dotazione libraria. Un posto magico, assolutamente straordinario e visitabile.
'''
    index_file = content_dir / '_index.md'
    index_file.write_text(contenuto, encoding='utf-8')
    return "content/_index.md"


def sistema_chi_sono(content_dir):
    """Sistema la pagina Chi sono"""
    chi_sono_dir = content_dir / 'chi-sono'
    chi_sono_dir.mkdir(parents=True, exist_ok=True)
    
    contenuto = '''---
title: "Chi sono"
---

Mi chiamo Alessandra Neve, sono una traduttrice e lavoro con tre lingue: inglese, francese e spagnolo.

Traduco in prevalenza giornalismo e saggi, meno spesso ma molto volentieri faccio traduzioni per il doppiaggio. Quando non lavoro mi dedico alle letture, alle visioni e agli ascolti che stanno alla base delle mie segnalazioni. Porto avanti con costanza anche un'attività di scouting, proponendo agli editori testi di giornalismo che credo valga la pena di far conoscere al pubblico italiano.

Ritengo che l'infinita varietà della realtà che ci circonda superi di slancio (nel bene e nel male, purtroppo) ogni fantasia e ogni sforzo dell'immaginazione. Non finisco mai di stupirmi e di gioire quando un libro, un articolo, un podcast o un documentario mi rivelano lo sguardo indagatore di un autore che con dedizione, magari con un lavoro di anni, si è impegnato a tentare di comprendere, di interpretare e di spiegare agli altri qualche aspetto di questo formidabile mondo in cui viviamo.

"Miss Otter" è uno pseudonimo giocoso nato assieme al blog diversi anni fa, in onore di un animale da me molto amato, la lontra. Le ragioni di questo amore, per i più curiosi, le ho raccontate [in questo post](/biblioteca/oldies/how-it-all-began-1-una-strana-coincidenza/) e [in questo](/biblioteca/oldies/how-it-all-began-2-le-americane-e-lo-scozzese/).

I post sono aperti ai commenti, ma se volete scrivermi in privato per segnalare qualche testo/documentario/podcast interessante, discutere di qualcosa, o magari affidarmi una traduzione, c'è un indirizzo email a vostra disposizione:

**missotter (at) outlook (punto) com**

Sono (ero?) anche moderatamente attiva su Twitter, dove il mio handle è @laleneve.

[Una pagina di questo blog](/traduzioni/) raccoglie i rimandi ad alcune mie traduzioni pubblicate online. Se volete farvi un'idea di come traduco, siete i benvenuti.
'''
    index_file = chi_sono_dir / '_index.md'
    index_file.write_text(contenuto, encoding='utf-8')
    return "content/chi-sono/_index.md"


def sistema_biblioteca(content_dir):
    """Sistema la pagina La biblioteca"""
    biblioteca_dir = content_dir / 'biblioteca'
    biblioteca_dir.mkdir(parents=True, exist_ok=True)
    
    contenuto = '''---
title: "La biblioteca"
---

![](biblioteca_cesena.jpg)

Questa esplorazione, questo viaggio nella parola scritta (ma non solo scritta, lo vedremo) parte da me, dai libri che ho amato in diverse epoche della mia vita e dalle ragioni per cui li ho amati, e si estende a cercare di afferrare la natura sfuggente della categoria, o forse meglio sovracategoria, della *narrazione del reale*.

Un contenitore con molti nomi (in ambito anglosassone "creative nonfiction", "literary nonfiction", "narrative nonfiction" o ancora "verfabula"; in Italia spesso "nonfiction" tout court) contenuti estremamente vari, pochi confini e poche certezze. Ma ai curiosi e agli eclettici può piacere anche così.

Leggevo di recente Paolo Cognetti, in un vecchio post del suo defunto blog, che si interrogava, un paio d'anni dopo l'uscita di *Gomorra* e dal punto di vista di un autore di narrativa, sulla natura di questa "nuova" narrativa del reale, senza riuscire ad afferrare cosa fosse esattamente, associandola ad altri fenomeni in crescita come i reality show o le docufiction e usando aggettivi a mio parere fuori fuoco, come "sinistro", "pericoloso", "disonesto".

Ecco, già che ci siamo, *Gomorra*. Nel lungo, estenuante dibattito nazionale seguito alla pubblicazione, del libro di Saviano si è detto tutto e il contrario di tutto; un saggio di Simone Del Latte ne descrive la genesi in casa editrice come l'idea di creare "un'opera che se la giocasse a cavallo tra fiction e non-fiction". Il risultato è un libro importante nella storia della nostra cultura (più per il suo valore civile che per quello artistico) ma immaturo dal punto di vista del giornalismo narrativo, complici probabilmente la giovane età dell'autore e la poca dimestichezza dell'editor che lo ha seguito con questo genere.

Ma torniamo a noi e cerchiamo di capire cosa comprende questo genere. Una definizione molto ampia potrebbe essere "un genere di scrittura che applica le tecniche della narrativa a fatti realmente accaduti, argomenti che potrebbero trovare spazio in un giornale o in un libro di testo scolastico". Quando dà il meglio di sé combina la raffinatezza tecnica di un romanzo ben costruito con la rigorosa verifica delle informazioni tipica del giornalismo.

Al suo interno trovano spazio molte cose diverse, provo a elencarle:

- **i memoir o autobiografie.** Un esempio per tutti: *L'anno del pensiero magico* di Joan Didion, per citare da subito una protagonista del new journalism americano.

- **le biografie.** Qui, fra i tanti esempi possibili, mi viene subito da sfoderare un altro asso: *Limonov* di Carrère.

- **il giornalismo narrativo.** C'è l'imbarazzo della scelta, faccio solo qualche nome: Gay Talese, Rodolfo Walsh, Philip Gourevitch, William Langewiesche, Lawrence Wright, Martín Caparrós.

- **il reportage d'autore,** quando in un ribaltamento di ruoli è lo scrittore a decidere di cimentarsi con il reale, come nel caso di David Foster Wallace che, su incarico della rivista Harper's, parte per una crociera ai Caraibi e ci regala *Una cosa divertente che non farò mai più*, oppure come nel nitido *Underground* di Haruki Murakami.

- **certe cronache di viaggio,** come *Ebano* di Kapuscinski.

- **saggi di giornalismo scientifico,** come per esempio i libri di Michael Pollan pubblicati da Adelphi.

- **opere "true crime",** fra cui non si può non citare *A sangue freddo* di Capote, capostipite del genere, oppure *Un estraneo al mio fianco*, l'incredibile libro di Ann Rule su Ted Bundy. Qui aggiungo volentieri un'opera italiana, recente e molto bella: *La città dei vivi* di Nicola Lagioia.

- **per chiudere la panoramica con una nota lievemente trasgressiva,** merita una menzione anche il gonzo journalism, il cui testo di culto è senza dubbio *Paura e disgusto a Las Vegas* di Hunter S. Thompson.

Mi rendo conto che è un panorama molto vasto, se si aggiunge poi che io amo molto anche il giornalismo investigativo (le cui imprese tuttavia, quando si trasformano in libri, sono spesso meno stilisticamente rifinite), i reportage lunghi, i podcast e i documentari, c'è l'imbarazzo della scelta.

Ebbene, quello che mi propongo è di guidarvi o, forse meglio, di farmi accompagnare in questa esplorazione, articolata in:

- una rassegna dei grandi classici del genere (nella sezione **[Vecchie Glorie](/biblioteca/vecchieglorie/)**)
- una raccolta di recensioni delle mie scoperte recenti (nella sezione **[Nuovi Arrivi](/biblioteca/nuoviarrivi/)**)
- qualche gustosa digressione su articoli, podcast o documentari particolarmente interessanti (nella sezione **[Fior da Fiore](/biblioteca/fiordafiore/)**)

Va da sé che ogni contributo alla riflessione o suggerimento di nuovi spunti di lettura sarà accolto con entusiasmo e gratitudine.

---

Chiudo in bellezza con una citazione da uno splendido saggio di Leila Guerriero sul "giornalismo narrativo, le sue origini e le sue ragioni", pubblicato originariamente su Revista Anfibia e tradotto e ospitato dal blog delle edizioni SUR, che vi consiglio caldamente di leggere:

> "Il giornalismo narrativo è un mestiere modesto, praticato da individui abbastanza umili da sapere che non potranno mai comprendere il mondo, abbastanza testardi da perseverare nei propri obiettivi, e abbastanza superbi da credere che questi obiettivi interessino a tutti."
'''
    index_file = biblioteca_dir / '_index.md'
    index_file.write_text(contenuto, encoding='utf-8')
    return "content/biblioteca/_index.md"


def sistema_traduzioni(content_dir):
    """Sistema la pagina Traduzioni"""
    traduzioni_dir = content_dir / 'traduzioni'
    traduzioni_dir.mkdir(parents=True, exist_ok=True)
    
    contenuto = '''---
title: "Traduzioni"
---

Prosegue la mia collaborazione con il progetto di blog collettivo *Assaggi* di nonfiction.it. I testi che seleziono per il progetto sono spesso articoli, racconti o estratti delle opere recensite in questo spazio, i cui autori mi hanno gentilmente concesso di tradurre e pubblicare un loro scritto inedito in Italia. Per chi volesse farsi un'idea di come traduco, *Assaggi* è il posto giusto. I link sono qui, sotto le fotografie degli autori.

---

![](darren_byler-edited-2.png)

**Darren Byler**

**[La storia di Vera](https://nonfiction.it/assaggi/la-storia-di-vera/)**

Una studentessa dell'Università di Washington, originaria dello Xinjiang, invischiata nelle maglie della sorveglianza cinese.

---

![](ravi_somaiya-edited.jpg)

**Ravi Somaiya**

**[Il complotto africano](https://nonfiction.it/assaggi/il-complotto-africano/)**

Sono stati i bianchi europei, guidati da un fantomatico "mister X", a uccidere sessant'anni fa in Congo il segretario generale delle Nazioni Unite per mantenere il potere sui neri africani?

---

![](emiliosanchezmediavilla-edited.jpeg)

**Emilio Sánchez Mediavilla**

**[Beirut non esiste più](https://nonfiction.it/assaggi/beirut-non-esiste-piu/)**

Una passeggiata per le strade e fra la gente di Beirut nella primavera del 2016, per assaggiare, osservare e ascoltare le molte contraddizioni di una città complessa e tormentata.

---

![](zahra_hankir-edited.jpg)

**Zahra Hankir**

**[Il re del Ful](https://nonfiction.it/assaggi/il-re-del-ful/)**

Lo stufato di fave è il protagonista indiscusso di questo viaggio nella gastronomia, nelle tradizioni e nella storia del Libano meridionale.

---

![](altman_headshot-edited.jpeg)

**Rebecca Altman**

**[Sul vinile](https://nonfiction.it/assaggi/sul-vinile/)**

Un saggio storico sulla produzione della plastica per capire le ragioni del disastro ferroviario di East Palestine e sensibilizzare sui rischi per la salute umana e ambientale.

---

![](clare-edited-1.jpg)

**Clare Hammond**

**[Lungo i binari delle ferrovie fantasma](https://nonfiction.it/assaggi/lungo-i-binari-delle-ferrovie-fantasma/)**

Un estratto da "On the Shadow Tracks", il viaggio-inchiesta di Clare Hammond lungo le ferrovie birmane.
'''
    index_file = traduzioni_dir / '_index.md'
    index_file.write_text(contenuto, encoding='utf-8')
    return "content/traduzioni/_index.md"


def sistema_proposte(content_dir):
    """Sistema la pagina Proposte editoriali"""
    proposte_dir = content_dir / 'proposte-editoriali'
    proposte_dir.mkdir(parents=True, exist_ok=True)
    
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
    index_file = proposte_dir / '_index.md'
    index_file.write_text(contenuto, encoding='utf-8')
    return "content/proposte-editoriali/_index.md"


def sistema_sottosezioni_biblioteca(content_dir):
    """Crea gli _index.md per le sottosezioni di biblioteca"""
    sottosezioni = {
        'fiordafiore': 'Fior da Fiore',
        'nuoviarrivi': 'Nuovi Arrivi',
        'oldies': 'Oldies',
        'vecchieglorie': 'Vecchie Glorie',
    }
    
    creati = []
    for slug, titolo in sottosezioni.items():
        sez_dir = content_dir / 'biblioteca' / slug
        if sez_dir.exists():
            index_file = sez_dir / '_index.md'
            if not index_file.exists():
                contenuto = f'''---
title: "{titolo}"
---
'''
                index_file.write_text(contenuto, encoding='utf-8')
                creati.append(f"content/biblioteca/{slug}/_index.md")
    
    return creati


def verifica_file(content_dir):
    """Verifica i file necessari"""
    problemi = []
    
    # Immagini per biblioteca
    img = content_dir / 'biblioteca' / 'biblioteca_cesena.jpg'
    if not img.exists():
        problemi.append("biblioteca/biblioteca_cesena.jpg")
    
    # Immagini per traduzioni
    traduzioni_imgs = [
        'darren_byler-edited-2.png', 'ravi_somaiya-edited.jpg',
        'emiliosanchezmediavilla-edited.jpeg', 'zahra_hankir-edited.jpg',
        'altman_headshot-edited.jpeg', 'clare-edited-1.jpg',
    ]
    for img_name in traduzioni_imgs:
        img = content_dir / 'traduzioni' / img_name
        if not img.exists():
            problemi.append(f"traduzioni/{img_name}")
    
    # Immagini e PDF per proposte
    proposte_files = [
        'losmuertos.jpeg', 'copertina-1.png', 'golden_thread.jpg',
        'owotg.jpg', 'otst.jpg', 'una_dacha.jpeg', 'image003.jpg', 'fentanyl.jpg',
        'los_muertos_y_el_periodista_scheda.pdf', 'the-naked-dont-fear-the-water_scheda.pdf',
        'thegoldenthread_proposta_scheda.pdf', 'owotg_proposta_scheda.pdf',
        'otst_scheda.pdf', 'una_dacha_en_el_golfo_scheda.pdf',
        'we_are_bellingcat_proposta_scheda.pdf', 'fentanyl_inc_proposta_scheda.pdf',
    ]
    for f_name in proposte_files:
        f = content_dir / 'proposte-editoriali' / f_name
        if not f.exists():
            problemi.append(f"proposte-editoriali/{f_name}")
    
    return problemi


def main():
    print("=" * 70)
    print("SISTEMA TUTTE LE PAGINE")
    print("=" * 70)
    print()
    
    script_dir = Path(__file__).parent.absolute()
    content_dir = script_dir / 'content'
    
    if not content_dir.exists():
        print("ERRORE: Cartella 'content' non trovata!")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"Cartella: {content_dir}")
    print()
    
    # Sistema le pagine
    print("Sistemo le pagine...")
    print("-" * 50)
    
    creati = []
    creati.append(sistema_home(content_dir))
    print(f"  ✓ Homepage")
    
    creati.append(sistema_chi_sono(content_dir))
    print(f"  ✓ Chi sono")
    
    creati.append(sistema_biblioteca(content_dir))
    print(f"  ✓ La biblioteca")
    
    creati.append(sistema_traduzioni(content_dir))
    print(f"  ✓ Traduzioni")
    
    creati.append(sistema_proposte(content_dir))
    print(f"  ✓ Proposte editoriali")
    
    sottosezioni = sistema_sottosezioni_biblioteca(content_dir)
    for s in sottosezioni:
        print(f"  ✓ {s}")
        creati.append(s)
    
    print()
    print("=" * 70)
    print(f"FILE CREATI/AGGIORNATI: {len(creati)}")
    print("=" * 70)
    
    # Verifica file mancanti
    print()
    print("Verifico file necessari...")
    print("-" * 50)
    
    problemi = verifica_file(content_dir)
    
    if problemi:
        print(f"\n⚠️  FILE MANCANTI ({len(problemi)}):")
        for p in problemi:
            print(f"  ✗ {p}")
        print()
        print("Devi copiare questi file dalle cartelle")
        print("dove li hai scaricati da WordPress.")
    else:
        print("  ✓ Tutti i file necessari sono presenti!")
    
    print()
    print("=" * 70)
    print("COMPLETATO!")
    print()
    print("Ora fai commit e push con GitHub Desktop")
    print("=" * 70)
    input("\nPremi INVIO per chiudere...")


if __name__ == '__main__':
    main()
