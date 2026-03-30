#!/usr/bin/env bash

mkdir -p "$HOME/gw-analysis/data/events"
cd "$HOME/gw-analysis/data/events"

uv run zenodo_get 17014085 # GWTC-4
uv run zenodo_get 8177023 # GWTC-3
uv run zenodo_get 6513631 # GWTC-2.1
