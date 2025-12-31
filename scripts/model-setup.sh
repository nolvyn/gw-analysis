#!/usr/bin/env bash

echo "Setting up required waveform models..."

cd "$HOME/gw-analysis/data/models"

git clone https://git.ligo.org/lscsoft/lalsuite-extra.git
git clone https://git.ligo.org/waveforms/software/lalsuite-waveform-data.git

cp -a lalsuite-extra/data/lalsimulation/. ./
cp -a -f lalsuite-waveform-data/waveform_data/. ./

rm -rf lalsuite-extra
rm -rf lalsuite-waveform-data
