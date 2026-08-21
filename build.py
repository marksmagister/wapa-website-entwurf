#!/usr/bin/env python3
"""Baut die ausgelieferte Fassung aus der Quelle im selben Repo.

    python3 build.py              # nur index.html
    python3 build.py --assets     # zusätzlich die Bilder aus src/originals/

Quelle ist `src/website.html`. Alles im Wurzelverzeichnis (`index.html`,
`assets/*.jpg`) ist daraus **abgeleitet** und wird bei jedem Lauf überschrieben —
niemals von Hand bearbeiten.

`--assets` erzeugt die Webfassungen aus `src/originals/` (längste Kante 1500 px,
JPEG 78) und entfernt anschließend alles, was `index.html` nicht referenziert.
Ohne den Schalter bleibt `assets/` unangetastet; das ist der Normalfall, weil
Bilder sich selten ändern. Braucht Pillow.
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

    vault = os.path.join(hier, "src", "originals")
    if not os.path.isdir(vault):
        sys.exit("Originalordner nicht gefunden: " + vault)

    uebersprungen = []

    def einpassen(src, dst):
        """Ein Original auf Webgröße bringen.

        Gibt 0 zurück, wenn die Datei nicht lesbar ist. Das kommt vor: macOS
        bindet Dateien aus iCloud per `com.apple.macl` an den Ort, an dem sie
        angelegt wurden. Wird eine solche Datei verschoben, verliert ein
        Hintergrundprozess den Zugriff — die Datei ist unversehrt, nur für uns
        nicht mehr zu öffnen. Dann bleibt die bereits erzeugte Webfassung stehen,
        statt dass der ganze Lauf abbricht."""
        try:
            im = Image.open(src); im = ImageOps.exif_transpose(im).convert("RGB")
        except (PermissionError, OSError) as e:
            uebersprungen.append((os.path.basename(src), type(e).__name__))
            return 0
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

    print("Bilder erzeugt: %d Dateien, %.1f MB" % (anzahl - len(uebersprungen), gesamt / 1048576))
    if uebersprungen:
        print("  %d Originale nicht lesbar, vorhandene Webfassung behalten:" % len(uebersprungen))
        for name, art in uebersprungen[:4]:
            print("    %s (%s)" % (name, art))
        if len(uebersprungen) > 4:
            print("    … und %d weitere" % (len(uebersprungen) - 4))
    aufraeumen(hier, schonen=bool(uebersprungen))

def aufraeumen(hier, schonen=False):
    """Bilder entfernen, die index.html nicht referenziert.

    Die Originale liegen im Vault; hier gehört nur hinein, was die Seite braucht.
    Git bewahrt jede je eingecheckte Fassung für immer auf — ungenutzte Dateien
    wären dauerhafter Ballast."""
    idx = os.path.join(hier, "index.html")
    if not os.path.exists(idx):
        return
    s = io.open(idx, encoding="utf-8").read()
    genutzt = set(re.findall(r"['\"](assets/[^'\"]+\.jpg)['\"]", s))
    if schonen:
        print("  Aufräumen übersprungen — es waren nicht alle Originale lesbar.")
        return
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
        print("  %d ungenutzte Bilder entfernt" % weg)

if __name__ == "__main__":
    hier = os.path.dirname(os.path.abspath(__file__))
    # Pfad ist optional — Vorgabe ist die Quelle im Repo
    argumente = [a for a in sys.argv[1:] if not a.startswith("--")]
    quelle = argumente[0] if argumente else os.path.join(hier, "src", "website.html")
    if not os.path.exists(quelle):
        sys.exit("Quelle nicht gefunden: " + quelle)
    html_bauen(quelle, hier)
    if "--assets" in sys.argv:
        bilder_bauen(quelle, hier)
