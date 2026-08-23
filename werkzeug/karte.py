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

def pfad(geom, proj, tol, dez=1, mindest=0):
    """`dez` = Nachkommastellen. Auf der Kontinentkarte reichen ganze Pixel und
    sparen ein knappes Drittel der Zeichen. `mindest` wirft Ringe weg, die im
    Bild kleiner als ein paar Pixel wären — Inseln und Kleinstaaten, die man
    ohnehin nicht sieht, aber voll bezahlt."""
    fmt = "%%.%df %%.%df" % (dez, dez)
    aus = []
    for ring in ringe(geom):
        r = vereinfachen(ring, tol)
        if len(r) < 3:
            continue
        pts = [proj(x, y) for x, y in r]
        if mindest:
            xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
            if (max(xs)-min(xs)) < mindest and (max(ys)-min(ys)) < mindest:
                continue
        aus.append("M" + "L".join(fmt % q for q in pts) + "Z")
    return "".join(aus)

_WELT = None
def welt():
    """Alle Länderumrisse aus einer Datei. Einmal einlesen, nach Namen greifen."""
    global _WELT
    if _WELT is None:
        d = json.load(io.open(os.path.join(ROH, "welt.json"), encoding="utf-8"))
        _WELT = {f["properties"]["name"]: f["geometry"] for f in d["features"]}
    return _WELT

def im_fenster(geom, lon0, lon1, lat0, lat1):
    """Grobprüfung, ob ein Land überhaupt ins Bild ragt. Spart Pfade für
    Länder, die vollständig außerhalb liegen."""
    for r in ringe(geom):
        for x, y in r:
            if lon0 <= x <= lon1 and lat0 <= y <= lat1:
                return True
    return False

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

def kurs(a, b):
    """Anfangskurs von a nach b in Grad, von Nord im Uhrzeigersinn.
    Damit zeigt der Pfeil wirklich dorthin, statt nur ungefähr nach oben."""
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    dlo = lo2 - lo1
    y = math.sin(dlo) * math.cos(la2)
    x = math.cos(la1)*math.sin(la2) - math.sin(la1)*math.cos(la2)*math.cos(dlo)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

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
    {"name": "Banakio", "lat": 12.205, "lon": -2.501, "fest": False,
     "was": "Solar-Wasseranlage", "anker": "start", "dx": 14, "dy": 4},
    {"name": "Ekulpung", "lat": 12.352, "lon": -2.629, "fest": False,
     "was": "Wasserstelle", "anker": "end", "dx": -14, "dy": 4},
]
SIGMARINGEN = (48.087, 9.218)
OUAGADOUGOU = (12.3714, -1.5197)

# ---------------------------------------------------------------- Karte A
# Die Region, um die es geht. Diese Länder bekommen Fläche; alles andere im
# Bild nur einen Umriss. So bleibt der Blick unten, obwohl Deutschland
# mit im Bild ist.
WESTAFRIKA = {
    "Burkina Faso", "Mali", "Niger", "Nigeria", "Ghana", "Ivory Coast",
    "Benin", "Togo", "Senegal", "Guinea", "Guinea Bissau", "Sierra Leone",
    "Liberia", "Gambia", "Mauritania",
}

