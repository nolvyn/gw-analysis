#!/usr/bin/env bash

echo "Downloading required waveform models..."

mkdir -p "$HOME/gw-analysis/data/models"
cd "$HOME/gw-analysis/data/models"
touch .gitkeep

uv run zenodo_get 14999310
