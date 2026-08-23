#!/bin/sh
# Holt die Geodaten, aus denen werkzeug/karte.py die Umrisse rechnet.
# Die Dateien sind bewusst nicht eingecheckt (siehe .gitignore).
set -e
cd "$(dirname "$0")"

# Ländergrenzen — Natural Earth, gemeinfrei
curl -sSf -o welt.json \
  https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json

# Provinzgrenzen Burkina Faso — geoBoundaries, CC BY 4.0
curl -sSf -o adm2.json \
  https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/releaseData/gbOpen/BFA/ADM2/geoBoundaries-BFA-ADM2_simplified.geojson

echo "Geodaten geholt. Jetzt:  python3 werkzeug/karte.py"
