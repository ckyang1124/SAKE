#!/bin/bash

set -e

export HF_TOKEN="<YOUR_HF_TOKEN_HERE>"
mkdir audio_data

# animal
git clone https://github.com/YashNita/Animal-Sound-Dataset.git
git clone https://github.com/karolpiczak/ESC-50.git

# emotion
git clone https://github.com/CheyneyComputerScience/CREMA-D.git
wget http://web.eecs.umich.edu/~mihalcea/downloads/MELD.Raw.tar.gz
tar -xvzf MELD.Raw.tar.gz
tar -xzvf MELD.Raw/train.tar.gz -C MELD.Raw
tar -xzvf MELD.Raw/test.tar.gz -C MELD.Raw

# Organize and download audio files needed in CommonVoice
python download_audio.py

# Remove temp files
rm -rf Animal-Sound-Dataset ESC-50 MELD.Raw.tar.gz MELD.Raw CREMA-D