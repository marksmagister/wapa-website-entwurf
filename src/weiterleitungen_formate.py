# -*- coding: utf-8 -*-
"""Erzeugt aus weiterleitungen.csv die Dateien, die der jeweilige Host braucht.

    python3 src/weiterleitungen_formate.py

Schreibt nach build/:
  .htaccess          Apache — die meisten deutschen Hoster
  _redirects         Netlify, Cloudflare Pages
  nginx.conf         nginx
  weiterleitungen/   HTML-Weichen, falls der Host gar nichts davon kann
                     (z. B. GitHub Pages)

Alle Pfade sind **relativ**. Die Karte gilt unverändert, egal ob die Seite unter
gemeinsamfuerwapa.de, einer Vorschauadresse oder sonstwo läuft.
"""
import csv, os, io, sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
ZIEL = os.path.join(REPO, "build")

PFADE = "--pfade" in sys.argv   # echte Pfade statt Hash-Adressen

def ziel(neu):
    """#/aktuelles/x  ->  /#/aktuelles/x   bzw. mit --pfade  ->  /aktuelles/x/"""
    rest = neu[2:] if neu.startswith("#/") else neu.lstrip("/")
    if PFADE:
        return "/" + rest + ("/" if rest else "")
    return "/#/" + rest

zeilen = [r for r in csv.DictReader(io.open(os.path.join(HIER, "weiterleitungen.csv"), encoding="utf-8"))
          if r["neu"]]
# Nur die Wurzel selbst fliegt raus — sie zeigt auf sich, das wäre eine Schleife.
# Alles andere, was auf die Startseite zeigt (etwa die Theme-Reste), bleibt.
zeilen = [r for r in zeilen if r["alt"].strip("/") != ""]
for r in zeilen:
    r["ziel"] = ziel(r["neu"])
os.makedirs(ZIEL, exist_ok=True)

# Apache
with io.open(os.path.join(ZIEL, ".htaccess"), "w", encoding="utf-8") as f:
    f.write("# Weiterleitungen von der alten WordPress-Struktur.\n"
            "# Erzeugt aus src/weiterleitungen.csv — nicht von Hand pflegen.\n\n"
            "<IfModule mod_rewrite.c>\n  RewriteEngine On\n\n")
    for r in zeilen:
        # NE ist wesentlich: ohne den Schalter kodiert Apache das # zu %23
        f.write("  RewriteRule ^%s/?$ %s [R=301,L,NE]\n" % (r["alt"].strip("/").replace(".", r"\."), r["ziel"]))
    f.write("</IfModule>\n")

# Netlify / Cloudflare Pages
with io.open(os.path.join(ZIEL, "_redirects"), "w", encoding="utf-8") as f:
    f.write("# Erzeugt aus src/weiterleitungen.csv — nicht von Hand pflegen.\n")
    for r in zeilen:
        f.write("%-52s %s  301\n" % (r["alt"], r["ziel"]))

# nginx
with io.open(os.path.join(ZIEL, "nginx.conf"), "w", encoding="utf-8") as f:
    f.write("# Erzeugt aus src/weiterleitungen.csv — nicht von Hand pflegen.\n")
    for r in zeilen:
        f.write("rewrite ^%s/?$ %s permanent;\n" % (r["alt"].rstrip("/"), r["ziel"]))

# HTML-Weichen für Hosts ohne Weiterleitungen
VORLAGE = """<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<title>Umgezogen</title>
<link rel="canonical" href="%(ziel)s">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=%(ziel)s">
<script>location.replace("%(ziel)s")</script>
</head><body style="font-family:system-ui;padding:2rem">
<p>Diese Seite ist umgezogen. <a href="%(ziel)s">Hier geht es weiter.</a></p>
</body></html>
"""
n = 0
for r in zeilen:
    pfad = os.path.join(ZIEL, "weiterleitungen", r["alt"].strip("/"))
    os.makedirs(pfad, exist_ok=True)
    io.open(os.path.join(pfad, "index.html"), "w", encoding="utf-8").write(VORLAGE % r)
    n += 1

print("Weiterleitungen: %d  (%s)" % (len(zeilen), "echte Pfade" if PFADE else "Hash-Adressen"))
print("geschrieben nach build/: .htaccess · _redirects · nginx.conf · %d HTML-Weichen" % n)
