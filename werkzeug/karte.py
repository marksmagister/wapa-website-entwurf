#!/usr/bin/env python3
"""Erzeugt die Übersichtskarte als statisches SVG.

    python3 werkzeug/karte.py            # schreibt werkzeug/karte.svg.txt

Die Karte wird EINMAL gerechnet und als fertiges SVG in die Seite eingesetzt.
Kein JavaScript, keine Geodaten zur Laufzeit, keine externe Kachel — die Seite
bleibt eine Datei und lädt nichts nach.

Quellen der Umrisse (beide frei, siehe Attribution unten):
  Ländergrenzen   Natural Earth via world.geo.json — public domain
  Provinz Sanguié geoBoundaries gbOpen ADM2 — CC BY 4.0
"""
import json, math, os, io

HIER = os.path.dirname(os.path.abspath(__file__))
ROH  = HIER  # hier liegen die heruntergeladenen GeoJSON-Dateien

# ---------------------------------------------------------------- Geometrie

def ringe(geom):
    """Alle äußeren Ringe einer Polygon/MultiPolygon-Geometrie."""
    if geom["type"] == "Polygon":
        return [geom["coordinates"][0]]
    return [p[0] for p in geom["coordinates"]]

def vereinfachen(punkte, tol):
    """Douglas-Peucker. Halbiert die Dateigröße, ohne dass man es sieht."""
    if len(punkte) < 3:
        return punkte
    a, b = punkte[0], punkte[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    laenge = math.hypot(dx, dy)
    weit, idx = 0.0, 0
    for i in range(1, len(punkte) - 1):
        p = punkte[i]
        if laenge == 0:
            d = math.hypot(p[0] - a[0], p[1] - a[1])
        else:
            d = abs(dy * p[0] - dx * p[1] + b[0] * a[1] - b[1] * a[0]) / laenge
        if d > weit:
            weit, idx = d, i
    if weit > tol:
        links  = vereinfachen(punkte[:idx + 1], tol)
        rechts = vereinfachen(punkte[idx:], tol)
        return links[:-1] + rechts
    return [a, b]

class Projektion:
    """Plattkarte mit Breitenkorrektur. Auf diesen Ausschnitten völlig ausreichend."""
    def __init__(self, lon0, lon1, lat0, lat1, breite, hoehe, rand=0):
        self.k = math.cos(math.radians((lat0 + lat1) / 2))
        x0, x1 = lon0 * self.k, lon1 * self.k
        sx = (breite - 2 * rand) / (x1 - x0)
        sy = (hoehe - 2 * rand) / (lat1 - lat0)
        self.s = min(sx, sy)
        self.ox = rand + (breite - 2 * rand - (x1 - x0) * self.s) / 2 - x0 * self.s
        self.oy = rand + (hoehe - 2 * rand - (lat1 - lat0) * self.s) / 2 + lat1 * self.s
    def __call__(self, lon, lat):
        return (lon * self.k * self.s + self.ox, self.oy - lat * self.s)

def pfad(geom, proj, tol):
    aus = []
    for ring in ringe(geom):
        r = vereinfachen(ring, tol)
        if len(r) < 3:
            continue
        pts = [proj(x, y) for x, y in r]
        aus.append("M" + "L".join("%.1f %.1f" % p for p in pts) + "Z")
    return "".join(aus)

def laden(datei):
    d = json.load(io.open(os.path.join(ROH, datei), encoding="utf-8"))
    return d["features"][0]["geometry"]

def sanguie():
    d = json.load(io.open(os.path.join(ROH, "adm2.json"), encoding="utf-8"))
    for f in d["features"]:
        if f["properties"].get("shapeName") == "Sanguie":
            return f["geometry"]
    raise SystemExit("Sanguié nicht gefunden")


def liegt_in(lon, lat, ring):
    """Punkt-in-Polygon. Fängt ab, dass eine falsch eingetippte Koordinate
    unbemerkt außerhalb der Provinz landet — beim letzten Stand traf das auf
    zwei der geschätzten Orte zu, und im fertigen Bild sieht man es kaum."""
    drin, n = False, len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if ((y1 > lat) != (y2 > lat)) and (lon < (x2-x1)*(lat-y1)/(y2-y1) + x1):
            drin = not drin
    return drin

def entfernung(a, b):
    """Großkreis in km."""
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2 * 6371 * math.asin(math.sqrt(h))

# ---------------------------------------------------------------- Orte
# `fest` sagt, ob die Koordinate belegt ist. Genau wie `neu` im Register
# steuert dieses Feld die Darstellung — wird es auf True gesetzt, ändert sich
# die Signatur von selbst und der Warnhinweis verschwindet, sobald keiner mehr
# offen ist. Kein zweites Dokument, das veralten kann.
ORTE = [
    {"name": "Réo", "lat": 12.317, "lon": -2.470, "fest": True,
     "was": "Ausbildungszentrum · Agrarschule · Kinder-Academy · Sommerschule",
     "anker": "start", "dx": 14, "dy": -6},
    {"name": "Wapa", "lat": 12.268, "lon": -2.548, "fest": False,
     "was": "Erster Brunnen · Tiefbrunnen mit Wasserturm · Waldgarten",
     "anker": "end", "dx": -14, "dy": 16},
    {"name": "Tukon", "lat": 12.382, "lon": -2.542, "fest": False,
     "was": "Wasserpumpe", "anker": "end", "dx": -14, "dy": -4},
    {"name": "Bankio", "lat": 12.205, "lon": -2.501, "fest": False,
     "was": "Solar-Wasseranlage", "anker": "start", "dx": 14, "dy": 4},
    {"name": "Ekulpung", "lat": 12.352, "lon": -2.629, "fest": False,
     "was": "Wasserstelle", "anker": "end", "dx": -14, "dy": 4},
]
SIGMARINGEN = (48.087, 9.218)
OUAGADOUGOU = (12.3714, -1.5197)

# ---------------------------------------------------------------- Karte A
def karte_fern(b=430, h=580):
    """Deutschland und Burkina Faso in einem Bild. Beantwortet die Frage,
    die sich ein Leser hier zuerst stellt: wo ist das überhaupt?
    Hochformat, weil der Ausschnitt hoch ist — im Querformat stünde die
    Karte als schmaler Streifen in viel leerer Fläche."""
    proj = Projektion(-13, 19, 4, 56, b, h, rand=16)
    teile = []
    for datei in ("MLI.json","NER.json","GHA.json","CIV.json","TGO.json","BEN.json"):
        teile.append('<path d="%s" class="k-land"/>' % pfad(laden(datei), proj, .07))
    teile.append('<path d="%s" class="k-de"/>' % pfad(laden("DEU.json"), proj, .07))
    teile.append('<path d="%s" class="k-bf"/>' % pfad(laden("bf.geo.json"), proj, .04))

    a = proj(SIGMARINGEN[1], SIGMARINGEN[0])
    z = proj(ORTE[0]["lon"], ORTE[0]["lat"])
    km = entfernung(SIGMARINGEN, (ORTE[0]["lat"], ORTE[0]["lon"]))
    # Steuerpunkt seitlich versetzt, damit der Bogen sichtbar krümmt
    mx, my = (a[0]+z[0])/2 - 86, (a[1]+z[1])/2
    teile.append('<path d="M%.1f %.1fQ%.1f %.1f %.1f %.1f" class="k-bogen"/>'
                 % (a[0],a[1],mx,my,z[0],z[1]))
    teile.append('<circle cx="%.1f" cy="%.1f" r="3.4" class="k-pkt-de"/>' % a)
    teile.append('<circle cx="%.1f" cy="%.1f" r="4" class="k-pkt"/>' % z)
    teile.append('<text x="%.1f" y="%.1f" class="k-ort halo">Sigmaringen</text>' % (a[0]+10, a[1]+4))
    teile.append('<text x="%.1f" y="%.1f" class="k-ort halo">Réo · Wapa</text>' % (z[0]+11, z[1]+4))
    teile.append('<text x="%.1f" y="%.1f" class="k-land-be halo" text-anchor="middle">Burkina Faso</text>'
                 % (z[0]-4, z[1]+34))
    # Massangabe auf dem Bogen, mit Papier-Halo freigestellt
    bx = 0.25*a[0] + 0.5*mx + 0.25*z[0]
    by = 0.25*a[1] + 0.5*my + 0.25*z[1]
    # 30 px neben den Bogen, sonst läuft die Linie mitten durch die Schrift
    teile.append('<text x="%.1f" y="%.1f" class="k-mass halo" text-anchor="end">%s km</text>'
                 % (bx-48, by, format(int(round(km/10.0)*10), ",d").replace(",", ".")))
    teile.append('<text x="%.1f" y="%.1f" class="k-mass halo" text-anchor="end">Luftlinie</text>'
                 % (bx-48, by+14))
    return b, h, "".join(teile)

# ---------------------------------------------------------------- Karte B
def karte_land(b=560, h=430):
    """Burkina Faso, und darin die Provinz Sanguié.

    Ohne diese Zwischenstufe sieht die Provinz aus wie ein eigenes Land: eine
    Fläche mit Umriss, die in nichts drinliegt. Hier liegt sie sichtbar in
    etwas drin. Der goldene Suchrahmen taucht auf der nächsten Karte wieder
    auf — daran erkennt man, dass die eine der Ausschnitt der anderen ist."""
    gs = sanguie()
    proj = Projektion(-5.9, 2.8, 9.2, 15.3, b, h, rand=14)

    teile = []
    for datei in ("MLI.json","NER.json","GHA.json","CIV.json","TGO.json","BEN.json"):
        teile.append('<path d="%s" class="k-land"/>' % pfad(laden(datei), proj, .035))
    teile.append('<path d="%s" class="k-bf-voll"/>' % pfad(laden("bf.geo.json"), proj, .02))
    teile.append('<path d="%s" class="k-prov-klein"/>' % pfad(gs, proj, .012))

    # Suchrahmen um die Provinz
    xs = [proj(x, y)[0] for r in ringe(gs) for x, y in r]
    ys = [proj(x, y)[1] for r in ringe(gs) for x, y in r]
    rx, ry = min(xs) - 7, min(ys) - 7
    rw, rh = max(xs) - min(xs) + 14, max(ys) - min(ys) + 14
    teile.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" class="k-rahmen"/>'
                 % (rx, ry, rw, rh))

    # Beschriftung der Provinz, nach links abgesetzt
    teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="k-fuehr"/>'
                 % (rx - 3, ry + rh/2, rx - 26, ry + rh/2))
    teile.append('<text x="%.1f" y="%.1f" class="k-ort halo" text-anchor="end">Provinz Sanguié</text>'
                 % (rx - 31, ry + rh/2 + 4))

    # Ouagadougou zur Orientierung
    ox, oy = proj(OUAGADOUGOU[1], OUAGADOUGOU[0])
    teile.append('<circle cx="%.1f" cy="%.1f" r="2.8" class="k-pkt-neben"/>' % (ox, oy))
    teile.append('<text x="%.1f" y="%.1f" class="k-neben halo">Ouagadougou</text>' % (ox + 8, oy + 4))

    teile.append('<text x="16" y="24" class="k-titel">Burkina Faso</text>')
    return b, h, "".join(teile)

