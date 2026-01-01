#!/usr/bin/env bash

echo "Downloading required waveform models..."

mkdir -p "$HOME/gw-analysis/data/models"
cd "$HOME/gw-analysis/data/models"

git clone https://git.ligo.org/lscsoft/lalsuite-extra.git
git clone https://git.ligo.org/waveforms/software/lalsuite-waveform-data.git

cp -a lalsuite-extra/data/lalsimulation/. ./
rm SEOBNRv5ROM_v1.0.hdf5
cp -a lalsuite-waveform-data/waveform_data/. ./

rm -rf lalsuite-extra
rm -rf lalsuite-waveform-data