def karte_fern(b=520, h=700):
    """Westafrika, mit Deutschland gerade noch am oberen Rand.

    Zwei Stufen: die Länder der Region sind gefüllt, alles dazwischen —
    Maghreb, Iberische Halbinsel, Frankreich — steht nur als Umriss da. Das
    Bild bleibt damit auf Westafrika gewichtet, obwohl es bis Süddeutschland
    reicht, und die Strecke dazwischen ist trotzdem zu sehen statt nur
    behauptet."""
    LON0, LON1, LAT0, LAT1 = -18.5, 16.5, 3.0, 50.0
    proj = Projektion(LON0, LON1, LAT0, LAT1, b, h, rand=12)
    W = welt()

    umriss, flaeche = [], []
    for name, geom in sorted(W.items()):
        if name in ("Burkina Faso", "Germany"):
            continue
        if not im_fenster(geom, LON0, LON1, LAT0, LAT1):
            continue
        d = pfad(geom, proj, .14, dez=0, mindest=4)
        if not d:
            continue
        (flaeche if name in WESTAFRIKA else umriss).append(
            '<path d="%s" class="%s"/>' % (d, "k-land" if name in WESTAFRIKA else "k-durch"))
    teile = umriss + flaeche
    teile.append('<path d="%s" class="k-de"/>' % pfad(W["Germany"], proj, .12, dez=0))
    teile.append('<path d="%s" class="k-bf"/>' % pfad(W["Burkina Faso"], proj, .03))

    xs = [proj(x, y)[0] for r in ringe(W["Burkina Faso"]) for x, y in r]
    ys = [proj(x, y)[1] for r in ringe(W["Burkina Faso"]) for x, y in r]
    rx, ry = min(xs) - 6, min(ys) - 6
    rw, rh = max(xs) - min(xs) + 12, max(ys) - min(ys) + 12
    teile.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" class="k-rahmen"/>'
                 % (rx, ry, rw, rh))

    # Nachbarn in der Region. Benin und Togo sind hierfür zu schmal.
    for name, lon, lat in (("Mali", -5.4, 19.2), ("Niger", 9.4, 17.4),
                           ("Nigeria", 8.2, 9.2), ("Ghana", -1.2, 7.5),
                           ("Elfenbeinküste", -6.4, 7.2), ("Senegal", -15.0, 14.7),
                           ("Mauretanien", -11.4, 20.8), ("Guinea", -11.8, 10.4)):
        x, y = proj(lon, lat)
        teile.append('<text x="%.1f" y="%.1f" class="k-neben halo" text-anchor="middle">%s</text>'
                     % (x, y, name))
    # Die Länder dazwischen, noch zurückhaltender beschriftet
    for name, lon, lat in (("Marokko", -7.4, 31.6), ("Algerien", 2.4, 27.8),
                           ("Spanien", -3.9, 40.2), ("Frankreich", 2.2, 46.6)):
        x, y = proj(lon, lat)
        teile.append('<text x="%.1f" y="%.1f" class="k-fern halo" text-anchor="middle">%s</text>'
                     % (x, y, name))

    a = proj(SIGMARINGEN[1], SIGMARINGEN[0])
    z = proj(ORTE[0]["lon"], ORTE[0]["lat"])
    km = entfernung(SIGMARINGEN, (ORTE[0]["lat"], ORTE[0]["lon"]))
    mx, my = (a[0]+z[0])/2 - 74, (a[1]+z[1])/2
    teile.append('<path d="M%.1f %.1fQ%.1f %.1f %.1f %.1f" class="k-bogen"/>'
                 % (a[0], a[1], mx, my, z[0], z[1]))
    teile.append('<circle cx="%.1f" cy="%.1f" r="3.2" class="k-pkt-de"/>' % a)
    teile.append('<text x="%.1f" y="%.1f" class="k-ort halo" text-anchor="end">Sigmaringen</text>'
                 % (a[0]-9, a[1]+4))

    # Entfernung neben den Bogen, im freien Atlantik
    t = 0.42
    bx = (1-t)**2*a[0] + 2*(1-t)*t*mx + t*t*z[0]
    by = (1-t)**2*a[1] + 2*(1-t)*t*my + t*t*z[1]
    teile.append('<text x="%.1f" y="%.1f" class="k-mass halo" text-anchor="end">%s km</text>'
                 % (bx-20, by, format(int(round(km/10.0)*10), ",d").replace(",", ".")))
    teile.append('<text x="%.1f" y="%.1f" class="k-mass halo" text-anchor="end">Luftlinie</text>'
                 % (bx-20, by+13))

    teile.append('<text x="%.1f" y="%.1f" class="k-ort halo" text-anchor="end">Burkina Faso</text>'
                 % (rx - 9, ry + rh/2 + 4))
    teile.append('<text x="16" y="24" class="k-titel">Westafrika</text>')
    return b, h, "".join(teile)

# ---------------------------------------------------------------- Karte B
def karte_land(b=560, h=430):
    """Burkina Faso, und darin die Provinz Sanguié.

    Ohne diese Zwischenstufe sieht die Provinz aus wie ein eigenes Land: eine
    Fläche mit Umriss, die in nichts drinliegt. Hier liegt sie sichtbar in
    etwas drin. Der goldene Suchrahmen taucht auf der nächsten Karte wieder
    auf — daran erkennt man, dass die eine der Ausschnitt der anderen ist."""
    gs = sanguie()
    LON0, LON1, LAT0, LAT1 = -5.9, 2.8, 9.2, 15.3
    proj = Projektion(LON0, LON1, LAT0, LAT1, b, h, rand=14)
    W = welt()

    teile = []
    for name, geom in sorted(W.items()):
        if name == "Burkina Faso" or not im_fenster(geom, LON0, LON1, LAT0, LAT1):
            continue
        d = pfad(geom, proj, .06, dez=0, mindest=4)
        if d:
            teile.append('<path d="%s" class="k-land"/>' % d)
    teile.append('<path d="%s" class="k-bf-voll"/>' % pfad(W["Burkina Faso"], proj, .02))
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
