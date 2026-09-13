# Zu übertragen in die Vault-Datei

Stand 13.09.2026 · Rückmeldung Bertrand und Noah vom selben Tag

`index.html` in diesem Repo ist **abgeleitet**. Die Änderungen unten stehen dort
bereits drin, damit man sie ansehen kann — aber der nächste
`python3 build.py …` überschreibt sie wieder. Sie müssen in
`Website-Entwurf-final.html` im Vault nachgezogen werden.

Suchen und ersetzen, Zeichen für Zeichen. Die Zeilennummern beziehen sich auf
die abgeleitete Datei und dienen nur zum Wiederfinden.

---

## 1 · Monatslohn des Gärtners: 23 € → 150 €

**Achtung:** 23 € steht an drei weiteren Stellen für eine **Handwaschstation**.
Die bleiben unverändert. Nur diese sieben:

| alt | neu |
|---|---|
| `Ein Gärtner pflegt ihn für 23 € im Monat, bezahlt aus Spenden.` | `… für 150 € im Monat …` |
| `Er erhält einen monatlichen Lohn von umgerechnet 23 Euro` | `… von umgerechnet 150 Euro` |
| `<span class="a">23 €</span><span class="w">Ein Monatslohn des Gärtners</span>` | `150 €` |
| `Der Gärtner wird aus Spenden bezahlt — 23 € im Monat.` | `… — 150 € im Monat.` |
| `Ein Gärtner pflegt ihn für 23 € im Monat.` | `… für 150 € im Monat.` |
| `<div class="b1">23 €</div><div class="b2">Der Monatslohn unseres Gärtners<span>` | `150 €` |
| `<div class="b1">23 €</div><div class="b2">Der Monatslohn unseres Gärtners</div>` | `150 €` |

**Unverändert lassen:** „Jede Station 23 €“ (Corona-Hilfsaktion), „Eine Station
dieser Art kostet 23€“, `<div class="b1">23 €</div><div class="b2">Eine Handwaschstation`.

## 2 · Tropfenbewässerung: 1.000 € → 3.000 €

Vier Stellen: Registereintrag, Projekttext, Startseiten-Preisliste,
Spendenseite. Jeweils `1.000` → `3.000` bzw. `1.000 Euro` → `3.000 Euro`.

## 3 · Unterrichtsraum: 3.050 € → 3.600 €

Nur die **zwei Spendenangaben** geändert (Startseite und Spendenseite).

Der Projekttext des Ausbildungszentrums nennt weiterhin 3.050 € — das ist eine
Rechnung aus der **ersten Bauphase 2018** (10.600 € für drei Räume plus
Sanitär). Historische Angabe, deshalb nicht angefasst. Der Widerspruch steht
jetzt in der Prüfliste unter `#/neu`; **der Vorstand muss sagen, welcher Betrag
gilt**, sonst stehen zwei Zahlen für dieselbe Sache auf der Seite.

## 4 · Serverraum aus dem Spendenplan

Die Zeile `3.500 € · Der Serverraum und Copyshop · Zu 90 % finanziert` ist von
der Spendenseite entfernt.

**Bewusst stehen geblieben:** der Registereintrag und die Projektseite. „Kann
aus dem Plan raus“ hieß für mich: nicht mehr um Geld dafür bitten — nicht: das
Projekt verschwindet. Wenn es ganz weg soll, bitte sagen.

## 5 · Betterplace

Beide Schaltflächen entfernt:
- `<a class="b gold" …>Über Betterplace spenden</a>` im Spendenblock
- `<a class="b leer" …>Zu Betterplace</a>` auf der Spendenseite

**Stehen geblieben:** der erklärende Absatz „Betterplace und PayPal“ (nennt die
Gebühren und dass eine Überweisung vollständig ankommt) und der Betterplace-Link
**im Beitrag von 2018** — der gehört zum damaligen Text und wird nicht
rückwirkend geändert.

## 6 · Mitmachen