# ---------------------------------------------------------------- Karte C
def karte_nah(b=520, h=620):
    """Die Provinz Sanguié mit den Orten, an denen der Verein gebaut hat.
    Auf der Karte stehen nur die Namen — was wo gebaut wurde, steht in der
    Liste darunter. Fünf Beschriftungen mit Projektlisten überlagern sich
    sonst gegenseitig, und die Liste kann umbrechen, die Karte nicht."""
    g = sanguie()
    lons = [p[0] for r in ringe(g) for p in r]
    lats = [p[1] for r in ringe(g) for p in r]
    proj = Projektion(min(lons)-.06, max(lons)+.06, min(lats)-.05, max(lats)+.05, b, h, rand=18)

    teile = ['<path d="%s" class="k-prov"/>' % pfad(g, proj, .003)]
    for o in ORTE:
        x, y = proj(o["lon"], o["lat"])
        tx, ty = x + o["dx"], y + o["dy"]
        # Führungslinie, wo die Beschriftung merklich abgesetzt ist
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="k-fuehr"/>'
                     % (x + (5.5 if o["dx"] > 0 else -5.5), y, tx - (3 if o["dx"] > 0 else -3), ty-4))
        if o["fest"]:
            teile.append('<circle cx="%.1f" cy="%.1f" r="5" class="k-pkt"/>' % (x, y))
        else:
            teile.append('<circle cx="%.1f" cy="%.1f" r="6" class="k-pkt-frei"/>' % (x, y))
            teile.append('<circle cx="%.1f" cy="%.1f" r="1.7" class="k-pkt-kern"/>' % (x, y))
        teile.append('<text x="%.1f" y="%.1f" class="k-ort halo" text-anchor="%s">%s</text>'
                     % (tx, ty, o["anker"], o["name"]))
    # Maßstabsbalken. Eine Fläche ohne Maßstab wird automatisch als Land gelesen;
    # 20 km daneben rücken die Größenordnung sofort zurecht.
    km = 20.0
    lang = (km / 111.32) * proj.s          # Grad Breite -> Pixel
    bx, by = 20, h - 30
    teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="k-massstab"/>'
                 % (bx, by, bx + lang, by))
    for tick in (bx, bx + lang):
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="k-massstab"/>'
                     % (tick, by - 3.5, tick, by + 3.5))
    teile.append('<text x="%.1f" y="%.1f" class="k-neben">%d km</text>'
                 % (bx + lang + 7, by + 4, int(km)))

    # Derselbe goldene Rahmen wie auf der Landkarte — das ist das Bindeglied
    teile.append('<rect x="3" y="3" width="%d" height="%d" rx="2" class="k-rahmen"/>' % (b-6, h-6))
    teile.append('<text x="18" y="26" class="k-titel">Ausschnitt — Provinz Sanguié</text>')
    return b, h, "".join(teile)

