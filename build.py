#!/usr/bin/env python3
"""Baut aus dem Entwurf im Vault die statische Fassung für GitHub Pages.

    python3 build.py "/Pfad/zu/Website-Entwurf-final.html"

Ersetzt die externen Abhängigkeiten durch lokale Dateien: Fotos, Archivbilder,
Logo und Schriften liegen alle unter assets/. Bilder werden dabei nicht neu
heruntergeladen — die liegen bereits im Repo. Es wird nur die HTML umgeschrieben.
"""
import io, re, sys, os

quelle = sys.argv[1] if len(sys.argv) > 1 else None
if not quelle or not os.path.exists(quelle):
    sys.exit("Quelle fehlt. Aufruf: python3 build.py <Website-Entwurf-final.html>")

hier = os.path.dirname(os.path.abspath(__file__))
s = io.open(quelle, encoding="utf-8").read()

# Google Fonts raus, lokale Schriften rein
s = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", s)
s = re.sub(r'<link href="https://fonts\.googleapis\.com[^"]*" rel="stylesheet">',
           '<link rel="stylesheet" href="fonts.css">', s)

# Suchmaschinen aussperren — das hier ist ein Entwurf
if "noindex" not in s:
    s = s.replace('<meta name="viewport"',
                  '<meta name="robots" content="noindex, nofollow">\n<meta name="viewport"', 1)

# Fotos: N('20.32.45') -> assets/fotos/20-32-45.jpg
def slug(t):
    for a, b in (("%20", ""), ("%28", ""), ("%29", ""), (" ", ""), ("(", ""), (")", ""), (".", "-")):
        t = t.replace(a, b)
    return t
s = re.sub(r"N\('([^']+)'\)", lambda m: "'assets/fotos/%s.jpg'" % slug(m.group(1)), s)
s = re.sub(r"const N = [^;]+;\s*", "", s)

# Aufnahmen aus der Präsentation Projektbedarf
s = re.sub(r"P\('([^']+)'\)", lambda m: "'assets/fotos-2026/%s.jpg'" % m.group(1), s)
s = re.sub(r"const P = [^;]+;\s*", "", s)

# Archivbilder: der Schlüsselname ist der Dateiname
s = re.sub(r"^(\s*)(\w+):\s*W\('[^']+'\)", r"\1\2: 'assets/archiv/\2.jpg'", s, flags=re.M)
s = re.sub(r"const W = [^;]+;\s*", "", s)

# Logo
s = re.sub(r"https://gemeinsamfuerwapa\.de/wp-content/uploads/2018/07/gemeinsam-fuer-wapa-logo\.jpg",
           "assets/logo.jpg", s)

io.open(os.path.join(hier, "index.html"), "w", encoding="utf-8").write(s)

rest = re.findall(r'https?://(?!www\.betterplace|www\.instagram|www\.facebook|www\.linkedin)[^"\')\s]+', s)
print("index.html geschrieben.")
print("verbleibende externe Verweise:", sorted(set(rest)) or "keine")
