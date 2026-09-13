---
type: reference
created: 2026-08-21
updated: 2026-08-21
maintained_by: noah
holds_state: true
tags: [wapa, website, weiterleitungen, umzug]
---

# Weiterleitungskarte

Jede Adresse der alten WordPress-Seite und wohin sie künftig zeigt. **87 Einträge,
Abdeckung der Sitemaps vollständig** (85 von 85 geprüft am 21.08.2026).

## Wie das benutzt wird

Die Karte lebt als `src/weiterleitungen.csv`. Daraus erzeugt

```bash
python3 src/weiterleitungen_formate.py
```

die Dateien für den jeweiligen Host — `.htaccess` (Apache, die meisten deutschen
Hoster), `_redirects` (Netlify, Cloudflare Pages), `nginx.conf`, und ersatzweise
HTML-Weichen für Hosts, die gar nichts davon können.

**Alle Pfade sind relativ.** Die Karte gilt unverändert, egal unter welcher
Domain die Seite läuft — für den Umzug auf gemeinsamfuerwapa.de ist nichts
anzupassen.

## Ein Punkt, der vorher entschieden werden muss

Die Ziele stehen zurzeit als **Hash-Adressen** (`/#/aktuelles/…`), weil der
Entwurf eine einzelne Datei ist. Für den Dauerbetrieb sind **echte Pfade**
(`/aktuelles/…/`) besser: Suchmaschinen behandeln sie als eigene Seiten,
Hash-Adressen nicht.

Das Skript kann beides:

```bash
python3 src/weiterleitungen_formate.py --pfade
```

Voraussetzung für echte Pfade ist der Generator, der je Beitrag eine eigene
Datei erzeugt — der steht noch aus. **Die linke Spalte der Karte ändert sich
dadurch nicht**, nur die rechte. Die Arbeit ist also nicht umsonst.

## Warum das vor dem Umschalten stehen muss

Zehn Jahre Links zeigen auf die alten Adressen: aus Zeitungsartikeln, aus
Newslettern, aus Suchmaschinen, aus Betterplace. Ohne Karte werden daraus am
Umschalttag lauter Fehlseiten — und zwar genau bei den Menschen, die schon
einmal Interesse hatten.

---

## Seiten

| alt | neu |
|---|---|
| `/` | `#/` |
| `/ausbildungszentrum_bau/` | `#/projekt/ausbildungszentrum` |
| `/bildung/` | `#/projekte/Bildung` |
| `/danke/` | `#/spenden` |
| `/datenschutzerklaerung/` | `#/datenschutz` |
| `/grundversorgung/` | `#/projekte/Grundversorgung` |
| `/home/` | `#/` |
| `/impressum/` | `#/impressum` |
| `/infrastruktur/` | `#/projekte/Infrastruktur` |
| `/mitmachen/` | `#/mitmachen` |
| `/partner/` | `#/partner` |
| `/patenschaft/` | `#/spenden` |
| `/projekte/` | `#/projekte` |
| `/projekte/bericht-von-sabine-und-martin-vatter/` | `#/aktuelles/bericht-vatter` |
| `/satzung/` | `#/satzung` |
| `/sommerschule/` | `#/projekt/sommerschule` |
| `/spenden/` | `#/spenden` |
| `/ueber-uns/` | `#/ueber-uns` |
| `/umweltschutz/` | `#/projekte/Umweltschutz` |
| `/wapa-burkina-faso/` | `#/burkina-faso` |

## Beiträge

| alt | neu |
|---|---|
| `/1360-2/` | `#/aktuelles/corona-erste-erfolge` |
| `/7369-2/` | `#/aktuelles/neujahr-2021` |
| `/artikel-baumprojekt-dezember-2020/` | `#/aktuelles/bericht-baumprojekt-2020` |
| `/brunnenbau/` | `#/aktuelles/brunnenbau-beginnt` |
| `/brunnenbau2/` | `#/aktuelles/brunnenbau-fertiggestellt` |
| `/corona-hilfskation-ende-der-aktuellen-phase/` | `#/aktuelles/corona-ende-der-phase` |
| `/corona-spendenaktion-2/` | `#/aktuelles/corona-zwei-hilfsprojekte` |
| `/corona-spendenaktion/` | `#/aktuelles/corona-spendenaufruf` |
| `/mauer-fuer-die-schule/` | `#/aktuelles/mauer-fuer-die-schule` |
| `/nachruf-mitgruenderin-marlis-schmitt-sickinger/` | `#/aktuelles/nachruf-marlis-schmitt-sickinger` |
| `/naehmaschinenlieferung/` | `#/aktuelles/naehmaschinenlieferung` |
| `/news_garten/` | `#/aktuelles/garten-am-wasserturm` |
| `/pflanzaktion-februar-2022/` | `#/aktuelles/pflanzaktion-februar-2022` |
| `/schulausbau/` | `#/aktuelles/schulausbau` |
| `/schulbesuch/` | `#/aktuelles/schulbesuch-2020` |
| `/schulprojekt/` | `#/aktuelles/schulprojekt-abschluss` |
| `/unser-besuch-in-burkina-faso/` | `#/aktuelles/besuch-in-burkina-faso` |
| `/waldgarten-waechst/` | `#/aktuelles/waldgarten-waechst` |
| `/wasser-fuer-ekulpung/` | `#/aktuelles/wasser-fuer-ekulpung` |

