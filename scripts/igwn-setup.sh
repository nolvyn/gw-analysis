#!/usr/bin/env bash

echo "What would you like to do?"
echo "1) Create an exact igwn environment"
echo "2) Create a minimal igwn environment"

read -p "Enter choice: " choice

if [ "$choice" == 1 ]; then
  micromamba env create -f "$HOME/gw-analysis/envs/igwn.yaml"
elif [ "$choice" == 2 ]; then
  micromamba env create -f "$HOME/gw-analysis/envs/igwn-minimal.yaml"
fi
