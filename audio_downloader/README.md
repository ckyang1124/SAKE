# Audio Data Downloading Scripts

This folder contains the scripts to download audio data for SAKE.

## Requirements

- A Hugging Face Token with access to: https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0
- Install the following packages:
  - `datasets`
  - `soundfile`
  - `av`
  - `tqdm`
  - `pandas`
  - `numpy`


## Usage

1. Set your Hugging Face Token in `download_audio.sh` by replacing `<YOUR_HF_TOKEN_HERE>` with your actual token.
2. Run `download_audio.sh` to download all the audio data and organize them into `./audio_data/` folder. Downloading may take hours depending on your internet speed. Make sure your internet connection is stable during the process.