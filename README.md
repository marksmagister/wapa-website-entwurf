# Gemeinsam für Wapa — Website-Entwurf

Gestaltungsentwurf für die neue Website von **Gemeinsam für Wapa e. V.**
(Stand August 2026). **Kein Livebetrieb, keine offizielle Vereinsseite.**

Die Seite dient dem Vorstand als Diskussionsgrundlage. Über die Leiste am
oberen Rand lassen sich **Randnotizen einblenden**, die jede Abweichung vom
bisherigen Auftritt begründen. Sie sind standardmäßig aus.

## Neu bauen
Der Entwurf wird im Vault gepflegt, nicht hier. Nach Änderungen:

    python3 build.py "…/Gemeinsam für Wapa Website/Website-Entwurf-final.html"

Das Skript schreibt `index.html` neu und hängt die Seite von den lokalen
Dateien unter `assets/` ab. Bilder werden nicht erneut geladen.

## Was hier drin steckt
- `index.html` — der gesamte Entwurf (eine Datei, Ansichten über `#/…`)
- `fonts.css` + `assets/fonts/` — Fraunces und Atkinson Hyperlegible,
  selbst gehostet statt über Google Fonts
- `assets/fotos/` — Aufnahmen aus dem Waldgarten, August 2026
- `assets/archiv/` — ältere Bilder aus der bestehenden Website

## Hinweise
- `noindex, nofollow` und `robots.txt` sind gesetzt: Die Seite soll nicht in
  Suchmaschinen auftauchen.
- Der Beitrag *So sieht der Waldgarten heute aus* ist ein **Textvorschlag**
  und vom Verein nicht abgenommen.
- Die Zuordnung Foto → Projekt ist teils geraten und muss geprüft werden.
- Offene Punkte für den Vorstand stehen im Vault unter
  `Offene Entscheidungen.md`.
