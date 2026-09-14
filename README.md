# Gemeinsam für Wapa — Website-Entwurf

Gestaltungsentwurf für die neue Website von **Gemeinsam für Wapa e. V.**
**Kein Livebetrieb, keine offizielle Vereinsseite.**

**Live:** <https://marksmagister.github.io/wapa-website-entwurf/>

---

## Wo was liegt

| | |
|---|---|
| **Quelle** | `src/website.html` — hier wird inhaltlich gearbeitet |
| **Originalbilder** | `src/originals/` |
| **Abgeleitet** | `index.html` und `assets/*.jpg` entstehen daraus |

**`index.html` niemals von Hand ändern** — der nächste Build überschreibt sie.
Alle inhaltlichen Änderungen gehen in `src/website.html`.

## Bauen

```bash
python3 build.py
```

Das schreibt `index.html` neu: Google Fonts raus, lokale Schriften rein,
Bildpfade auf `assets/`, `noindex` gesetzt, `og:image` absolut.

Wenn sich **Bilder** geändert haben, zusätzlich `--assets`. Dann werden die
Webfassungen aus `src/originals/` erzeugt (längste Kante 1500 px, JPEG 78) und
alles gelöscht, was die Seite nicht referenziert.

```bash
python3 build.py --assets
git add -A && git commit -m "…" && git push
```

Braucht Pillow: `python3 -m pip install Pillow`

## Was sonst noch erzeugt wird

| | |
|---|---|
| `werkzeug/karte.py` | Übersichtskarten als statisches SVG → `werkzeug/karte.svg.txt`. Geodaten vorher mit `werkzeug/holen.sh` holen (bewusst nicht eingecheckt). **Noch nicht in der Seite eingebaut.** |
| `werkzeug/beitrittserklaerung.html` | Quelle der Beitrittserklärung. Rendern mit `node werkzeug/pdf.mjs` → `assets/dokumente/` |
| `werkzeug/visitenkarte.html` | Visitenkarte. Rendern mit `node werkzeug/karte-pdf.mjs` → `druck/` |
| `src/weiterleitungen.csv` | Weiterleitungen der alten WordPress-Adressen. Formate erzeugen mit `python3 src/weiterleitungen_formate.py` |

Die PDF-Skripte brauchen einen laufenden lokalen Server
(`python3 -m http.server 8899`) und Playwright.

## Warum Quelle und Ableitung getrennt sind

Git bewahrt jede eingecheckte Fassung dauerhaft auf. Ein ausgetauschtes 4-MB-Foto
belegt für immer 8 MB. Deshalb liegen die Originale unter `src/originals/` und im
Wurzelverzeichnis nur, was die Seite wirklich zeigt — verkleinert und beschnitten.
Das Repo bleibt erzeugbar, ohne dass jede Zwischenfassung eines Fotos mitwächst.

## Aufbau

- `index.html` — die ganze Seite, eine Datei. Ansichten über `#/…`
- `fonts.css` + `assets/fonts/` — Fraunces und Atkinson Hyperlegible, selbst
  gehostet. Keine Verbindung zu Google.
- `assets/fotos/` — Waldgarten, August 2026
- `assets/fotos-2026/` — aus der Präsentation *Projektbedarf* (08/2026)
- `assets/archiv/` — von der alten Website
- `assets/dokumente/` — Satzung, Manifest, Beitrittserklärung

## Stand der Inhalte

- **23 Projekte** im Register, **20 Beiträge** — alle 19 Beiträge der alten
  Website vollständig übertragen, plus ein neuer Entwurfsbeitrag von 2026.
- **7 Projekte** stammen aus Unterlagen, die nicht auf der alten Website standen.
  Sie sind mit **neu** markiert; **`#/neu`** listet sie zum Abhaken auf, samt
  der bekannten Unstimmigkeiten. Die Liste erzeugt sich aus den Daten — fällt
  das Feld `neu` weg, verschwindet der Eintrag dort von selbst.

## Bevor irgendetwas davon offiziell wird

- Der Beitrag *So sieht der Waldgarten heute aus* ist ein **Textvorschlag**,
  nicht vom Verein abgenommen.
- Das Zitat auf der Startseite ist der Quelle zugeschrieben, nicht namentlich —
  der Text auf der alten Projektseite ist nirgends gezeichnet.
- Auf der Vorstandsseite steht über eine Person nur, was der Verein oder die
  Presse über sie in ihrer Rolle veröffentlicht hat, oder was sie selbst
  beigesteuert hat. Fehlende Fotos stehen als Lücke da.
- `noindex` und `robots.txt` sind gesetzt. Die Seite soll geteilt, nicht
  gefunden werden. **Das Repo ist öffentlich** — auf einem freien GitHub-Konto
  geht Pages nicht anders.

Offene Punkte für den Vorstand: `docs/Offene Entscheidungen.md` — eine Zeile je
Entscheidung, dort und sonst nirgends.
Quellenlage und Presseberichte: `docs/Quellen und neue Inhalte.md`.
Weiterleitungen der alten Adressen: `docs/Weiterleitungskarte.md`.
