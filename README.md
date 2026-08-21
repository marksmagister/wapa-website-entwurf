# Gemeinsam für Wapa — Website-Entwurf

Gestaltungsentwurf für die neue Website von **Gemeinsam für Wapa e. V.**
**Kein Livebetrieb, keine offizielle Vereinsseite.**

**Live:** <https://marksmagister.github.io/wapa-website-entwurf/>

---

## Wo was liegt

| | |
|---|---|
| **Original** | `Projects/Gemeinsam für Wapa Website/Website-Entwurf-final.html` **im Obsidian-Vault** |
| **Originalbilder** | derselbe Ordner, Unterordner `other assets/` |
| **Dieses Repo** | abgeleitet. `index.html` und `assets/*.jpg` entstehen aus dem Original |

**`index.html` niemals von Hand ändern** — der nächste Build überschreibt sie.
Alle inhaltlichen Änderungen gehen in die Vault-Datei.

## Bauen

```bash
python3 build.py "…/Gemeinsam für Wapa Website/Website-Entwurf-final.html"
```

Das schreibt `index.html` neu: Google Fonts raus, lokale Schriften rein,
Bildpfade auf `assets/`, `noindex` gesetzt.

Wenn sich **Bilder** geändert haben, zusätzlich `--assets`. Dann werden die
Webfassungen aus den Originalen im Vault erzeugt (längste Kante 1500 px,
JPEG 78) und alles gelöscht, was die Seite nicht referenziert. Die Originale
bleiben im Vault unberührt.

```bash
python3 build.py "…/Website-Entwurf-final.html" --assets
git add -A && git commit -m "…" && git push
```

Braucht Pillow: `python3 -m pip install Pillow`

## Warum Original und Ableitung getrennt sind

Git bewahrt jede eingecheckte Fassung dauerhaft auf. Ein ausgetauschtes 4-MB-Foto
belegt für immer 8 MB. Deshalb liegen die Originale im Vault (und damit in Noahs
bestehender Sicherung), und hier nur, was die Seite wirklich zeigt. Das Repo
bleibt leicht und ist jederzeit vollständig neu erzeugbar.

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

Offene Punkte für den Vorstand: `Offene Entscheidungen.md` im Vault.
Quellenlage und Presseberichte: `Quellen und neue Inhalte.md`.