# ---------------------------------------------------------------- Ausgabe
if __name__ == "__main__":
    ring = ringe(sanguie())[0]
    ausserhalb = [o["name"] for o in ORTE if not liegt_in(o["lon"], o["lat"], ring)]
    offen = [o["name"] for o in ORTE if not o["fest"]]
    bloecke = []
    for name, fn in (("fern", karte_fern), ("land", karte_land), ("nah", karte_nah)):
        b, h, inhalt = fn()
        bloecke.append('<svg class="karte" viewBox="0 0 %d %d" role="img" '
                       'aria-label="Karte">%s</svg>' % (b, h, inhalt))
    ziel = os.path.join(HIER, "karte.svg.txt")
    io.open(ziel, "w", encoding="utf-8").write("\n\n".join(bloecke))
    print("geschrieben:", ziel)
    for etikett, block in zip(("fern", "land", "nah"), bloecke):
        print("  Karte %-5s %5d Zeichen" % (etikett, len(block)))
    print("  zusammen   %5d Zeichen" % sum(len(x) for x in bloecke))
    if offen:
        print("  Position geschätzt, nicht belegt: " + ", ".join(offen))
    if ausserhalb:
        print("  FEHLER — außerhalb der Provinz Sanguié: " + ", ".join(ausserhalb))
    else:
        print("  alle Orte liegen innerhalb der Provinzgrenze")