## Projekte (vormals Portfolio-Items)

| alt | neu |
|---|---|
| `/portfolio-items/ausbildungszentrum/` | `#/projekt/ausbildungszentrum` |
| `/portfolio-items/baumprojekt/` | `#/projekt/baumprojekt` |
| `/portfolio-items/garten-wasserturm/` | `#/projekt/waldgarten` |
| `/portfolio-items/neuer-brunnen-in-wapa/` | `#/projekt/tiefbrunnen` |
| `/portfolio-items/seife/` | `#/projekt/seifenherstellung` |
| `/portfolio-items/serverraum/` | `#/projekt/serverraum` |
| `/portfolio-items/solaranlage/` | `#/projekt/solaranlage` |
| `/portfolio-items/solarofen/` | `#/projekt/solaroefen` |
| `/portfolio-items/sprachkurs/` | `#/projekt/sprachkurs-lele` |
| `/portfolio-items/textilfaerbung/` | `#/projekt/textilfaerbung` |
| `/portfolio-items/tropfenbewaesserung/` | `#/projekt/tropfenbewaesserung` |
| `/portfolio-items/wasser/` | `#/projekt/wasser-fuer-wapa` |

## Portfolio-Kategorien

| alt | neu |
|---|---|
| `/portfolio_category/all/` | `#/projekte` |
| `/portfolio_category/baumprojekt/` | `#/projekte/Umweltschutz` |
| `/portfolio_category/mithelfen/` | `#/mitmachen` |
| `/portfolio_category/polytechnisches-ausbildungszentrum/` | `#/projekte/Bildung` |
| `/portfolio_category/projekt-finanzieren/` | `#/spenden` |
| `/portfolio_category/solaranlage/` | `#/projekt/solaranlage` |
| `/portfolio_category/wasser-fuer-wapa/` | `#/projekte/Grundversorgung` |

## Schlagwörter

| alt | neu |
|---|---|
| `/tag/aufforstung/` | `#/projekt/baumprojekt` |
| `/tag/waldgarten/` | `#/projekt/waldgarten` |

## Sammelkategorie

| alt | neu |
|---|---|
| `/category/uncategorized/` | `#/aktuelles` |

## Übersicht der Portfolio-Items

| alt | neu |
|---|---|
| `/portfolio-items/` | `#/projekte` |

## Autorenarchiv — entfällt, Namen stehen am Beitrag

*Autorenarchiv — entfällt, Namen stehen am Beitrag*

| alt | neu |
|---|---|
| `/author/bateaublanc/` | `#/aktuelles` |
| `/author/caro/` | `#/aktuelles` |
| `/author/thomas/` | `#/aktuelles` |

## war kein Projekt, sondern eine Aufgabe für Freiwillige

*war kein Projekt, sondern eine Aufgabe für Freiwillige*

| alt | neu |
|---|---|
| `/portfolio-items/agrarexperten/` | `#/mitmachen` |
| `/portfolio-items/impressionen/` | `#/mitmachen` |
| `/portfolio-items/marketing/` | `#/mitmachen` |
| `/portfolio-items/rechtsberater/` | `#/mitmachen` |

## Demo-Rest des Avada-Themes — kein Inhalt, den jemand sucht

*Demo-Rest des Avada-Themes — kein Inhalt, den jemand sucht*

| alt | neu |
|---|---|
| `/slide-page/burkina/` | `#/` |
| `/slide-page/charity-blog-post-1/` | `#/` |
| `/slide-page/charity-blog-post-5/` | `#/` |
| `/slide-page/charity-blog-post-6/` | `#/` |
| `/slide-page/charity-blog-post-7/` | `#/` |
| `/slide-page/charity-dontate/` | `#/` |
| `/slide-page/charity-fair-trade/` | `#/` |
| `/slide-page/charity-farming/` | `#/` |
| `/slide-page/charity-mission/` | `#/` |
| `/slide-page/charity-shelter/` | `#/` |
| `/slide-page/datenschutz/` | `#/` |
| `/slide-page/gartenprojekt/` | `#/` |
| `/slide-page/impressum/` | `#/` |
| `/slide-page/patenschaft/` | `#/` |
| `/slide-page/poly-ausbildungszentrum/` | `#/` |
| `/slide-page/polytechnikum/` | `#/` |
| `/slide-page/startseite/` | `#/` |
| `/slide-page/waldgarten/` | `#/` |