- Abschnitt von der **Startseite** entfernt (war Abschnitt 9)
- aus der **Hauptnavigation** entfernt
- als **Abschnitt auf der Spendenseite** neu angelegt, gekürzt
- Fußzeile: „Mitmachen“ zeigt jetzt auf `#/spenden`
- `VIEWS['mitmachen']` gelöscht
- **`#/mitmachen` leitet auf `#/spenden` weiter** — geteilte Links und
  Lesezeichen laufen nicht ins Leere

## 7 · Mitglied werden (neu, auf der Spendenseite)

Beitragsstufen **25 / 50 / 100 € / Frei, im Monat**, dazu die neue
Beitrittserklärung als PDF mit dem Hinweis, sie ausgefüllt an
`info@gemeinsamfuerwapa.de` zu senden.

**Bitte gegenlesen:** Die alte Beitrittserklärung nannte **12,00 € im Jahr**.
25 € im Monat sind das Fünfundzwanzigfache davon. Der Sprung steht so auch als
Hinweis auf der Seite. Über die Höhe entscheidet nach § 8 der Satzung die
Mitgliederversammlung — ein Beschluss dazu wäre nötig.

## 8 · Beitrittserklärung neu gesetzt

Neu: `assets/dokumente/Wapa-Beitrittserklaerung-2026.pdf`, eine Seite A4,
Quelle in `werkzeug/beitrittserklaerung.html`, gerendert mit
`werkzeug/pdf.mjs`.

Inhaltlich gleichwertig zur alten Fassung, aber:

- **Rücksendung per E-Mail** an `info@gemeinsamfuerwapa.de` statt an eine
  Privatanschrift
- **§ 8 statt § 5.** Die alte Erklärung verwies auf „§ 5 der Satzung“ — in der
  Satzung von 2021 ist § 5 *Unternehmensgründungen*; die Mitgliedsbeiträge
  stehen in § 8. Der Verweis war schlicht falsch.
- **Kein fester Betrag im Fließtext.** § 8 überlässt die Höhe der
  Mitgliederversammlung; die drei Stufen stehen als Ankreuzfelder daneben.
- **Datenschutzhinweis ergänzt** (Art. 6 Abs. 1 lit. b DSGVO, Zweck, keine
  Weitergabe, Löschung, Auskunftsrecht). In der alten Fassung fehlte er ganz.
- Gläubiger-ID `DE42ZZZ00002068902` und der Wortlaut des Lastschriftmandats
  sind **unverändert übernommen** — daran sollte niemand ohne Not etwas ändern.
- Feld für Telefon (freiwillig) und für abweichende Kontoinhaber ergänzt.

**Die alte Datei ist gelöscht.** Sie nannte als Rücksendeadresse „Josef Kurz,
Schulstraße 2/1, 72488 Sigmaringen-Laiz“ — eine Privatanschrift einer Person,
die im heutigen Vorstand nicht mehr auftaucht. Auf einer öffentlichen Seite hat
das nichts zu suchen. **In der Git-Historie bleibt die Datei erhalten**; wer sie
auch dort entfernt haben will, muss die Historie umschreiben.

---

## Noch zu tun — geht nicht von hier aus

**Banakio.** Im Register steht viermal „Bankio“: Titel, Ortsfeld, Projekttext
und der Slug `wasser-bankio`. Der Slug ist Teil einer teilbaren Adresse
(`#/projekt/wasser-bankio`) — wer ihn ändert, macht bereits verschickte Links
ungültig. Entscheidung des Vorstands; der Punkt steht in der Prüfliste.

**PDF nach Dropbox → Finanzen.** Auf Dropbox habe ich keinen Zugriff. Die Datei
liegt hier unter `assets/dokumente/Wapa-Beitrittserklaerung-2021-neu.pdf`.

**Vier Dorfkoordinaten.** Für später in diesem Jahr angekündigt. Eintragen in
`werkzeug/karte.py`, `fest` auf `True`, Generator laufen lassen.
