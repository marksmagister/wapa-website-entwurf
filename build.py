#!/usr/bin/env python3
"""Baut die statische Fassung für GitHub Pages aus dem Entwurf im Vault.

    python3 build.py <Pfad zu Website-Entwurf-final.html>          # nur HTML
    python3 build.py <Pfad ...> --assets                            # auch Bilder neu

Der Entwurf im Vault ist das Original. `index.html` hier ist abgeleitet und wird
bei jedem Lauf überschrieben — niemals von Hand bearbeiten.

Mit `--assets` werden die Bilder aus den Originalen im Vault-Ordner
`other assets/` neu erzeugt und auf Webgröße gebracht. Ohne den Schalter bleibt
`assets/` unangetastet; das ist der Normalfall, weil Bilder sich selten ändern.
"""
import io, re, sys, os, shutil

BREITE   = 1500   # längste Kante der Webfassung
QUALITAET = 78

def slug(t):
    for a, b in (("%20",""),("%28",""),("%29",""),(" ",""),("(",""),(")",""),(".","-")):
        t = t.replace(a, b)
    return t

def html_bauen(quelle, hier):
    s = io.open(quelle, encoding="utf-8").read()

    s = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", s)
    s = re.sub(r'<link href="https://fonts\.googleapis\.com[^"]*" rel="stylesheet">',
               '<link rel="stylesheet" href="fonts.css">', s)
    if "noindex" not in s:
        s = s.replace('<meta name="viewport"',
                      '<meta name="robots" content="noindex, nofollow">\n<meta name="viewport"', 1)

    s = re.sub(r"N\('([^']+)'\)", lambda m: "'assets/fotos/%s.jpg'" % slug(m.group(1)), s)
    s = re.sub(r"const N = [^;]+;\s*", "", s)
    s = re.sub(r"P\('([^']+)'\)", lambda m: "'assets/fotos-2026/%s.jpg'" % m.group(1), s)
    s = re.sub(r"const P = [^;]+;\s*", "", s)
    s = re.sub(r"^(\s*)(\w+):\s*W\('[^']+'\)", r"\1\2: 'assets/archiv/\2.jpg'", s, flags=re.M)
    s = re.sub(r"const W = [^;]+;\s*", "", s)
    s = re.sub(r"https://gemeinsamfuerwapa\.de/wp-content/uploads/2018/07/gemeinsam-fuer-wapa-logo\.jpg",
               "assets/logo.jpg", s)

    io.open(os.path.join(hier, "index.html"), "w", encoding="utf-8").write(s)
    uebrig = re.findall(r'https?://(?!www\.betterplace|www\.instagram|www\.facebook|www\.linkedin'
                        r'|www\.schwaebische|www\.suedkurier|web\.archive)[^"\')\s]+', s)
    print("index.html geschrieben.")
    if uebrig:
        print("  noch extern (prüfen):", sorted(set(uebrig))[:5])

def bilder_bauen(quelle, hier):
    """Webfassungen aus den Originalen im Vault erzeugen."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit("Pillow fehlt:  python3 -m pip install Pillow")

    vault = os.path.join(os.path.dirname(os.path.abspath(quelle)), "other assets")
    if not os.path.isdir(vault):
        sys.exit("Originalordner nicht gefunden: " + vault)

    def einpassen(src, dst):
        im = Image.open(src); im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((BREITE, BREITE), Image.LANCZOS)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        im.save(dst, "JPEG", quality=QUALITAET, optimize=True, progressive=True)
        return os.path.getsize(dst)

    gesamt = 0; anzahl = 0

    # Waldgarten-Fotos (August 2026)
    for f in os.listdir(vault):
        if f.startswith("WhatsApp Image 2026-08-12 at ") and f.endswith(".jpeg"):
            name = slug(f[len("WhatsApp Image 2026-08-12 at "):-len(".jpeg")])
            gesamt += einpassen(os.path.join(vault, f),
                                os.path.join(hier, "assets", "fotos", name + ".jpg")); anzahl += 1

    # Aufnahmen aus der Präsentation
    d = os.path.join(vault, "aus Projektbedarf 2026-08")
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".jpg"):
                gesamt += einpassen(os.path.join(d, f),
                                    os.path.join(hier, "assets", "fotos-2026", f)); anzahl += 1

    # Archivbilder von der alten Website
    d = os.path.join(vault, "aus wp-content-uploads")
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.lower().endswith((".jpg", ".jpeg")):
                name = os.path.splitext(f)[0]
                gesamt += einpassen(os.path.join(d, f),
                                    os.path.join(hier, "assets", "archiv", name + ".jpg")); anzahl += 1

    print("Bilder erzeugt: %d Dateien, %.1f MB" % (anzahl, gesamt / 1048576))
    aufraeumen(hier)

def aufraeumen(hier):
    """Bilder entfernen, die index.html nicht referenziert.

    Die Originale liegen im Vault; hier gehört nur hinein, was die Seite braucht.
    Git bewahrt jede je eingecheckte Fassung für immer auf — ungenutzte Dateien
    wären dauerhafter Ballast."""
    idx = os.path.join(hier, "index.html")
    if not os.path.exists(idx):
        return
    s = io.open(idx, encoding="utf-8").read()
    genutzt = set(re.findall(r"['\"](assets/[^'\"]+\.jpg)['\"]", s))
    weg = 0
    for ordner in ("fotos", "fotos-2026", "archiv"):
        d = os.path.join(hier, "assets", ordner)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            rel = "assets/%s/%s" % (ordner, f)
            if f.endswith(".jpg") and rel not in genutzt:
                os.remove(os.path.join(hier, rel)); weg += 1
    if weg:
        print("  %d ungenutzte Bilder entfernt (im Vault bleiben sie erhalten)" % weg)

if __name__ == "__main__":
    argumente = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not argumente or not os.path.exists(argumente[0]):
        sys.exit("Aufruf: python3 build.py <Website-Entwurf-final.html> [--assets]")
    quelle = argumente[0]
    hier = os.path.dirname(os.path.abspath(__file__))
    html_bauen(quelle, hier)
    if "--assets" in sys.argv:
        bilder_bauen(quelle, hier)
