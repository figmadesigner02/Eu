# -*- coding: utf-8 -*-
"""Genera lo script video "Lezione 1 · Cos'è il job shadowing Erasmus+" (PDF + teleprompter .txt).

Uso:  python3 build_script.py
I timecode sono calcolati dalla lunghezza del parlato (~145 parole/minuto).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "guida-job-shadowing"))

from build_pdf import (BLUE, CORAL, GREEN, GREY, INK, LIGHT, NAVY, ORANGE,  # noqa: E402
                       PURPLE, TEAL, YELLOW, HRule, S, bullets, callout, table)
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame,  # noqa: E402
                                KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle  # noqa: E402

PDF = os.path.join(HERE, "Script_Video_Lezione1_Job_Shadowing.pdf")
TXT = os.path.join(HERE, "Teleprompter_Lezione1_Job_Shadowing.txt")
WPM = 145

S["voice"] = ParagraphStyle("voice", parent=S["body"], fontSize=10, leading=14.5, spaceAfter=0)
S["screen"] = ParagraphStyle("screen", parent=S["body"], fontSize=8.2, leading=11, textColor=GREY, spaceAfter=0)


def P(t, st="body"):
    return Paragraph(t, S[st])


# =============================================================== SCENE
# Ogni scena: (titolo, colore, [(a_schermo, voce), ...])
SCENES = [
    ("Apertura", CORAL, [
        ("Primo piano in camera, luce naturale, ripresa grezza (niente intro animata). "
         "Testo in sovrimpressione: <b>«Una settimana dentro un'organizzazione all'estero»</b>.",
         "Immagina di passare una settimana dentro un'organizzazione in un altro Paese europeo. Non in aula, "
         "e nemmeno da turista: dentro. Ti siedi accanto ai colleghi, guardi come lavorano, fai domande, e ti "
         "porti a casa metodi che da noi quasi nessuno usa. Viaggio e soggiorno sono coperti da un contributo "
         "dell'Unione Europea."),
        ("Taglio secco. Titolo grande: <b>JOB SHADOWING</b>.",
         "Si chiama job shadowing. È una delle attività di Erasmus+ meno conosciute, e quando ne parli la prima "
         "reazione è quasi sempre: «ma esiste davvero?». Esiste. Però ha regole precise, e chi non le conosce "
         "perde mesi."),
        ("Grafica G1: indice dei capitoli che scorre.",
         "In questa lezione te le do tutte, dall'inizio: cos'è, chi può farlo, chi paga, come si trova "
         "l'organizzazione che ti ospita e come si costruisce, giorno per giorno. In fondo trovi gli errori più "
         "comuni, così li eviti prima ancora di cominciare."),
    ]),
    ("Cos'è, in una frase", BLUE, [
        ("Grafica G2: la parola <b>shadow = ombra</b>, una sagoma che segue un professionista.",
         "Partiamo dalla parola. Shadow vuol dire ombra. Fare job shadowing significa fare da ombra a un "
         "professionista: lo segui mentre lavora, osservi, lo affianchi. Non sei lì per produrre, sei lì per "
         "imparare."),
        ("Box definizione: <b>Mobilità dello staff · Azione chiave 1 (KA1) di Erasmus+</b>.",
         "Dentro Erasmus+ il job shadowing è un'attività di mobilità dello staff, nell'Azione chiave 1. Tradotto: "
         "è pensato per chi lavora in un'organizzazione, cioè docenti, formatori, educatori, operatori, chi "
         "gestisce i progetti. Serve a far crescere queste persone e, attraverso di loro, l'organizzazione "
         "intera."),
        ("Testo: <b>Regola n. 1 · Non è un viaggio premio</b>.",
         "Prima regola, da tenere a mente per tutto il corso: il job shadowing non è un viaggio premio. Ha "
         "obiettivi di apprendimento, un programma, e un risultato atteso: tornare e cambiare qualcosa nel modo "
         "in cui lavori."),
    ]),
    ("Tre attività da non confondere", TEAL, [
        ("Grafica G3: tabella a tre colonne che si riempie una colonna alla volta.",
         "Nella mobilità dello staff ci sono tre attività che spesso si confondono. Mettiamole una accanto "
         "all'altra."),
        ("Colonna 1: <b>Job shadowing · 2–60 giorni (+ viaggio)</b>.",
         "Uno: il job shadowing. Osservi e affianchi i colleghi dell'organizzazione ospitante. Dura da due a "
         "sessanta giorni, più i giorni di viaggio."),
        ("Colonna 2: <b>Incarico di insegnamento / formazione</b>. Nota: «durata: vedi Guida dell'anno».",
         "Due: l'incarico di insegnamento o di formazione. Qui il ruolo si ribalta: sei tu che insegni o formi "
         "presso l'ospitante, e impari insegnando. Può durare anche periodi più lunghi; la durata esatta per il "
         "tuo settore la trovi nella Guida al Programma dell'anno."),
        ("Colonna 3: <b>Corso strutturato · con quota di iscrizione</b>.",
         "Tre: il corso strutturato. È un corso vero e proprio, organizzato da un ente di formazione, con una "
         "quota di iscrizione. Lo cito solo per distinguerlo: nel job shadowing non ci sono quote e non c'è "
         "aula. C'è il lavoro reale."),
        ("Testo riassuntivo su tre righe.",
         "Un modo semplice per ricordarle. Job shadowing: imparo guardando te. Incarico di insegnamento: imparo "
         "insegnando da te. Corso: imparo in aula."),
    ]),
    ("Chi può farlo (risposta onesta)", PURPLE, [
        ("In camera, tono diretto. Testo: <b>«Posso candidarmi da solo?»</b>",
         "Ora la domanda che arriva più spesso: «posso candidarmi io, da solo?». La risposta onesta è no. Il job "
         "shadowing Erasmus+ non lo chiede un privato cittadino. A chiedere i fondi è un'organizzazione, per "
         "esempio un'associazione, una scuola, un ente di formazione, un centro per adulti o un'organizzazione "
         "giovanile, che manda all'estero il proprio staff."),
        ("Grafica G4: tre cerchi collegati. <b>Organizzazione d'invio → Partecipante → Organizzazione "
         "ospitante</b>.",
         "Quindi i protagonisti sono tre. L'organizzazione d'invio: è quella italiana, riceve il contributo e "
         "organizza la mobilità. Il partecipante: una persona dello staff di quell'organizzazione. "
         "L'organizzazione ospitante: l'ente all'estero che ti accoglie."),
        ("Testo: <b>La domanda giusta</b>.",
         "E questo cambia la domanda da farti. Non «come mi candido?», ma: «faccio parte di un'organizzazione "
         "che può candidarsi? E se no, con quale organizzazione posso collaborare?». Il corso parte proprio da "
         "qui."),
        ("Grafica G5: quattro icone di settore. <b>Adulti · Scuola · Formazione professionale (VET) · "
         "Gioventù</b>.",
         "Attenzione a un dettaglio: l'organizzazione d'invio deve essere ammissibile nel settore in cui si "
         "candida. Se si candida nell'educazione degli adulti, per esempio, deve fare davvero educazione o "
         "formazione per adulti. I settori in cui esiste la mobilità dello staff sono l'educazione degli adulti, "
         "l'istruzione scolastica e la formazione professionale; e con un'azione dedicata anche la gioventù, "
         "per gli youth worker."),
    ]),
    ("Dove si va", ORANGE, [
        ("Grafica G6: mappa d'Europa, i Paesi aderenti si colorano.",
         "Dove si va? In uno dei Paesi aderenti al Programma: i ventisette Stati dell'Unione Europea, più "
         "Islanda, Liechtenstein, Norvegia, Macedonia del Nord, Serbia e Turchia."),
        ("Testo: <b>L'ospitante non paga</b>.",
         "L'ospitante può essere un ente pubblico o privato attivo nel tuo stesso settore: un'associazione, una "
         "scuola, un centro di formazione, una cooperativa. E qui c'è la cosa che sorprende sempre: l'ospitante "
         "non paga nulla. Mette a disposizione tempo ed esperienza. Ecco perché il modo in cui lo contatti conta "
         "tantissimo. Ci arriviamo tra poco."),
    ]),
    ("Chi paga e come", GREEN, [
        ("Grafica G7: <b>UE → Agenzia Nazionale → Organizzazione d'invio</b>. Loghi testuali: INDIRE · INAPP · "
         "Agenzia Italiana per la Gioventù.",
         "Chi paga, allora? L'Unione Europea, attraverso l'Agenzia Nazionale Erasmus+. In Italia sono tre: "
         "INDIRE per scuola ed educazione degli adulti, INAPP per la formazione professionale, e l'Agenzia "
         "Italiana per la Gioventù per il settore giovanile."),
        ("Testo grande: <b>COSTI UNITARI</b>.",
         "Qui c'è un concetto che spiega quasi tutto: i costi unitari. Erasmus+ non rimborsa scontrino per "
         "scontrino. Assegna importi fissi, calcolati con regole precise."),
        ("Grafica G8: tre icone che compaiono in sequenza: treno, letto, ufficio.",
         "Il viaggio: un importo fisso in base alla distanza, con una maggiorazione se viaggi in modo "
         "sostenibile, per esempio in treno o in autobus. Il supporto individuale: un importo per ogni giorno, "
         "che cambia in base al Paese di destinazione, e serve per vitto, alloggio e spostamenti locali. Il "
         "supporto organizzativo: un importo per ogni partecipante, che va all'organizzazione d'invio per "
         "preparare, gestire e seguire la mobilità."),
        ("Testo piccolo: <b>+ inclusione · + costi eccezionali</b>.",
         "Poi ci sono voci per casi specifici: il supporto all'inclusione per i partecipanti con minori "
         "opportunità, e i costi eccezionali, per esempio un viaggio molto costoso ma giustificato."),
        ("In camera. Sovrimpressione: <b>«Le cifre si verificano sulla Guida al Programma»</b>.",
         "Gli importi esatti cambiano ogni anno e li trovi nella Guida al Programma. Non te li do a memoria, ed è "
         "la prima abitudine che voglio darti: numeri e scadenze si verificano sempre sulla fonte ufficiale."),
    ]),
    ("Le strade per ottenere i fondi", NAVY, [
        ("Grafica G9: quattro strade che si diramano.",
         "Come fa un'organizzazione a ottenere questi fondi? Le strade principali sono quattro."),
        ("Strada 1: <b>KA122 · Progetto a breve termine · scadenza di norma a febbraio</b>.",
         "Uno: il progetto di mobilità a breve termine, chiamato KA122. È la porta d'ingresso per chi inizia: un "
         "progetto che dura da sei a diciotto mesi, con un numero limitato di partecipanti. La scadenza, di "
         "norma, è a febbraio."),
        ("Strada 2: <b>Accreditamento Erasmus → KA121 ogni anno</b>.",
         "Due: l'accreditamento Erasmus. L'organizzazione presenta un piano pluriennale, il Piano Erasmus. Se "
         "viene accreditata, ogni anno può chiedere il budget per le mobilità con una domanda semplificata: è "
         "il progetto KA121. È lo strumento di chi vuole fare mobilità in modo continuativo."),
        ("Strada 3: <b>Entrare in un consorzio accreditato</b>.",
         "Tre: il consorzio. Esistono consorzi già accreditati, coordinati per esempio da reti o enti "
         "territoriali. Un'organizzazione può entrarci come membro e far partire il proprio staff senza scrivere "
         "un progetto proprio."),
        ("Strada 4: <b>Gioventù · KA153 · youth worker</b>.",
         "Quattro, per il settore gioventù: la mobilità degli youth worker, chiamata KA153, che prevede anch'essa "
         "il job shadowing ed è gestita dall'Agenzia Italiana per la Gioventù."),
        ("Freccia: <b>breve termine / consorzio → accreditamento</b>.",
         "Per chi parte da zero, il percorso tipico è questo: prima un progetto breve, oppure l'ingresso in un "
         "consorzio, per fare esperienza. Poi, se le mobilità diventano una cosa stabile, l'accreditamento."),
    ]),
    ("Come trovare l'ospitante: 7 canali", ORANGE, [
        ("In camera. Testo: <b>«Ospitante + programma giornaliero»</b>.",
         "Arriviamo alla parte pratica, quella dove si blocca quasi tutti: trovare l'organizzazione che ti ospita. "
         "La regola di base è questa: prendi contatto con un ente di uno dei Paesi aderenti e costruisci insieme "
         "a lui un programma giornaliero delle attività. Ecco sette canali per trovarlo."),
        ("Grafica G10: i 7 canali come lista che si accende. Canale 1: <b>EPALE</b> (schermata reale del sito).",
         "Uno: EPALE, la piattaforma europea per l'educazione degli adulti. Ha uno strumento di ricerca partner e "
         "annunci di enti che cercano o offrono job shadowing. Crei il profilo della tua organizzazione, cerchi "
         "per Paese e tema, e pubblichi la tua richiesta."),
        ("Canale 2: <b>ESEP</b> (schermata reale).",
         "Due: ESEP, la piattaforma europea per l'istruzione scolastica, che comprende anche eTwinning. Ha una "
         "sezione di opportunità di mobilità, con offerte di job shadowing e di insegnamento."),
        ("Canale 3: <b>Piattaforma dei risultati dei progetti Erasmus+</b> (schermata reale con filtri).",
         "Tre: la Piattaforma dei risultati dei progetti Erasmus+, l'archivio dei progetti finanziati. Puoi "
         "filtrare per Paese, settore e tema. Ogni ente che trovi lì ha già fatto Erasmus+, e sa cosa vuol dire "
         "ospitare."),
        ("Canale 4: <b>Esperienze precedenti</b>.",
         "Quattro: le esperienze precedenti. Partner di progetti passati, enti con cui avete già fatto mobilità. "
         "Chiedi a loro di ospitarti, oppure di presentarti a qualcuno della loro rete."),
        ("Canale 5: <b>Seminari internazionali TCA</b> (calendario eventi dell'Agenzia Nazionale).",
         "Cinque: i seminari internazionali TCA, eventi di formazione e di contatto organizzati dalle Agenzie "
         "Nazionali. L'Agenzia italiana pubblica il calendario degli eventi finanziati per i partecipanti "
         "italiani. Sono pensati proprio per far nascere collaborazioni."),
        ("Canale 6: <b>Siti UE · gemellaggi tra città · mobilità precedenti</b>.",
         "Sei: i siti dell'Unione Europea e i gemellaggi tra città. Chiedi al tuo Comune con chi è gemellato. E "
         "riattiva i contatti nati da mobilità precedenti."),
        ("Canale 7: <b>Contatti privati</b>.",
         "Sette: i contatti privati. La tua rete, LinkedIn, i gruppi dedicati a Erasmus+, i colleghi che lavorano "
         "all'estero."),
        ("Grafica G11: anatomia del primo messaggio (chi siamo · cosa vogliamo imparare · quando · costi coperti · "
         "call di 20 minuti · reciprocità).",
         "Un consiglio di metodo. Non mandare tre email per poi aspettare: fai una lista ampia, contatta tutti, e "
         "metti in conto che risponderà solo una parte. Nel primo messaggio sii specifico: chi siete, cosa "
         "volete imparare, quando, per quanti giorni, e che i costi sono coperti dal vostro contributo "
         "Erasmus+. Chiedi solo tempo e una videochiamata di venti minuti. E offri qualcosa in cambio, per "
         "esempio la disponibilità ad accogliere il loro staff in Italia."),
    ]),
    ("Il programma giornaliero e i documenti", TEAL, [
        ("In camera. Testo: <b>Il cuore di tutto</b>.",
         "Hai trovato l'ospitante. Adesso il cuore di tutto: il programma giornaliero. È il documento che "
         "trasforma «andiamo a vedere come lavorano» in un percorso di apprendimento vero."),
        ("Grafica G12: settimana tipo, cinque colonne Lun–Ven che si compilano.",
         "Facciamo un esempio di cinque giorni. Lunedì: accoglienza, presentazione dell'ente, obiettivi "
         "condivisi, e nel pomeriggio già l'osservazione di un'attività. Martedì: affiancamento a un "
         "coordinatore e interviste allo staff su metodi e strumenti. Mercoledì: osservazione di un laboratorio, "
         "magari una visita a un ente della loro rete locale. Giovedì: co-progettazione di un'attività con lo "
         "staff, oppure una breve sessione tenuta da te. Venerdì: restituzione, cosa ti porti a casa, feedback "
         "reciproco e firma dell'attestato."),
        ("Grafica G13: documento con tre firme. <b>Invio · Ospitante · Partecipante</b>.",
         "Il programma si concorda con l'ospitante e si allega all'accordo di mobilità, firmato da tre parti: "
         "organizzazione d'invio, ospitante e partecipante."),
        ("Checklist che si spunta: convenzione · assicurazione · viaggio · attestato di presenza · Europass "
         "Mobility · report del partecipante.",
         "Poi ci sono gli altri documenti: la convenzione tra organizzazione e partecipante, l'assicurazione, i "
         "documenti di viaggio, l'attestato di presenza con le date esatte, l'Europass Mobility, che certifica "
         "le competenze acquisite, e il report del partecipante, un questionario online che arriva dopo la "
         "mobilità."),
    ]),
    ("Prima, durante, dopo", BLUE, [
        ("Grafica G14: linea del tempo orizzontale con tre blocchi colorati.",
         "Mettiamo tutto in fila. Prima: definisci bisogni e obiettivi, scegli il Paese, trova gli ospitanti, e "
         "l'organizzazione presenta la candidatura. Se viene approvata, firma la convenzione con l'Agenzia "
         "Nazionale. Qualche mese prima della partenza: accordo di mobilità e programma giornaliero, poi "
         "logistica e preparazione, anche linguistica e culturale."),
        ("Blocchi «Durante» e «Dopo» si accendono.",
         "Durante: un diario quotidiano, materiali raccolti, confronto costante con l'ospitante. Dopo: il report, "
         "l'Europass e soprattutto la parte che molti saltano: applicare quello che hai imparato, e raccontarlo, "
         "dentro l'organizzazione e fuori. Alla fine del progetto l'organizzazione rendiconta all'Agenzia "
         "Nazionale."),
    ]),
    ("Cinque errori comuni", CORAL, [
        ("In camera. Numeri grandi 1–5 in sovrimpressione, uno per frase.",
         "Cinque errori comuni, così li eviti. Uno: viverlo come una vacanza. Se il programma è vago, la mobilità "
         "è debole, e anche il suo impatto. Due: cercare l'ospitante all'ultimo momento. La ricerca va fatta mesi "
         "prima della candidatura."),
        ("Numeri 3–5.",
         "Tre: obiettivi generici, tipo «migliorare le competenze». Scrivi invece che cosa vuoi saper fare al "
         "ritorno che oggi non sai fare. Quattro: dimenticare il dopo. Il valore del job shadowing si vede quando "
         "torni: se nel vostro lavoro non cambia niente, l'occasione è sprecata. Cinque: fidarsi di numeri e "
         "scadenze sentiti in giro. Ogni anno escono un nuovo Invito e una nuova Guida al Programma: si verifica "
         "lì."),
    ]),
    ("Benefici e chiusura", NAVY, [
        ("Grafica G15: tre colonne. <b>Chi parte · Organizzazione · Ospitante</b>.",
         "Perché vale la pena? Per chi parte: competenze nuove, lingua, fiducia, una rete di colleghi in Europa e "
         "un Europass da mettere nel curriculum. Per l'organizzazione: metodi nuovi, servizi migliori, una "
         "dimensione internazionale, e la base per progetti più grandi, come i partenariati. Per l'ospitante: "
         "uno sguardo esterno sul proprio lavoro e nuovi partner."),
        ("Grafica G16: <b>Riassunto in 3 frasi</b>.",
         "Riassunto in tre frasi. Uno: il job shadowing è imparare osservando, dentro un'organizzazione "
         "all'estero, per un periodo da due a sessanta giorni. Due: lo chiede un'organizzazione per il proprio "
         "staff, con fondi Erasmus+ calcolati a costi unitari. Tre: tutto ruota attorno a due cose: l'ospitante "
         "giusto e un programma giornaliero credibile."),
        ("In camera. Testo finale: <b>Lezione 2 · La tua organizzazione può candidarsi?</b>",
         "Nelle prossime lezioni entriamo dentro ognuno di questi passaggi, con esempi e modelli pronti. Si "
         "comincia dalla domanda più importante: la tua organizzazione può candidarsi? Ci vediamo nella "
         "prossima lezione."),
    ]),
]


def words(t):
    return len(re.findall(r"\w+", re.sub(r"<[^>]+>", "", t)))


def mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def timings():
    out, t = [], 0.0
    for title, col, segs in SCENES:
        w = sum(words(v) for _, v in segs)
        d = w / WPM * 60 + 2 * len(segs)  # piccola pausa tra i blocchi
        out.append((t, t + d, w))
        t += d
    return out, t


class SceneBar(Flowable):
    def __init__(self, num, title, col, tc, w):
        super().__init__()
        self.num, self.title, self.col, self.tc, self.w = num, title, col, tc, w

    def wrap(self, aw, ah):
        return self.w, 22

    def draw(self):
        c = self.canv
        c.setFillColor(self.col)
        c.roundRect(0, 0, self.w, 22, 5, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("DVB", 10.5)
        c.drawString(8, 7, f"SCENA {self.num} · {self.title.upper()}")
        c.setFont("DV", 9)
        c.drawRightString(self.w - 8, 7, self.tc)


def on_page(c, doc):
    w, h = c._pagesize
    c.saveState()
    c.setFillColor(YELLOW)
    c.rect(0, h - 5, w, 5, stroke=0, fill=1)
    c.setFont("DV", 7.5)
    c.setFillColor(GREY)
    c.drawString(18 * mm, 10 * mm, "Corso Job Shadowing Erasmus+  ·  Lezione 1  ·  Script video  ·  MaisEurope")
    c.drawRightString(w - 18 * mm, 10 * mm, str(doc.page))
    c.restoreState()


def on_cover(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.rect(18 * mm, h - 300, 70, 5, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("DVB", 11)
    c.drawString(18 * mm, h - 270, "SCRIPT VIDEO · CORSO JOB SHADOWING ERASMUS+")
    c.setFont("DVB", 32)
    c.drawString(18 * mm, h - 345, "Lezione 1")
    c.setFillColor(YELLOW)
    c.drawString(18 * mm, h - 385, "Cos'è il job shadowing")
    c.setFillColor(colors.white)
    c.setFont("DV", 12.5)
    for i, ln in enumerate(["Panoramica completa: cos'è, chi può farlo, chi paga,",
                            "come trovare l'ospitante, programma giornaliero, documenti, errori comuni.",
                            f"Durata stimata del parlato: ~{int(round(TOTAL / 60))} minuti · formato 16:9"]):
        c.drawString(18 * mm, h - 430 - i * 19, ln)
    c.setFont("DVB", 10)
    c.drawString(18 * mm, 150, "MaisEurope · Materiale di produzione")
    c.setFont("DV", 9)
    c.setFillColor(colors.HexColor("#C9D6EE"))
    c.drawString(18 * mm, 133, "Ottobre 2026 · Importi, durate e scadenze: verificare sempre la Guida al Programma dell'anno.")
    c.restoreState()


TIMES, TOTAL = timings()


def build():
    pw, ph = A4
    M = 18 * mm
    fw = pw - 2 * M
    doc = BaseDocTemplate(PDF, pagesize=A4, title="Script video · Lezione 1 · Cos'è il job shadowing Erasmus+",
                          author="MaisEurope")
    doc.addPageTemplates([
        PageTemplate("cover", frames=[Frame(0, 0, pw, ph)], onPage=on_cover),
        PageTemplate("port", frames=[Frame(M, 17 * mm, fw, ph - 34 * mm)], onPage=on_page),
    ])
    st = [NextPageTemplate("port"), PageBreak()]

    # ------------------------------------------- scheda di produzione
    st += [P("PRIMA DI REGISTRARE", "kicker"), P("Scheda di produzione", "h1"), HRule(), Spacer(1, 8)]
    st.append(table([
        ["Voce", "Indicazione"],
        ["Obiettivo della lezione", "Dare una panoramica completa e corretta del job shadowing Erasmus+, così che "
         "chi guarda capisca cos'è, se può farlo e quali sono i passi. È la lezione 1 del corso: apre tutte le "
         "altre."],
        ["Pubblico", "Persone che lavorano o collaborano con associazioni, scuole, enti di formazione, "
         "organizzazioni giovanili; chi vuole capire se la propria organizzazione può far partire lo staff."],
        ["Durata", f"~{int(round(TOTAL / 60))} minuti di parlato ({sum(t[2] for t in TIMES)} parole a ~{WPM} "
         "parole/minuto). I timecode di ogni scena sono stimati su questo ritmo."],
        ["Formato", "16:9 orizzontale per piattaforma corso / YouTube. Sottotitoli sempre attivi."],
        ["Stile", "Ripresa grezza e diretta, in camera, alternata a grafiche semplici (navy #16305a + giallo). "
         "Niente intro animata lunga: si parte dalla prima frase."],
        ["Fonti da mostrare a schermo", "Schermate reali di EPALE, ESEP, Piattaforma dei risultati dei progetti "
         "Erasmus+, calendario eventi dell'Agenzia Nazionale, Guida al Programma."],
        ["Escluso da questa lezione", "Aspetti commerciali e servizi di terzi: la lezione è solo formativa."],
    ], [42 * mm, fw - 42 * mm], first_col_bold=True))
    st.append(callout(bullets([
        "<b>Nessun dato inventato.</b> Durate e strutture citate sono quelle della Guida al Programma; gli importi "
        "in euro non vengono detti apposta (cambiano ogni anno).",
        "<b>Incarichi di insegnamento:</b> la durata massima varia per settore e anno, per questo nello script "
        "si rimanda alla Guida invece di dare un numero.",
        "<b>Aneddoti dei founder:</b> se volete inserire un'esperienza personale (vedi box «Inserto opzionale»), "
        "usate solo episodi reali e verificabili.",
    ]), title="Regole di accuratezza", color=CORAL, bg=colors.HexColor("#FDEEE9")))

    st.append(P("Capitoli (da incollare nella descrizione del video)", "h2"))
    st.append(table([["Timecode", "Capitolo"]] +
                    [[mmss(TIMES[i][0]), f"{i + 1}. {SCENES[i][0]}"] for i in range(len(SCENES))],
                    [24 * mm, fw - 24 * mm]))

    # ------------------------------------------- script
    st += [PageBreak(), P("LO SCRIPT", "kicker"), P("Script scena per scena", "h1"), HRule(), Spacer(1, 4),
           P("Colonna sinistra: cosa si vede. Colonna destra: cosa si dice (testo da leggere così com'è). "
             "Le parole in grassetto a sinistra sono le sovrimpressioni.", "small"), Spacer(1, 6)]
    for i, (title, col, segs) in enumerate(SCENES):
        t0, t1, w = TIMES[i]
        rows = [[Paragraph(a, S["screen"]), Paragraph(v, S["voice"])] for a, v in segs]
        tb = Table(rows, colWidths=[56 * mm, fw - 56 * mm])
        tb.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, -1), LIGHT),
            ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#D5DCE8")),
            ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        st.append(CondPageBreak(60 * mm))
        st.append(SceneBar(i + 1, title, col, f"{mmss(t0)} – {mmss(t1)}", fw))
        st.append(Spacer(1, 3))
        st.append(tb)
        st.append(Spacer(1, 12))
        if title == "Chi può farlo (risposta onesta)":
            st.append(callout(
                "Qui potete inserire 20–30 secondi in prima persona: perché ve ne occupate, cosa vi ha insegnato "
                "un'esperienza Erasmus+ <b>reale</b>. Scrivetelo voi con dettagli veri (luogo, momento, cosa è "
                "cambiato). Se non c'è un episodio adatto, saltate l'inserto: la lezione regge anche senza.",
                title="Inserto opzionale (solo se vero)", color=PURPLE, bg=colors.HexColor("#F1ECFA")))

    # ------------------------------------------- grafiche
    st += [PageBreak(), P("POST-PRODUZIONE", "kicker"), P("Grafiche da preparare", "h1"), HRule(), Spacer(1, 8)]
    st.append(table([
        ["#", "Grafica", "Contenuto"],
        ["G1", "Indice", "Cos'è · Chi può farlo · Dove · Chi paga · Strade · Ospitante · Programma · Errori"],
        ["G2", "Shadow = ombra", "Sagoma che segue un professionista al lavoro"],
        ["G3", "Tre attività", "Job shadowing (2–60 gg) · Insegnamento/formazione (durata: Guida) · Corso (con quota)"],
        ["G4", "Tre protagonisti", "Organizzazione d'invio → Partecipante → Organizzazione ospitante"],
        ["G5", "Settori", "Adulti · Scuola · Formazione professionale (VET) · Gioventù (youth worker)"],
        ["G6", "Mappa", "UE-27 + Islanda, Liechtenstein, Norvegia, Macedonia del Nord, Serbia, Turchia"],
        ["G7", "Chi paga", "UE → Agenzia Nazionale (INDIRE · INAPP · Agenzia Italiana per la Gioventù) → ente d'invio"],
        ["G8", "Costi unitari", "Viaggio (distanza, bonus green) · Supporto individuale (giorno/Paese) · Supporto organizzativo"],
        ["G9", "Quattro strade", "KA122 · Accreditamento → KA121 · Consorzio · KA153 Gioventù"],
        ["G10", "Sette canali", "EPALE · ESEP · Piattaforma risultati · Esperienze precedenti · TCA · Siti UE/gemellaggi · Contatti privati"],
        ["G11", "Primo messaggio", "Chi siamo · Cosa vogliamo imparare · Quando/quanti giorni · Costi coperti · Call 20' · Reciprocità"],
        ["G12", "Settimana tipo", "Lun accoglienza · Mar affiancamento · Mer laboratorio/visita · Gio co-progettazione · Ven restituzione"],
        ["G13", "Accordo di mobilità", "Documento con tre firme"],
        ["G14", "Timeline", "Prima · Durante · Dopo"],
        ["G15", "Benefici", "Chi parte · Organizzazione · Ospitante"],
        ["G16", "Riassunto", "Le tre frasi finali"],
    ], [12 * mm, 34 * mm, fw - 46 * mm], first_col_bold=True))
    st.append(P("B-roll consigliato", "h2"))
    st += bullets([
        "Registrazioni schermo reali dei siti (EPALE, ESEP, Piattaforma dei risultati, Guida al Programma).",
        "Riprese reali di una vostra mobilità o di un ente partner, con liberatoria. Niente stock spacciato "
        "per esperienza reale.",
        "Dettagli di lavoro: agenda, programma giornaliero stampato, firme, laptop con videochiamata.",
    ])

    # ------------------------------------------- quiz
    st += [PageBreak(), P("PER LA PIATTAFORMA", "kicker"), P("Quiz e clip brevi", "h1"), HRule(), Spacer(1, 8)]
    st.append(P("Quiz di fine lezione", "h2"))
    quiz = [
        ("Quanto dura un job shadowing Erasmus+?", "A) 1–7 giorni · B) 2–60 giorni · C) 3–12 mesi", "B"),
        ("Chi chiede i fondi?", "A) Il partecipante · B) L'ospitante · C) L'organizzazione d'invio", "C"),
        ("L'organizzazione ospitante…", "A) paga una quota · B) non paga nulla · C) riceve la diaria del partecipante", "B"),
        ("Cosa sono i costi unitari?", "A) Rimborsi a scontrino · B) Importi fissi calcolati con regole precise · "
                                        "C) Un anticipo da restituire", "B"),
        ("Quale strumento serve a fare mobilità ogni anno?", "A) Accreditamento Erasmus (poi KA121) · B) Corso "
                                                              "strutturato · C) Europass", "A"),
        ("Quale documento si allega all'accordo di mobilità?", "A) Il curriculum · B) Il programma giornaliero · "
                                                                "C) La fattura del viaggio", "B"),
        ("Dove si cercano ospitanti nell'educazione degli adulti?", "A) EPALE · B) Solo tramite agenzie · "
                                                                     "C) Non serve cercarli", "A"),
        ("Qual è uno degli errori più comuni?", "A) Scrivere obiettivi specifici · B) Cercare l'ospitante "
                                                 "all'ultimo momento · C) Fare un diario", "B"),
    ]
    st.append(table([["#", "Domanda", "Opzioni", "Risposta"]] +
                    [[str(i), q, o, a] for i, (q, o, a) in enumerate(quiz, 1)],
                    [8 * mm, 58 * mm, fw - 84 * mm, 18 * mm]))

    st.append(P("Clip brevi ricavabili da questa lezione (Reel / TikTok / Shorts)", "h2"))
    st.append(table([
        ["Clip", "Da scena", "Formato", "Attacco"],
        ["«Una settimana dentro un'organizzazione all'estero»", "1", "Nessuno te lo dice",
         "Esiste un modo per lavorare una settimana dentro un ente in Europa, con i costi coperti dall'UE. "
         "Quasi nessuno lo usa."],
        ["«Posso candidarmi da solo?»", "4", "Nessuno te lo dice",
         "La domanda che fanno tutti sul job shadowing, e la risposta onesta che nessuno dà."],
        ["«5 errori che bruciano il job shadowing»", "11", "Engagement (vero/falso)",
         "Errore n. 2 lo fanno quasi tutti: cercare l'ospitante all'ultimo momento."],
    ], [48 * mm, 16 * mm, 32 * mm, fw - 96 * mm]))
    st.append(Spacer(1, 4))
    st.append(P("Il formato «Risposte Oneste» richiede una domanda reale ricevuta in DM o nei commenti: quando "
                "arriva, la scena 4 si può ripubblicare come risposta.", "small"))

    # ------------------------------------------- corso
    st += [PageBreak(), P("IL CORSO", "kicker"), P("Struttura del corso che parte da questa lezione", "h1"),
           HRule(), Spacer(1, 8)]
    mods = [
        ("1", "Cos'è il job shadowing", "Questa lezione: panoramica completa.", "Mappa mentale del quadro completo"),
        ("2", "La tua organizzazione può candidarsi?", "Ammissibilità per settore, ruolo dello staff, cosa fare "
         "se l'organizzazione non è ammissibile (consorzi, collaborazioni).", "Autovalutazione di ammissibilità"),
        ("3", "Bisogni e obiettivi di apprendimento", "Dai problemi reali dell'organizzazione agli obiettivi "
         "misurabili; esempi buoni e cattivi.", "3–5 obiettivi scritti bene"),
        ("4", "Trovare l'ospitante", "I 7 canali in pratica (con schermate), primo messaggio, videochiamata, "
         "reciprocità.", "Lista di enti + email pronta"),
        ("5", "Il programma giornaliero e l'accordo di mobilità", "Come si costruisce giorno per giorno, come "
         "si verifica l'apprendimento, chi firma.", "Programma di 5 giorni compilato"),
        ("6", "Fondi e budget", "Costi unitari, come leggere le tabelle della Guida, inclusione, costi "
         "eccezionali, supporto organizzativo.", "Budget del proprio flusso"),
        ("7", "La candidatura", "KA122, accreditamento e KA121, consorzi, KA153: scadenze, moduli, cosa "
         "valutano.", "Bozza delle sezioni chiave"),
        ("8", "Preparare la partenza", "Logistica, viaggio sostenibile, assicurazione, preparazione "
         "linguistica e culturale.", "Kit partenza"),
        ("9", "Durante e dopo", "Diario, Europass Mobility, report del partecipante, trasferimento nel lavoro, "
         "diffusione dei risultati.", "Piano di trasferimento"),
        ("10", "Ripetere e crescere", "Dalla prima mobilità a un piano annuale: accreditamento, partenariati, "
         "rete di ospitanti.", "Piano a 12 mesi"),
    ]
    st.append(table([["Mod.", "Titolo", "Cosa si impara", "Esercizio / risultato"]] + [list(m) for m in mods],
                    [12 * mm, 44 * mm, fw - 104 * mm, 48 * mm], first_col_bold=True))
    st.append(callout(
        "Formato consigliato per ogni modulo: 1 video principale (8–15 minuti) + 1–2 video brevi pratici "
        "(schermate, esempi) + scheda PDF + quiz. Il materiale della «Guida operativa» già prodotta (canali, "
        "timeline, programma giornaliero, checklist, glossario) copre gran parte delle schede dei moduli 3–9.",
        title="Come costruire ogni modulo"))

    doc.build(st)

    # ------------------------------------------- teleprompter
    with open(TXT, "w", encoding="utf-8") as f:
        f.write("TELEPROMPTER · LEZIONE 1 · COS'È IL JOB SHADOWING ERASMUS+\n")
        f.write(f"Durata stimata: ~{int(round(TOTAL / 60))} minuti\n\n")
        for i, (title, _, segs) in enumerate(SCENES):
            f.write(f"=== SCENA {i + 1} · {title.upper()} ({mmss(TIMES[i][0])}) ===\n\n")
            for _, v in segs:
                f.write(re.sub(r"<[^>]+>", "", v) + "\n\n")
    print("PDF:", PDF)
    print("TXT:", TXT)
    print("Parole:", sum(t[2] for t in TIMES), "Durata:", mmss(TOTAL))


if __name__ == "__main__":
    build()
