# -*- coding: utf-8 -*-
"""Genera la guida PDF "Job Shadowing & Teaching Erasmus+" (MaisEurope x Metiva).

Uso:  python3 build_pdf.py
Output: Guida_Job_Shadowing_Erasmus_MaisEurope_Metiva.pdf (nella stessa cartella)
"""
import math
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame,
                                KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Guida_Job_Shadowing_Erasmus_MaisEurope_Metiva.pdf")

# ---------------------------------------------------------------- font
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")

# ---------------------------------------------------------------- palette
NAVY = colors.HexColor("#0B2A5B")
BLUE = colors.HexColor("#1F5FBF")
YELLOW = colors.HexColor("#F4C20D")
TEAL = colors.HexColor("#0E8C88")
CORAL = colors.HexColor("#E4572E")
PURPLE = colors.HexColor("#6C4AB6")
GREEN = colors.HexColor("#2E9E4F")
ORANGE = colors.HexColor("#E08A00")
GREY = colors.HexColor("#5B6577")
LIGHT = colors.HexColor("#F3F6FB")
LINE = colors.HexColor("#D5DCE8")
INK = colors.HexColor("#1B2333")

# ---------------------------------------------------------------- stili
S = {}
S["body"] = ParagraphStyle("body", fontName="DV", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=5)
S["small"] = ParagraphStyle("small", parent=S["body"], fontSize=8.2, leading=11, textColor=GREY)
S["h1"] = ParagraphStyle("h1", fontName="DVB", fontSize=19, leading=23, textColor=NAVY, spaceBefore=4, spaceAfter=4)
S["kicker"] = ParagraphStyle("kicker", fontName="DVB", fontSize=8.5, leading=11, textColor=TEAL, spaceAfter=2)
S["h2"] = ParagraphStyle("h2", fontName="DVB", fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=10, spaceAfter=4)
S["h3"] = ParagraphStyle("h3", fontName="DVB", fontSize=10.4, leading=13.5, textColor=BLUE, spaceBefore=6, spaceAfter=2)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=13, bulletIndent=2, spaceAfter=2.5)
S["cell"] = ParagraphStyle("cell", fontName="DV", fontSize=8.4, leading=11, textColor=INK)
S["cellb"] = ParagraphStyle("cellb", parent=S["cell"], fontName="DVB")
S["cellh"] = ParagraphStyle("cellh", parent=S["cell"], fontName="DVB", textColor=colors.white)
S["callout"] = ParagraphStyle("callout", parent=S["body"], fontSize=9.3, leading=13, spaceAfter=0)
S["toc"] = ParagraphStyle("toc", parent=S["body"], fontSize=10.5, leading=17)


def P(t, st="body"):
    return Paragraph(t, S[st])


def bullets(items, st="bullet", sym="•"):
    return [Paragraph(i, S[st], bulletText=sym) for i in items]


def section(num, title, kicker):
    return [CondPageBreak(120 * mm), Spacer(1, 10), P(kicker.upper(), "kicker"), P(f"{num}. {title}", "h1"),
            HRule(), Spacer(1, 6)]


class HRule(Flowable):
    def __init__(self, color=YELLOW, w=60 * mm, t=3):
        super().__init__()
        self.color, self.w, self.t = color, w, t

    def wrap(self, aw, ah):
        return aw, self.t + 2

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.w, self.t, stroke=0, fill=1)


def callout(text, color=TEAL, bg=None, title=None):
    bg = bg or colors.HexColor("#EAF6F5")
    inner = []
    if title:
        inner.append(Paragraph(f"<font color='{color.hexval()}'><b>{title}</b></font>", S["callout"]))
        inner.append(Spacer(1, 3))
    if isinstance(text, str):
        inner.append(Paragraph(text, S["callout"]))
    else:
        inner.extend(text)
    t = Table([[inner]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 8)])


def table(rows, widths, head_bg=NAVY, zebra=True, first_col_bold=False):
    data = []
    for r, row in enumerate(rows):
        line = []
        for c, v in enumerate(row):
            if r == 0:
                line.append(Paragraph(v, S["cellh"]))
            else:
                line.append(Paragraph(v, S["cellb"] if (first_col_bold and c == 0) else S["cell"]))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if zebra:
        for r in range(1, len(rows)):
            if r % 2 == 0:
                st.append(("BACKGROUND", (0, r), (-1, r), LIGHT))
    t.setStyle(TableStyle(st))
    return KeepTogether(t) if len(rows) <= 8 else t


# ---------------------------------------------------------------- disegno: mappa mentale
def _wrap(text, font, size, width):
    return simpleSplit(text, font, size, width)


