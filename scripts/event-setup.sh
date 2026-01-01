#!/usr/bin/env bash

echo "Do you use NixOS?"
echo "1) Yes"
echo "2) No/I do not know"

read -p "Enter choice: " choice

mkdir -p "$HOME/gw-analysis/data/events"
cd "$HOME/gw-analysis/data/events"

eval "$(micromamba shell hook --shell bash)"
micromamba activate igwn

GWTC_4="17014085"
GWTC_3="8177023"
GWTC_2="6513631"

if [ "$choice" == 1 ]; then
  steam-run zenodo_get "$GWTC_4"
  steam-run zenodo_get "$GWTC_3"
  steam-run zenodo_get "$GWTC_2"
elif [ "$choice" == 2 ]; then
  zenodo_get "$GWTC_4"
  zenodo_get "$GWTC_3"
  zenodo_get "$GWTC_2"
fi