class MindMap(Flowable):
    """Mappa mentale radiale: nodo centrale + rami a sinistra/destra con sotto-voci."""

    def __init__(self, title, subtitle, center, branches, w, h):
        super().__init__()
        self.title, self.subtitle, self.center, self.branches = title, subtitle, center, branches
        self.w, self.h = w, h

    def wrap(self, aw, ah):
        return self.w, self.h

    def _card_h(self, br, cw):
        h = 22
        for it in br[2]:
            h += len(_wrap(it, "DV", 8.3, cw - 22)) * 10.4 + 2.5
        return h + 6

    def draw(self):
        c = self.canv
        W, H = self.w, self.h
        c.setFillColor(NAVY)
        c.setFont("DVB", 17)
        c.drawString(0, H - 18, self.title)
        c.setFillColor(GREY)
        c.setFont("DV", 9)
        c.drawString(0, H - 32, self.subtitle)

        top, bottom = H - 46, 4
        cw = 214
        n = len(self.branches)
        right = self.branches[: (n + 1) // 2]
        left = self.branches[(n + 1) // 2:]
        cx, cy = W / 2, (top + bottom) / 2

        def place(side_branches, x):
            hs = [self._card_h(b, cw) for b in side_branches]
            gap = max(6, (top - bottom - sum(hs)) / max(1, len(hs)))
            y = top - gap / 2
            out = []
            for b, hh in zip(side_branches, hs):
                out.append((b, x, y - hh, hh))
                y -= hh + gap
            return out

        placed = place(right, W - cw) + place(left[::-1], 0)

        # connettori
        for b, x, y, hh in placed:
            col = b[1]
            c.setStrokeColor(col)
            c.setLineWidth(2.2)
            ty = y + hh / 2
            if x > cx:
                sx, ex = cx + 70, x
            else:
                sx, ex = cx - 70, x + cw
            p = c.beginPath()
            p.moveTo(sx, cy)
            mid = (sx + ex) / 2
            p.curveTo(mid, cy, mid, ty, ex, ty)
            c.drawPath(p, stroke=1, fill=0)

        # nodo centrale
        c.setFillColor(NAVY)
        c.setStrokeColor(YELLOW)
        c.setLineWidth(3)
        c.ellipse(cx - 92, cy - 46, cx + 92, cy + 46, stroke=1, fill=1)
        lines = self.center.split("\n")
        c.setFillColor(colors.white)
        y0 = cy + (len(lines) - 1) * 7.5 - 4
        for i, ln in enumerate(lines):
            c.setFont("DVB", 11.5 if i == 0 else 9.5)
            c.drawCentredString(cx, y0 - i * 15, ln)

        # card
        for b, x, y, hh in placed:
            title, col, items = b
            c.setFillColor(colors.white)
            c.setStrokeColor(col)
            c.setLineWidth(1.4)
            c.roundRect(x, y, cw, hh, 7, stroke=1, fill=1)
            c.setFillColor(col)
            c.roundRect(x, y + hh - 19, cw, 19, 7, stroke=0, fill=1)
            c.rect(x, y + hh - 19, cw, 8, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("DVB", 9.6)
            c.drawString(x + 8, y + hh - 13.5, title)
            ty = y + hh - 33
            for it in items:
                ls = _wrap(it, "DV", 8.3, cw - 22)
                c.setFillColor(col)
                c.circle(x + 10, ty + 3, 1.8, stroke=0, fill=1)
                c.setFillColor(INK)
                c.setFont("DV", 8.3)
                for ln in ls:
                    c.drawString(x + 16, ty, ln)
                    ty -= 10.4
                ty -= 2.5


class Cycle(Flowable):
    """Diagramma del circolo virtuoso: nodi su un cerchio con frecce."""

    def __init__(self, nodes, center, w, h, r=None):
        super().__init__()
        self.nodes, self.center, self.w, self.h = nodes, center, w, h
        self.rx, self.ry = w / 2 - 70, h / 2 - 30

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        cx, cy, RX, RY = self.w / 2, self.h / 2, self.rx, self.ry
        n = len(self.nodes)
        # anello
        c.setStrokeColor(LINE)
        c.setLineWidth(10)
        c.ellipse(cx - RX, cy - RY, cx + RX, cy + RY, stroke=1, fill=0)
        # frecce sull'anello
        c.setStrokeColor(YELLOW)
        c.setFillColor(YELLOW)
        for i in range(n):
            a = math.pi / 2 - (i + 0.5) * 2 * math.pi / n
            px, py = cx + RX * math.cos(a), cy + RY * math.sin(a)
            d = math.atan2(-RY * math.cos(a), RX * math.sin(a))  # tangente, verso orario
            s = 9
            p = c.beginPath()
            p.moveTo(px + s * math.cos(d), py + s * math.sin(d))
            p.lineTo(px + s * 0.8 * math.cos(d + 2.4), py + s * 0.8 * math.sin(d + 2.4))
            p.lineTo(px + s * 0.8 * math.cos(d - 2.4), py + s * 0.8 * math.sin(d - 2.4))
            p.close()
            c.drawPath(p, stroke=0, fill=1)
        # centro
        c.setFillColor(NAVY)
        c.circle(cx, cy, 54, stroke=0, fill=1)
        c.setFillColor(colors.white)
        lines = self.center.split("\n")
        for i, ln in enumerate(lines):
            c.setFont("DVB", 10.5 if i == 0 else 8.6)
            c.drawCentredString(cx, cy + (len(lines) - 1) * 6 - i * 13 - 3, ln)
        # nodi
        bw, bh = 128, 50
        for i, (title, txt, col) in enumerate(self.nodes):
            a = math.pi / 2 - i * 2 * math.pi / n
            px, py = cx + RX * math.cos(a), cy + RY * math.sin(a)
            x, y = px - bw / 2, py - bh / 2
            c.setFillColor(colors.white)
            c.setStrokeColor(col)
            c.setLineWidth(1.6)
            c.roundRect(x, y, bw, bh, 8, stroke=1, fill=1)
            c.setFillColor(col)
            c.circle(x + 12, y + bh - 12, 8, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("DVB", 8.5)
            c.drawCentredString(x + 12, y + bh - 15, str(i + 1))
            c.setFillColor(col)
            c.setFont("DVB", 8.8)
            c.drawString(x + 24, y + bh - 15, title)
            c.setFillColor(INK)
            c.setFont("DV", 7.5)
            ty = y + bh - 28
            for ln in _wrap(txt, "DV", 7.5, bw - 12)[:3]:
                c.drawString(x + 6, ty, ln)
                ty -= 9


class Funnel(Flowable):
    def __init__(self, stages, w, h):
        super().__init__()
        self.stages, self.w, self.h = stages, w, h

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        n = len(self.stages)
        sh = self.h / n
        maxw, minw = self.w * 0.62, self.w * 0.22
        for i, (label, kpi, col) in enumerate(self.stages):
            w1 = maxw - (maxw - minw) * i / n
            w2 = maxw - (maxw - minw) * (i + 1) / n
            yt = self.h - i * sh
            yb = yt - sh + 3
            cx = maxw / 2
            p = c.beginPath()
            p.moveTo(cx - w1 / 2, yt)
            p.lineTo(cx + w1 / 2, yt)
            p.lineTo(cx + w2 / 2, yb)
            p.lineTo(cx - w2 / 2, yb)
            p.close()
            c.setFillColor(col)
            c.drawPath(p, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("DVB", 8.6)
            c.drawCentredString(cx, (yt + yb) / 2 - 3, label)
            c.setFillColor(INK)
            c.setFont("DV", 8.2)
            c.drawString(maxw + 12, (yt + yb) / 2 - 3, kpi)
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            c.line(cx + w1 / 2 - 4, (yt + yb) / 2, maxw + 8, (yt + yb) / 2)


# ---------------------------------------------------------------- pagine
def on_page(c, doc):
    w, h = c._pagesize
    c.saveState()
    c.setFillColor(YELLOW)
    c.rect(0, h - 5, w, 5, stroke=0, fill=1)
    c.setFont("DV", 7.5)
    c.setFillColor(GREY)
    c.drawString(18 * mm, 10 * mm, "Guida operativa Job Shadowing & Teaching Erasmus+  ·  MaisEurope × Metiva")
    c.drawRightString(w - 18 * mm, 10 * mm, str(doc.page))
    c.restoreState()


def on_cover(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    # stelle UE stilizzate
    c.setFillColor(YELLOW)
    cx, cy, R = w - 120, h - 150, 62
    for i in range(12):
        a = 2 * math.pi * i / 12
        _star(c, cx + R * math.cos(a), cy + R * math.sin(a), 7)
    c.setFillColor(colors.HexColor("#173F7E"))
    c.rect(0, 0, w, 210, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.rect(18 * mm, h - 300, 70, 5, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("DVB", 11)
    c.drawString(18 * mm, h - 270, "GUIDA OPERATIVA + MAPPE MENTALI")
    c.setFont("DVB", 34)
    c.drawString(18 * mm, h - 345, "Job Shadowing")
    c.drawString(18 * mm, h - 385, "& Teaching")
    c.setFillColor(YELLOW)
    c.drawString(18 * mm, h - 425, "Erasmus+")
    c.setFillColor(colors.white)
    c.setFont("DV", 12.5)
    for i, ln in enumerate([
        "Come funziona · come trovare l'ospitante · come attuarlo",
        "Come ripeterlo più volte l'anno nello stesso Paese",
        "Come trasformare gli ospitanti in clienti Metiva (40% a MaisEurope)",
    ]):
        c.drawString(18 * mm, h - 470 - i * 19, ln)
    c.setFont("DVB", 10)
    c.drawString(18 * mm, 150, "MaisEurope × Metiva")
    c.setFont("DV", 9)
    c.setFillColor(colors.HexColor("#C9D6EE"))
    c.drawString(18 * mm, 133, "Documento interno di studio e lavoro · Ottobre 2026")
    c.drawString(18 * mm, 118, "Regole, importi e scadenze: verificare sempre l'Invito e la Guida al Programma dell'anno in corso.")
    c.restoreState()


def _star(c, x, y, r):
    p = c.beginPath()
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = math.pi / 2 + k * math.pi / 5
        (p.moveTo if k == 0 else p.lineTo)(x + rr * math.cos(a), y + rr * math.sin(a))
    p.close()
    c.drawPath(p, stroke=0, fill=1)


# ================================================================ CONTENUTI
def build():
    pw, ph = A4
    lw, lh = landscape(A4)
    M = 18 * mm
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=17 * mm,
                          bottomMargin=17 * mm, title="Job Shadowing & Teaching Erasmus+ — Guida operativa",
                          author="MaisEurope", subject="Erasmus+ KA1 mobilità staff, strategia MaisEurope × Metiva")
    fw = pw - 2 * M
    doc.addPageTemplates([
        PageTemplate("cover", frames=[Frame(0, 0, pw, ph, id="c")], onPage=on_cover, pagesize=A4),
        PageTemplate("port", frames=[Frame(M, 17 * mm, fw, ph - 34 * mm, id="p")], onPage=on_page, pagesize=A4),
        PageTemplate("land", frames=[Frame(14 * mm, 15 * mm, lw - 28 * mm, lh - 27 * mm, id="l",
                                           leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                     onPage=on_page, pagesize=landscape(A4)),
    ])
    MW, MH = lw - 28 * mm, lh - 27 * mm

    st = [NextPageTemplate("port"), PageBreak()]

    # ------------------------------------------------ indice
    st += [P("COME USARE QUESTA GUIDA", "kicker"), P("Indice", "h1"), HRule(), Spacer(1, 8)]
    toc = [
        ("1", "Le basi in una pagina"),
        ("—", "Mappa mentale 1 · Il quadro completo"),
        ("2", "Come si finanzia: le strade per partire"),
        ("3", "Come trovare l'organizzazione ospitante: i 7 canali"),
        ("—", "Mappa mentale 2 · I 7 canali in azione"),
        ("4", "Come attuarlo, passo dopo passo"),
        ("5", "Budget: come si calcolano i fondi"),
        ("6", "I benefici (per chi parte, per chi ospita, per MaisEurope)"),
        ("7", "Ripeterlo più volte l'anno nello stesso Paese"),
        ("8", "Dall'ospitante al cliente Metiva: il funnel e il 40%"),
        ("9", "Il circolo virtuoso"),
        ("—", "Mappa mentale 3 · Il circolo virtuoso"),
        ("10", "Regole d'oro e compliance"),
        ("11", "Modelli pronti all'uso (email, programma, script, CRM)"),
        ("12", "Ripasso: domande-flash, glossario, link utili"),
    ]
    st.append(table([["#", "Contenuto"]] + [[a, b] for a, b in toc], [14 * mm, fw - 14 * mm], zebra=True))
    st.append(Spacer(1, 10))
    st.append(callout(
        bullets([
            "<b>Studio:</b> leggi prima la Sezione 1, poi fissa tutto con la <b>Mappa mentale 1</b>. "
            "Ripassa con le domande-flash della Sezione 12 (copri la risposta e prova a rispondere).",
            "<b>Operatività:</b> Sezioni 3, 4 e 11 sono la cassetta degli attrezzi (canali, timeline, modelli).",
            "<b>Business:</b> Sezioni 7, 8 e 9 spiegano come ripetere le mobilità e far nascere clienti Metiva; "
            "la Sezione 10 è il recinto entro cui farlo senza rischi.",
        ]), title="Tre modi di leggere questo documento"))
    st.append(callout(
        "Le regole Erasmus+ (durate, importi, scadenze) cambiano ogni anno con l'Invito a presentare proposte e la "
        "Guida al Programma. Qui trovi i valori di riferimento noti a ottobre 2026: prima di candidarti verifica "
        "sempre sulla Guida ufficiale e sul sito dell'Agenzia Nazionale competente.",
        color=CORAL, bg=colors.HexColor("#FDEEE9"), title="Nota di affidabilità"))

    # ------------------------------------------------ 1. basi
    st += section(1, "Le basi in una pagina", "Capire")
    st.append(P("Il <b>job shadowing</b> e gli <b>incarichi di insegnamento o formazione</b> sono due attività di "
                "<b>mobilità dello staff</b> dell'Azione chiave 1 (KA1) di Erasmus+. Servono a far crescere le "
                "persone che lavorano in un'organizzazione (docenti, formatori, educatori, operatori, staff "
                "amministrativo) facendole lavorare per qualche giorno <b>dentro</b> un'organizzazione simile in un "
                "altro Paese aderente al Programma."))
    st.append(table([
        ["", "Job shadowing", "Incarico di insegnamento / formazione", "Corso strutturato (per confronto)"],
        ["Cosa fai", "Osservi e affianchi i colleghi dell'ospitante nel loro lavoro quotidiano",
         "Insegni o formi tu: porti competenze all'ospitante e impari facendo",
         "Frequenti un corso a pagamento organizzato da un ente formativo"],
        ["Durata", "2–60 giorni (+ giorni di viaggio)", "2–365 giorni (+ giorni di viaggio)", "2–30 giorni"],
        ["Ruolo", "Apprendi osservando", "Apprendi insegnando / formando", "Apprendi in aula"],
        ["Costo per l'ospitante", "Nessuno: l'ospitante dedica tempo, non paga", "Nessuno", "—"],
        ["Ideale per", "Primi contatti, scoprire metodi, costruire relazione",
         "Relazione più profonda, scambio di competenze", "Formazione su un tema preciso"],
    ], [26 * mm, 46 * mm, 52 * mm, fw - 124 * mm], first_col_bold=True))
    st.append(Spacer(1, 8))
    st.append(P("Chi è coinvolto", "h3"))
    st += bullets([
        "<b>Organizzazione d'invio</b> (es. un'associazione italiana attiva nell'educazione degli adulti, una scuola, "
        "un ente VET, un'organizzazione giovanile): riceve i fondi e manda il proprio staff.",
        "<b>Partecipante</b>: membro dello staff dell'organizzazione d'invio (dipendente, collaboratore o, dove previsto, "
        "volontario con ruolo stabile).",
        "<b>Organizzazione ospitante</b>: ente pubblico o privato attivo nello stesso settore in un Paese aderente al "
        "Programma (i 27 Stati UE + Islanda, Liechtenstein, Norvegia, Macedonia del Nord, Serbia, Turchia).",
        "<b>Agenzia Nazionale</b> (in Italia): INDIRE per Scuola, Educazione degli adulti e Università; INAPP per "
        "Istruzione e formazione professionale (VET); Agenzia Italiana per la Gioventù per il settore Gioventù.",
    ])
    st.append(P("Il cuore operativo", "h3"))
    st.append(P("Per organizzare job shadowing o attività di insegnamento è necessario <b>prendere contatti con "
                "un'organizzazione o ente di uno dei Paesi aderenti al Programma</b> e <b>definire insieme un programma "
                "giornaliero</b> delle attività da svolgere nel periodo di formazione. Tutto il resto (fondi, "
                "documenti, strategia) ruota attorno a questi due elementi: <b>l'ospitante giusto</b> e <b>un programma "
                "di apprendimento credibile</b>."))
    st.append(callout("Job shadowing = <b>io imparo guardando te</b>. Teaching assignment = <b>io imparo insegnando "
                      "da te</b>. In entrambi i casi l'ospitante non paga nulla, l'UE copre viaggio e soggiorno di chi "
                      "parte, e il risultato atteso è un cambiamento concreto nel lavoro dell'organizzazione d'invio.",
                      title="Da ricordare in una frase"))

    # ------------------------------------------------ MAPPA 1
    st += [NextPageTemplate("land"), PageBreak()]
    st.append(MindMap(
        "Mappa mentale 1 · Il quadro completo",
        "Leggi in senso orario partendo da destra in alto. Ogni ramo = una sezione della guida.",
        "JOB SHADOWING\n& TEACHING\nErasmus+ KA1",
        [
            ("1 · Cos'è", BLUE, [
                "Job shadowing: osservi/affianchi, 2–60 gg",
                "Teaching/training: insegni, 2–365 gg",
                "Settori: Adulti · Scuola · VET · Gioventù",
                "Ospitante in un Paese aderente, non paga nulla",
            ]),
            ("2 · Come si finanzia", TEAL, [
                "KA122 progetto breve (scadenza a febbraio)",
                "KA121 con accreditamento (budget annuale)",
                "Entrare in un consorzio accreditato",
                "Gioventù: KA153 youth workers",
                "AN: INDIRE · INAPP · Agenzia Gioventù",
            ]),
            ("3 · Trovare l'ospitante", ORANGE, [
                "EPALE · ESEP · Project Results Platform",
                "Partner e mobilità precedenti",
                "Seminari TCA delle Agenzie Nazionali",
                "Siti UE, gemellaggi, contatti privati",
            ]),
            ("4 · Attuarlo", PURPLE, [
                "Obiettivi → ospitante → candidatura",
                "Accordo di mobilità firmato a 3",
                "Programma giornaliero concordato",
                "Europass Mobility + report + diffusione",
            ]),
            ("5 · Fondi", GREEN, [
                "Viaggio (fasce km, bonus green)",
                "Supporto individuale per giorno",
                "Supporto organizzativo per partecipante",
                "Inclusione e costi eccezionali",
            ]),
            ("6 · Benefici", BLUE, [
                "Competenze, lingue, metodi nuovi",
                "Rete internazionale di enti",
                "Base per partenariati KA2",
            ]),
            ("7-9 · Strategia MaisEurope × Metiva", CORAL, [
                "1 Paese focus, N flussi l'anno",
                "Ospitante diverso ogni volta",
                "Valore prima → poi proposta Metiva",
                "40% del chiuso a MaisEurope",
                "Ogni cliente porta nuovi ospitanti",
            ]),
            ("10 · Regole d'oro", NAVY, [
                "L'apprendimento viene prima di tutto",
                "Nessuna vendita nelle ore finanziate",
                "Contratti scritti, GDPR, trasparenza",
            ]),
        ], MW, MH))
    st += [NextPageTemplate("port"), PageBreak()]

    # ------------------------------------------------ 2. finanziamento
    st += section(2, "Come si finanzia: le strade per partire", "Capire")
    st.append(P("Il job shadowing non si richiede da solo: lo chiede l'<b>organizzazione d'invio</b> dentro un progetto "
                "di mobilità KA1. Le strade sono quattro."))
    st.append(table([
        ["Strada", "Per chi", "Come funziona", "Quando"],
        ["<b>KA122</b> Progetto di mobilità a breve termine",
         "Chi inizia o fa poche mobilità (Adulti, Scuola, VET)",
         "Un progetto di 6–18 mesi, fino a 30 partecipanti. Limite di progetti brevi finanziabili nell'arco di "
         "più anni (verificare il limite nella Guida dell'anno).",
         "Una scadenza l'anno, di norma a febbraio (2026: 19 febbraio, ore 12:00 Bruxelles)."],
        ["<b>KA121</b> Progetto accreditato",
         "Chi vuole fare mobilità ogni anno",
         "Si ottiene prima l'<b>Accreditamento Erasmus (KA120)</b> con un Piano Erasmus pluriennale; poi ogni anno si "
         "chiede il budget con una domanda semplificata.",
         "Accreditamento: autunno (2026: 29 settembre). Budget annuale: febbraio."],
        ["<b>Consorzio accreditato</b>",
         "Chi non vuole/può scrivere un progetto proprio",
         "Si entra come membro in un consorzio già accreditato (reti regionali, enti coordinatori) che gestisce "
         "candidatura e fondi.",
         "Secondo i tempi del coordinatore."],
        ["<b>KA153</b> Mobilità degli youth workers",
         "Organizzazioni del settore Gioventù",
         "Include job shadowing per youth workers. Gestito dall'Agenzia Italiana per la Gioventù.",
         "Di norma due scadenze l'anno (febbraio, ottobre)."],
    ], [34 * mm, 32 * mm, 66 * mm, fw - 132 * mm], first_col_bold=False))
    st.append(callout(
        bullets([
            "<b>Anno 1:</b> KA122 (o ingresso in un consorzio) per fare i primi flussi e costruire storico.",
            "<b>Anno 1–2:</b> candidatura all'<b>accreditamento KA120</b> per avere budget ogni anno senza riscrivere "
            "il progetto: è lo strumento naturale per <b>ripetere</b> le mobilità (Sezione 7).",
            "<b>Settore giusto:</b> l'organizzazione d'invio deve essere ammissibile nel settore scelto (es. per "
            "Adulti deve offrire educazione/formazione agli adulti). Verificalo prima di tutto.",
        ]), title="Percorso consigliato per MaisEurope e per gli enti clienti"))

    # ------------------------------------------------ 3. canali
    st += section(3, "Come trovare l'organizzazione ospitante: i 7 canali", "Fare")
    st.append(P("Obiettivo pratico: costruire una <b>lista di 30 enti</b> nel Paese scelto, contattarli tutti, "
                "ottenere <b>10 risposte</b> e chiudere <b>3 ospitanti confermati</b> per ogni ciclo di candidatura. "
                "Ecco i canali, dal più strutturato al più personale."))
    channels = [
        ("1 · EPALE — ricerca contatti", ORANGE,
         "Piattaforma europea per l'educazione degli adulti. Ha uno strumento di ricerca partner, un elenco di "
         "organizzazioni e le richieste pubblicate da enti che cercano o offrono job shadowing.",
         ["Registrati con EU Login e crea il profilo dell'organizzazione (completo, con foto e attività).",
          "Cerca per Paese e tema; leggi le richieste di partner già pubblicate.",
          "Pubblica la tua richiesta: «Cerchiamo ospitante per job shadowing a [città], tema [X], [mese]».",
          "Scrivi a 10–15 enti con il modello di email della Sezione 11."],
         "Gli enti che pubblicano su EPALE sono già abituati a Erasmus+: rispondono più spesso e conoscono i documenti."),
        ("2 · ESEP — opportunità di mobilità", BLUE,
         "European School Education Platform (include eTwinning): ha una sezione dedicata alle opportunità di "
         "mobilità, dove scuole ed enti offrono o cercano job shadowing, insegnamento e corsi.",
         ["Accedi con EU Login; filtra per tipo (job shadowing / teaching), Paese, periodo.",
          "Rispondi alle offerte aperte e pubblica la tua.",
          "Utile soprattutto per il settore Scuola e per enti che lavorano con le scuole."],
         "Se l'ente lavora anche con giovani o scuole, usa ESEP in parallelo a EPALE."),
        ("3 · Erasmus+ Project Results Platform", TEAL,
         "Il database ufficiale dei progetti finanziati: puoi filtrare per Paese, azione (KA1/KA2), settore e tema.",
         ["Filtra: Paese focus + settore + parola chiave (es. «inclusion», «digital», «migrants»).",
          "Annota gli enti coordinatori e partner: sono organizzazioni con esperienza Erasmus+ reale.",
          "Contattali citando il loro progetto: «Abbiamo letto del vostro progetto X…»."],
         "Miniera d'oro anche per Metiva: ogni ente trovato qui è già un utente Erasmus+ (potenziale cliente)."),
        ("4 · Esperienze precedenti di partenariato o mobilità", PURPLE,
         "Partner di progetti passati, enti che vi hanno già ospitato o che avete ospitato voi.",
         ["Chiedi a ogni partner storico: «Puoi ospitarci o presentarci a 2 enti della tua rete?».",
          "Riattiva i contatti delle mobilità passate (anche quelle dei colleghi)."],
         "La presentazione calda («warm intro») ha tassi di risposta molto più alti della email a freddo."),
        ("5 · Seminari internazionali TCA", GREEN,
         "Training and Cooperation Activities: seminari, eventi di contact-making e visite di studio organizzati dalle "
         "Agenzie Nazionali. L'Agenzia italiana pubblica il calendario degli eventi finanziati per i partecipanti italiani.",
         ["Controlla periodicamente il calendario Eventi/TCA dell'Agenzia Nazionale (e, per la Gioventù, il "
          "calendario SALTO).",
          "Candidati agli eventi nel Paese focus o sul tuo tema.",
          "Torna a casa con 10–20 contatti qualificati e proponi subito un job shadowing."],
         "Costi coperti dall'Agenzia: è il canale con il miglior rapporto contatti/costo."),
        ("6 · Siti UE, gemellaggi tra città, mobilità precedenti", CORAL,
         "Reti istituzionali: città gemellate con il tuo comune, reti Europe Direct/Eurodesk, elenchi di beneficiari, "
         "rapporti nati da una mobilità precedente.",
         ["Chiedi al Comune l'elenco delle città gemellate e i referenti.",
          "Contatta associazioni attive in quelle città (spesso già abituate a scambi)."],
         "Il gemellaggio dà un «perché» istituzionale al contatto e facilita la disseminazione locale."),
        ("7 · Contatti privati", NAVY,
         "Rete personale e professionale: ex colleghi, LinkedIn, gruppi Facebook Erasmus+, italiani all'estero, "
         "Camere di commercio italiane all'estero.",
         ["Post su LinkedIn e nei gruppi: «Cerchiamo ospitante a [città] per [tema]».",
          "Chiedi alla tua community (follower MaisEurope inclusi) chi conosce enti nel Paese focus."],
         "Fonte ottima per ospitanti e, allo stesso tempo, per futuri clienti Metiva."),
    ]
    for name, col, what, steps, tip in channels:
        block = [Paragraph(f"<font color='{col.hexval()}'><b>{name}</b></font>", S["h3"]),
                 P(what)]
        block += bullets(steps, sym="→")
        block.append(Paragraph(f"<b>Consiglio:</b> {tip}", S["small"]))
        block.append(Spacer(1, 4))
        st.append(KeepTogether(block))
    st.append(callout("Altri strumenti utili: <b>SALTO-YOUTH Otlas</b> (ricerca partner Gioventù), "
                      "<b>Portale europeo per i giovani</b>, ricerca partner del <b>Funding &amp; Tenders Portal</b>, "
                      "siti delle Agenzie Nazionali del Paese focus (pubblicano eventi e beneficiari).",
                      title="Bonus"))

    # ------------------------------------------------ MAPPA 2
    st += [NextPageTemplate("land"), PageBreak()]
    st.append(MindMap(
        "Mappa mentale 2 · I 7 canali per trovare l'ospitante",
        "Obiettivo per ogni ciclo: 30 enti in lista → 10 risposte → 3 ospitanti confermati.",
        "TROVARE\nL'OSPITANTE\n30 → 10 → 3",
        [
            ("1 · EPALE", ORANGE, ["Profilo ente + EU Login", "Cerca partner per Paese/tema",
                                   "Pubblica richiesta di job shadowing"]),
            ("2 · ESEP", BLUE, ["Sezione opportunità di mobilità", "Offerte job shadowing / teaching",
                                "Ideale settore Scuola"]),
            ("3 · Project Results Platform", TEAL, ["Filtra Paese + KA1/KA2 + tema",
                                                    "Enti già esperti Erasmus+", "Contatta citando il loro progetto"]),
            ("4 · Esperienze precedenti", PURPLE, ["Partner storici ospitano o presentano",
                                                   "«Warm intro» = più risposte"]),
            ("5 · Seminari TCA", GREEN, ["Calendario eventi dell'Agenzia Nazionale", "Costi coperti",
                                         "10–20 contatti qualificati a evento"]),
            ("6 · Siti UE e gemellaggi", CORAL, ["Città gemellate del tuo Comune", "Europe Direct, Eurodesk",
                                                 "Contatti da mobilità passate"]),
            ("7 · Contatti privati", NAVY, ["LinkedIn, gruppi Erasmus+", "Ex colleghi, italiani all'estero",
                                            "Community MaisEurope"]),
            ("Dopo il contatto", GREY, ["Videochiamata di 20 minuti", "Obiettivi + date + programma giornaliero",
                                        "Firma dell'accordo di mobilità"]),
        ], MW, MH))
    st += [NextPageTemplate("port"), PageBreak()]

    # ------------------------------------------------ 4. attuarlo
    st += section(4, "Come attuarlo, passo dopo passo", "Fare")
    st.append(table([
        ["Quando", "Passo", "Output concreto"],
        ["T-12/-9 mesi", "<b>Bisogni e obiettivi.</b> Cosa deve imparare lo staff? Quale problema dell'organizzazione "
         "risolve la mobilità?", "3–5 obiettivi di apprendimento misurabili"],
        ["T-9/-6", "<b>Paese focus e ospitanti.</b> Usa i 7 canali (Sezione 3).", "Lista 30 → 10 → 3 ospitanti, "
         "lettere di disponibilità"],
        ["Febbraio", "<b>Candidatura</b> KA122 (o budget KA121) sul portale della Commissione.", "Domanda inviata"],
        ["~Giugno", "<b>Esito e convenzione</b> con l'Agenzia Nazionale.", "Contratto di sovvenzione firmato"],
        ["T-3 mesi", "<b>Accordo di mobilità</b> firmato da ente d'invio, ospitante e partecipante, con il "
         "<b>programma giornaliero</b>.", "Accordo + programma giorno per giorno"],
        ["T-2/-1", "<b>Preparazione:</b> logistica, viaggio (preferibilmente green), assicurazione, lingua, "
         "cultura, accordo sulla diffusione.", "Kit partenza del partecipante"],
        ["Durante", "<b>Svolgimento:</b> diario quotidiano, raccolta materiali, foto (con consenso), "
         "debriefing a metà percorso.", "Diario + materiali + attestato di presenza"],
        ["T+0/+1", "<b>Chiusura individuale:</b> report del partecipante (questionario UE), Europass Mobility, "
         "attestato con le date.", "Report + Europass"],
        ["T+1/+3", "<b>Trasferimento e diffusione:</b> si applicano i metodi appresi, evento/post interni ed esterni.",
         "Cambiamenti documentati, contenuti social"],
        ["Fine progetto", "<b>Rendicontazione</b> nel Beneficiary Module e report finale.", "Saldo del contributo"],
    ], [24 * mm, 92 * mm, fw - 116 * mm], first_col_bold=True))
    st.append(P("Esempio di programma giornaliero (job shadowing, 5 giorni)", "h2"))
    st.append(P("Tema esempio: <i>metodi di inclusione degli adulti con minori opportunità</i>. Il programma va "
                "costruito <b>insieme all'ospitante</b> e allegato all'accordo di mobilità.", "body"))
    st.append(table([
        ["Giorno", "Mattina", "Pomeriggio", "Risultato atteso"],
        ["Lun", "Accoglienza, presentazione dell'ente, regole interne, obiettivi condivisi",
         "Osservazione di un'attività con i beneficiari", "Mappa dell'organizzazione e dei servizi"],
        ["Mar", "Affiancamento al coordinatore dei progetti", "Intervista allo staff su metodi e strumenti",
         "Schede di 3 metodi osservati"],
        ["Mer", "Osservazione di un laboratorio / corso", "Visita a un ente della rete locale dell'ospitante",
         "Confronto tra pratiche IT e locali"],
        ["Gio", "Co-progettazione di un'attività con lo staff (o micro-sessione tenuta da noi)",
         "Analisi di strumenti digitali e di valutazione usati", "Bozza di attività da replicare in Italia"],
        ["Ven", "Restituzione: cosa porteremo a casa; feedback reciproco", "Firma attestato; idee di cooperazione futura",
         "Piano di trasferimento + idee di follow-up"],
    ], [14 * mm, 52 * mm, 52 * mm, fw - 118 * mm], first_col_bold=True))
    st.append(Spacer(1, 6))
    st.append(callout(
        bullets([
            "Accordo di mobilità (con programma giornaliero) firmato dalle tre parti",
            "Convenzione tra ente d'invio e partecipante (importi, obblighi)",
            "Assicurazione (salute, responsabilità civile, infortuni) + Tessera europea di assicurazione malattia",
            "Biglietti e ricevute di viaggio, carte d'imbarco",
            "Attestato di presenza dell'ospitante con le date esatte",
            "Europass Mobility + report del partecipante",
            "Materiali di diffusione (post, articolo, presentazione interna)",
        ], sym="☐"), title="Checklist documenti"))

    # ------------------------------------------------ 5. budget
    st += section(5, "Budget: come si calcolano i fondi", "Capire")
    st.append(P("Erasmus+ KA1 usa soprattutto <b>costi unitari</b> (importi fissi): non rimborsa le spese a piè di lista "
                "ma assegna somme forfettarie per persona, per giorno o per fascia di distanza. Gli importi esatti "
                "sono nella Guida al Programma dell'anno."))
    st.append(table([
        ["Voce", "Come si calcola", "A chi serve"],
        ["Viaggio", "Importo fisso per fascia di distanza (calcolatore distanze UE); importo maggiorato e giorni "
         "extra se si viaggia green (treno, bus, car sharing).", "Biglietti A/R"],
        ["Supporto individuale", "Importo per giorno di attività (+ giorni di viaggio), diverso per gruppo di Paese "
         "di destinazione.", "Vitto, alloggio, trasporti locali"],
        ["Supporto organizzativo", "Importo per partecipante, va all'ente d'invio.", "Preparazione, gestione, "
         "monitoraggio, diffusione (anche servizi esterni)"],
        ["Supporto all'inclusione", "Costi reali o forfait per partecipanti con minori opportunità.",
         "Accompagnatori, esigenze specifiche"],
        ["Costi eccezionali", "Costi reali (es. visti, viaggi molto costosi) se giustificati.", "Casi particolari"],
        ["Quote di iscrizione ai corsi", "Solo per i corsi strutturati, importo giornaliero con tetto massimo.",
         "Non si applica al job shadowing"],
    ], [36 * mm, 88 * mm, fw - 124 * mm], first_col_bold=True))
    st.append(Spacer(1, 6))
    st.append(callout(
        "<b>Budget di un flusso</b> = Partecipanti × [ Viaggio (fascia km) + Giorni × Supporto individuale (Paese) ] "
        "+ Partecipanti × Supporto organizzativo.<br/>"
        "Esempio di ragionamento: 2 persone × 5 giorni + 2 giorni di viaggio in Spagna = 2 viaggi della fascia "
        "di distanza corretta + 2 × 7 diarie del gruppo di Paese della Spagna + 2 quote di supporto organizzativo. "
        "Inserisci i valori unitari ufficiali dell'anno per ottenere la cifra.",
        title="Formula da memorizzare"))
    st.append(P("Il supporto organizzativo è la voce che finanzia la <b>gestione</b> del progetto: è da qui che un "
                "ente può pagare servizi esterni (es. supporto alla gestione). Va speso in modo coerente con il "
                "progetto e documentabile."))

    # ------------------------------------------------ 6. benefici
    st += section(6, "I benefici", "Perché farlo")
    st.append(table([
        ["Per chi", "Benefici concreti"],
        ["Partecipante", "Competenze professionali nuove, lingua, fiducia, rete personale europea, Europass Mobility "
         "spendibile nel CV."],
        ["Organizzazione d'invio", "Metodi e strumenti nuovi, qualità dei servizi, staff motivato, dimensione "
         "internazionale, storico per accreditamento e per partenariati KA2."],
        ["Organizzazione ospitante", "Sguardo esterno sul proprio lavoro, visibilità internazionale, partner per "
         "futuri progetti, possibilità di mandare il proprio staff in Italia (reciprocità)."],
        ["Territorio e beneficiari", "Servizi migliori per adulti/giovani, contenuti e pratiche europee portati "
         "nella comunità locale."],
        ["MaisEurope (strategico)", "Rete di enti esteri qualificati, contenuti autentici per i social, autorevolezza, "
         "pipeline di clienti per Metiva e quindi ricavi ricorrenti (40%)."],
    ], [38 * mm, fw - 38 * mm], first_col_bold=True))

    # ------------------------------------------------ 7. ripetere
    st += section(7, "Ripeterlo più volte l'anno nello stesso Paese", "Scalare")
    st.append(P("L'idea: scegliere <b>un Paese focus</b> e fare <b>più flussi l'anno</b>, ogni volta presso "
                "un'<b>associazione diversa</b>. Così il Paese diventa un mercato che conosci a fondo e ogni flusso "
                "aggiunge un nodo alla rete (e un potenziale cliente Metiva)."))
    st.append(P("Come scegliere il Paese focus", "h3"))
    st += bullets([
        "<b>Densità di associazioni</b> attive in Erasmus+ (controlla la Project Results Platform).",
        "<b>Costi e collegamenti</b>: voli/treni frequenti dall'Italia, costo della vita compatibile con le diarie.",
        "<b>Lingua</b>: spagnolo/portoghese più vicini; inglese ovunque nel mondo associativo.",
        "<b>Domanda di servizi</b>: Paesi con molti enti piccoli che faticano a scrivere progetti = più clienti potenziali.",
    ])
    st.append(P("Esempio di piano annuale (Paese focus: Spagna)", "h3"))
    st.append(table([
        ["Flusso", "Mese", "Città", "Tipo di ospitante", "Tema di apprendimento", "Pers."],
        ["1", "Ott", "Valencia", "Associazione educazione adulti", "Inclusione adulti con minori opportunità", "2"],
        ["2", "Nov", "Siviglia", "Ente di orientamento al lavoro", "Metodi di orientamento e bilancio competenze", "2"],
        ["3", "Feb", "Madrid", "Centro giovanile / youth NGO", "Coinvolgimento di NEET", "2"],
        ["4", "Mar", "Bilbao", "Cooperativa sociale", "Imprenditorialità sociale", "2"],
        ["5", "Mag", "Granada", "Centro di formazione digitale", "Competenze digitali per adulti", "2"],
        ["6", "Giu", "Barcellona", "Rete/federazione di associazioni", "Gestione di progetti europei in rete", "2"],
    ], [13 * mm, 12 * mm, 22 * mm, 44 * mm, fw - 103 * mm, 12 * mm]))
    st.append(Spacer(1, 6))
    st.append(P("Regole per rendere il modello ripetibile (e approvabile)", "h3"))
    st += bullets([
        "<b>Un filo conduttore</b>: tutti i flussi rispondono agli obiettivi del Piano Erasmus/progetto dell'ente "
        "d'invio. Ogni flusso ha un tema diverso ma coerente.",
        "<b>Ospitante diverso ogni volta</b>: ogni ospitante è anche una porta d'ingresso verso 2–3 enti della sua "
        "rete («catena di referenze»): chiedi sempre una presentazione.",
        "<b>Staff a rotazione</b>: coinvolgi persone diverse; le mobilità devono avere un impatto sull'organizzazione, "
        "non solo sulle stesse due persone.",
        "<b>Strumento giusto</b>: con KA122 (fino a 30 partecipanti per progetto) copri un anno di flussi; con "
        "l'accreditamento KA121 hai budget ogni anno. Più enti d'invio diversi (es. associazioni partner italiane) "
        "moltiplicano i flussi possibili.",
        "<b>CRM</b>: ogni ente contattato entra in un foglio/CRM con stato, temi, bisogni e prossima azione (Sezione 11).",
        "<b>Reciprocità</b>: offri agli ospitanti di accogliere il loro staff in Italia (mobilità in entrata) tramite "
        "la rete MaisEurope. È il modo più forte per consolidare la relazione.",
    ])

    # ------------------------------------------------ 8. funnel
    st += section(8, "Dall'ospitante al cliente Metiva: il funnel e il 40%", "Monetizzare")
    st.append(P("Il principio: <b>prima il valore, poi la proposta</b>. Durante la mobilità si costruisce fiducia "
                "lavorando bene; la proposta commerciale arriva <b>dopo</b>, in un momento separato, solo se "
                "l'ente ha un bisogno reale."))
    st.append(Funnel([
        ("Enti contattati", "≈ 30 per ciclo (7 canali)", BLUE),
        ("Ospitanti confermati", "≈ 6 l'anno (uno per flusso)", TEAL),
        ("Relazioni attive", "+ 2–3 enti presentati da ogni ospitante", GREEN),
        ("Call di scoperta bisogni", "dopo la mobilità, fuori dalle ore finanziate", ORANGE),
        ("Proposta Metiva", "servizio su misura, prezzo chiaro", PURPLE),
        ("Cliente Metiva", "contratto firmato → 40% a MaisEurope", CORAL),
    ], fw, 175))
    st.append(Spacer(1, 6))
    st.append(P("Servizi Metiva proponibili (adattare al catalogo reale)", "h3"))
    st += bullets([
        "Scrittura e invio di candidature KA122 / KA153 per l'ente estero (o per i suoi partner).",
        "Percorso di accreditamento Erasmus (KA120) e gestione annuale KA121.",
        "Progettazione di partenariati su piccola scala (KA210) e di cooperazione (KA220), con MaisEurope/enti "
        "italiani come partner.",
        "Gestione, monitoraggio e rendicontazione (Beneficiary Module), formazione dello staff.",
        "Organizzazione di mobilità in entrata in Italia per lo staff dell'ente (accoglienza, programma, rete locale).",
    ])
    st.append(P("Il modello economico del 40% (scenari ipotetici)", "h3"))
    st.append(P("V = valore medio di un contratto Metiva. I numeri sotto sono <b>esempi</b>: sostituiscili con i "
                "prezzi reali Metiva e con i tuoi tassi di conversione dopo il primo anno.", "small"))
    st.append(table([
        ["Scenario", "Enti in relazione / anno", "Conv.", "Clienti", "Valore medio (V)", "Fatturato Metiva",
         "Quota 40%"],
        ["Prudente", "18 (6 ospitanti × 3)", "10%", "≈2", "2.500 €", "5.000 €", "2.000 €"],
        ["Medio", "24 (6 × 4)", "20%", "≈5", "3.000 €", "15.000 €", "6.000 €"],
        ["Ambizioso", "36 (9 flussi × 4)", "25%", "9", "3.500 €", "31.500 €", "12.600 €"],
    ], [23 * mm, 38 * mm, 15 * mm, 15 * mm, 26 * mm, 28 * mm, fw - 145 * mm], first_col_bold=True))
    st.append(Spacer(1, 4))
    st.append(callout(
        "Un cliente soddisfatto ricompra ogni anno (nuova candidatura, gestione KA121, nuovo partenariato) e "
        "presenta altri enti. Il valore vero non è il primo contratto ma il <b>valore nel tempo</b>: "
        "LTV ≈ V × anni di permanenza × (1 + referenze). Misura: clienti che rinnovano, referenze per cliente.",
        title="Ricorrenza: dove sta il guadagno"))
    st.append(P("KPI da monitorare ogni trimestre", "h3"))
    st += bullets([
        "Enti contattati / risposte / ospitanti confermati (30 → 10 → 3).",
        "Presentazioni ottenute per ogni ospitante (obiettivo ≥ 2).",
        "Call di scoperta svolte, proposte inviate, contratti chiusi (tasso di conversione).",
        "Valore chiuso con Metiva e quota 40% maturata/incassata.",
        "Rinnovi e referenze generate dai clienti.",
    ])

    # ------------------------------------------------ 9. circolo
    st.append(PageBreak())
    st += section(9, "Il circolo virtuoso", "Il sistema")
    st.append(P("Ogni giro del cerchio produce <b>apprendimento</b> (per lo staff), <b>relazioni</b> (per la rete), "
                "<b>contenuti</b> (per MaisEurope) e <b>ricavi</b> (Metiva + 40%). Il giro successivo parte più forte "
                "del precedente."))
    st.append(Cycle([
        ("Trova", "Ospitanti nel Paese focus con i 7 canali", ORANGE),
        ("Ospita / parti", "Job shadowing o teaching di qualità", TEAL),
        ("Dai valore", "Reciprocità, idee di progetto, visibilità", GREEN),
        ("Scopri bisogni", "Call separata dopo la mobilità", BLUE),
        ("Metiva", "Servizio su misura all'ente", PURPLE),
        ("40%", "Quota MaisEurope sul chiuso", CORAL),
        ("Racconta", "Contenuti social e casi di successo", NAVY),
        ("Referenze", "Il cliente presenta nuovi enti", GREY),
    ], "CIRCOLO\nVIRTUOSO\nMaisEurope\n× Metiva", fw, 470))
    st.append(Spacer(1, 6))
    st.append(table([
        ["Giro", "Cosa succede"],
        ["Anno 1", "6 flussi, 6 ospitanti, ~20 enti in relazione, primi 2–5 clienti Metiva. Contenuti social da ogni "
         "flusso."],
        ["Anno 2", "I clienti dell'anno 1 rinnovano e presentano nuovi enti; si avviano partenariati KA210/KA220 con "
         "partner italiani; si ospita staff estero in Italia."],
        ["Anno 3", "Il Paese focus è un mercato presidiato: si replica lo stesso modello in un secondo Paese."],
    ], [20 * mm, fw - 20 * mm], first_col_bold=True))

    # ------------------------------------------------ MAPPA 3
    st += [NextPageTemplate("land"), PageBreak()]
    st.append(MindMap(
        "Mappa mentale 3 · Strategia MaisEurope × Metiva",
        "Dal Paese focus al cliente ricorrente: cosa fare, in che ordine, entro quali regole.",
        "PAESE FOCUS\n→ OSPITANTI\n→ CLIENTI METIVA",
        [
            ("Scegli il Paese", BLUE, ["Molte associazioni Erasmus+", "Voli/treni e costi sostenibili",
                                       "Lingua accessibile", "Enti piccoli = domanda di servizi"]),
            ("Pianifica i flussi", TEAL, ["6+ flussi l'anno, città diverse", "Ospitante diverso ogni volta",
                                          "Temi coerenti col Piano Erasmus", "Staff a rotazione"]),
            ("Crea valore", GREEN, ["Programma di qualità", "Reciprocità: li ospiti in Italia",
                                    "Idee di partenariato KA2", "Visibilità sui canali MaisEurope"]),
            ("Converti", PURPLE, ["Call di scoperta dopo la mobilità", "Proposta Metiva su misura",
                                  "Contratto scritto e prezzo chiaro"]),
            ("Guadagna", CORAL, ["40% del chiuso a MaisEurope", "Rinnovi annuali = ricorrenza",
                                 "Referenze = nuovi enti"]),
            ("Misura", ORANGE, ["30 → 10 → 3 ospitanti", "≥2 presentazioni per ospitante",
                                "Conversione e valore chiuso"]),
            ("Rispetta le regole", NAVY, ["Nessuna vendita nelle ore finanziate", "Ospitare non è mai condizionato",
                                          "Conflitti d'interesse dichiarati", "GDPR sui contatti"]),
        ], MW, MH))
    st += [NextPageTemplate("port"), PageBreak()]

    # ------------------------------------------------ 10. compliance
    st += section(10, "Regole d'oro e compliance", "Proteggere il modello")
    st.append(P("Il modello funziona solo se resta <b>pulito</b>: un problema con l'Agenzia Nazionale (fondi "
                "revocati, reputazione) costerebbe molto più di qualunque commissione. Queste regole sono il recinto."))
    rules = [
        ("La mobilità è apprendimento, non una trasferta commerciale.",
         "Obiettivi e programma giornaliero devono essere reali e coerenti con il progetto. Nessuna attività di "
         "vendita durante le ore finanziate; la proposta Metiva avviene dopo, in un momento separato e non "
         "rendicontato."),
        ("Ospitare non è mai condizionato.",
         "Non si chiede all'ospitante di acquistare servizi per ospitarvi, né gli si fa pagare l'ospitalità. Se "
         "l'ente non diventa cliente, la relazione resta comunque di valore."),
        ("Trasparenza sui ruoli.",
         "Dichiara chi è MaisEurope, chi è Metiva e che esiste un accordo commerciale tra loro. Se Metiva scrive un "
         "progetto in cui MaisEurope o enti collegati sono partner, rendilo esplicito (conflitto di interessi)."),
        ("Contratti scritti.",
         "Accordo MaisEurope–Metiva sul 40% (segnalazione/procacciamento o partnership commerciale) con base di "
         "calcolo, tempi di pagamento, durata, esclusive. Fatturazione corretta: verificare con il commercialista."),
        ("Compensi chiari per i clienti.",
         "Preferire tariffe fisse per servizio, pagate dall'ente con fondi propri o con voci ammissibili (es. supporto "
         "organizzativo). Evitare formule opache legate a percentuali del contributo UE: chiarire con l'Agenzia "
         "Nazionale in caso di dubbio."),
        ("Nessun doppio finanziamento.",
         "La stessa attività non può essere pagata due volte con fondi UE. I viaggi di sviluppo commerciale si "
         "pagano con fondi propri."),
        ("Dati personali (GDPR).",
         "Contatti raccolti con consenso, informativa privacy, uso coerente (niente newsletter senza consenso), "
         "liberatorie per foto e video."),
        ("Qualità prima della quantità.",
         "Rispetta gli Standard di qualità Erasmus+: buona preparazione, accompagnamento, riconoscimento dei "
         "risultati, diffusione. È anche ciò che rende credibile Metiva."),
    ]
    for i, (t, d) in enumerate(rules, 1):
        st.append(KeepTogether([Paragraph(f"<font color='{CORAL.hexval()}'><b>{i}.</b></font> <b>{t}</b>", S["body"]),
                                Paragraph(d, S["bullet"]), Spacer(1, 2)]))

    # ------------------------------------------------ 11. modelli
    st += section(11, "Modelli pronti all'uso", "Copia e usa")
    st.append(P("A · Email di primo contatto (inglese)", "h3"))
    st.append(callout(
        "<b>Subject:</b> Erasmus+ job shadowing request – [your organisation], [month/year]<br/><br/>"
        "Dear [Name],<br/>"
        "I am [name], [role] at [organisation], an Italian [type of organisation] working on [topic]. We found you "
        "through [EPALE / your Erasmus+ project \"X\" / a TCA seminar / name of contact].<br/><br/>"
        "We are planning an Erasmus+ KA1 job shadowing of [2] staff members for [5] days in [month], focused on "
        "[learning topic]. We would love to observe how you [specific practice].<br/><br/>"
        "All costs are covered by our Erasmus+ grant: we only ask for your time and a short daily programme that "
        "we can build together. In return, we are happy to host your staff in Italy, share our methods and "
        "explore future cooperation.<br/><br/>"
        "Would you be available for a 20-minute call next week?<br/>Kind regards, [signature]",
        color=BLUE, bg=LIGHT))
    st.append(P("B · Stessa email (italiano, per riferimento interno)", "h3"))
    st.append(callout(
        "Oggetto: Richiesta di job shadowing Erasmus+ – [ente], [mese/anno]. Mi presento, spiego come vi ho "
        "trovato, propongo [2] persone per [5] giorni a [mese] sul tema [X], chiarisco che i costi sono coperti "
        "dal nostro contributo Erasmus+ e che chiediamo solo tempo e un programma giornaliero da costruire "
        "insieme; offro reciprocità (ospitare il loro staff in Italia) e propongo una call di 20 minuti.",
        color=BLUE, bg=LIGHT))
    st.append(P("C · Struttura del programma giornaliero (da allegare all'accordo)", "h3"))
    st.append(table([
        ["Campo", "Cosa scrivere"],
        ["Intestazione", "Ente d'invio, ospitante, partecipante, date, tipo di attività (job shadowing / teaching)"],
        ["Obiettivi", "3–5 risultati di apprendimento (conoscenze, abilità, competenze)"],
        ["Giorno per giorno", "Orario, attività, referente dell'ospitante, metodo (osservazione, affiancamento, "
         "sessione tenuta)"],
        ["Verifica", "Come si valuta l'apprendimento (diario, restituzione finale, prodotto)"],
        ["Riconoscimento", "Europass Mobility, attestato, eventuale certificazione interna"],
        ["Firme", "Ente d'invio, ospitante, partecipante"],
    ], [34 * mm, fw - 34 * mm], first_col_bold=True))
    st.append(P("D · Script della call di scoperta (dopo la mobilità, 25 minuti)", "h3"))
    st += bullets([
        "<b>Ringraziare e restituire</b> (5'): cosa abbiamo imparato, cosa abbiamo già applicato.",
        "<b>Capire la loro situazione</b> (10'): «Avete un accreditamento Erasmus+? Quante candidature fate l'anno? "
        "Chi le scrive? Cosa vi ha frenato finora? Che progetto vorreste fare nei prossimi 12 mesi?»",
        "<b>Proporre il prossimo passo</b> (5'): reciprocità (ospitarli in Italia) e/o idea di partenariato.",
        "<b>Solo se c'è un bisogno</b> (5'): «Lavoriamo con Metiva, che fa proprio questo: vi preparo una proposta?»",
    ], sym="→")
    st.append(P("E · Campi minimi del CRM", "h3"))
    st.append(table([
        ["Campo", "Esempio"],
        ["Ente / città / Paese", "Asociación X – Valencia – ES"],
        ["Canale di origine", "EPALE / TCA / referenza di [ente]"],
        ["Stato", "Contattato · Risposto · Ospitante · Relazione attiva · Proposta · Cliente · Rinnovo"],
        ["Esperienza Erasmus+", "Nessuna / KA122 / Accreditato / KA2"],
        ["Bisogni emersi", "Scrittura progetti, rendicontazione, partner italiani"],
        ["Consenso privacy", "Sì, data"],
        ["Prossima azione + data", "Call di scoperta il [data]"],
        ["Valore / 40%", "Contratto 3.000 € → 1.200 €"],
    ], [42 * mm, fw - 42 * mm], first_col_bold=True))

    # ------------------------------------------------ 12. ripasso
    st += section(12, "Ripasso: domande-flash, glossario, link utili", "Studiare")
    qa = [
        ("Qual è la differenza tra job shadowing e teaching assignment?",
         "Nel job shadowing osservi/affianchi (2–60 gg); nel teaching assignment insegni o formi (2–365 gg)."),
        ("Chi chiede i fondi?", "L'organizzazione d'invio, nel suo progetto KA1 (KA122, KA121 o tramite consorzio)."),
        ("L'ospitante paga qualcosa?", "No. Dedica tempo e costruisce con te il programma giornaliero."),
        ("Quali sono i due elementi indispensabili?", "Un ospitante in un Paese aderente e un programma giornaliero "
                                                       "concordato."),
        ("Quali sono i 7 canali per trovare l'ospitante?", "EPALE, ESEP, Project Results Platform, esperienze "
         "precedenti, seminari TCA, siti UE/gemellaggi/mobilità precedenti, contatti privati."),
        ("Quale strumento permette di ripetere le mobilità ogni anno?", "L'accreditamento Erasmus (KA120) e i "
         "relativi progetti annuali KA121."),
        ("Quali sono le voci di budget principali?", "Viaggio, supporto individuale, supporto organizzativo "
         "(+ inclusione e costi eccezionali)."),
        ("Quali documenti chiudono la mobilità?", "Attestato di presenza, Europass Mobility, report del "
         "partecipante, materiali di diffusione."),
        ("Quando si propone Metiva?", "Dopo la mobilità, in una call separata, solo se emerge un bisogno reale."),
        ("Come si calcola la quota MaisEurope?", "40% del valore dei contratti chiusi con Metiva, secondo "
         "l'accordo scritto."),
        ("Cosa rende il modello un circolo virtuoso?", "Ogni ospitante porta referenze, ogni cliente rinnova e "
         "presenta altri enti, ogni flusso genera contenuti che attirano nuovi contatti."),
        ("Qual è la regola d'oro?", "L'apprendimento reale viene prima: niente vendita nelle ore finanziate, "
         "ospitalità mai condizionata, contratti trasparenti."),
    ]
    st.append(table([["#", "Domanda", "Risposta (coprila e prova a rispondere)"]] +
                    [[str(i), q, a] for i, (q, a) in enumerate(qa, 1)],
                    [8 * mm, 62 * mm, fw - 70 * mm]))
    st.append(P("Glossario essenziale", "h2"))
    st.append(table([
        ["Termine", "Significato"],
        ["KA1", "Azione chiave 1 di Erasmus+: mobilità individuale per l'apprendimento."],
        ["KA120 / KA121", "Accreditamento Erasmus / progetti annuali per enti accreditati."],
        ["KA122", "Progetti di mobilità a breve termine (senza accreditamento)."],
        ["KA153", "Mobilità degli youth workers (settore Gioventù)."],
        ["KA210 / KA220", "Partenariati su piccola scala / partenariati di cooperazione (KA2)."],
        ["Agenzia Nazionale (AN)", "Gestisce il programma in Italia: INDIRE, INAPP, Agenzia Italiana per la Gioventù."],
        ["EPALE", "Piattaforma elettronica per l'educazione degli adulti in Europa."],
        ["ESEP", "European School Education Platform (include eTwinning)."],
        ["TCA", "Training and Cooperation Activities: seminari ed eventi di contatto delle Agenzie Nazionali."],
        ["Europass Mobility", "Documento europeo che certifica le competenze acquisite durante la mobilità."],
        ["Beneficiary Module", "Strumento online per gestire e rendicontare le mobilità."],
        ["Costi unitari", "Importi fissi (per persona, giorno, fascia km) usati per calcolare il contributo."],
    ], [38 * mm, fw - 38 * mm], first_col_bold=True))
    st.append(P("Link utili (verifica sempre le pagine ufficiali)", "h2"))
    st += bullets([
        "Guida al Programma Erasmus+ e inviti: <b>erasmus-plus.ec.europa.eu</b>",
        "Portale italiano Erasmus+ (INDIRE, INAPP, Agenzia Gioventù): <b>erasmusplus.it</b>",
        "EPALE: <b>epale.ec.europa.eu</b>",
        "ESEP: <b>school-education.ec.europa.eu</b>",
        "Erasmus+ Project Results Platform: <b>erasmus-plus.ec.europa.eu/projects</b>",
        "Agenzia Italiana per la Gioventù: <b>agenziagioventu.gov.it</b>",
        "SALTO-YOUTH (Otlas, European Training Calendar): <b>salto-youth.net</b>",
        "Funding &amp; Tenders Portal (ricerca partner e candidature): <b>ec.europa.eu/info/funding-tenders</b>",
    ])
    st.append(Spacer(1, 8))
    st.append(callout("1) Scegli il Paese focus. 2) Costruisci la lista di 30 enti con i 7 canali. 3) Verifica la "
                      "strada di finanziamento e la prossima scadenza (KA122: febbraio). 4) Firma l'accordo scritto "
                      "MaisEurope–Metiva sul 40%. 5) Imposta il CRM e i KPI.",
                      color=CORAL, bg=colors.HexColor("#FDEEE9"), title="Prossimi 5 passi (questa settimana)"))

    doc.build(st)
    print("PDF creato:", OUT)


if __name__ == "__main__":
    build()
