import json
import pandas as pd
from shutil import copyfile
from datasets import load_dataset
import soundfile
import av
import numpy as np
import wave
import os

from tqdm import tqdm


def mp4_to_wav_with_ffmpeg(input_path: str, output_path: str):
    """
    Used for the training set
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} does not exist.")
    os.system(f"ffmpeg -i {input_path} {output_path}")


def mp4_to_wav_with_av(input_path: str, output_path: str):
    """
    Used for the test set
    """
    container = av.open(input_path)
    audio_stream = next(s for s in container.streams if s.type == "audio")

    sample_rate = audio_stream.codec_context.sample_rate
    channels = audio_stream.codec_context.channels

    with wave.open(output_path, "wb") as wav_out:
        wav_out.setnchannels(channels)
        wav_out.setsampwidth(2)  # 16-bit PCM
        wav_out.setframerate(sample_rate)

        for frame in container.decode(audio_stream):
            pcm = frame.to_ndarray().astype(np.int16)
            wav_out.writeframes(pcm.tobytes())

    container.close()


def animal():
    os.makedirs("./audio_data/Animal", exist_ok=True)
    df = pd.read_csv("./animal_source_dataset_mapping.csv")
    # turn to dict
    animal_mapping = (
        df[["original_filename", "new_filename"]]
        .set_index("original_filename")
        .to_dict()["new_filename"]
    )
    for orig_f, new_f in animal_mapping.items():
        copyfile(orig_f, f"./audio_data/Animal/{new_f}")


def emotion():
    os.makedirs("./audio_data/Emotion", exist_ok=True)
    data = json.load(open("all_emotion_audios.json"))
    for audio_file in data["CREMA-D"]:
        copyfile(f"CREMA-D/AudioWAV/{audio_file}", f"./audio_data/Emotion/{audio_file}")

    for audio_file in data["MELD"]["train"]:
        mp4_to_wav_with_ffmpeg(
            f"MELD.Raw/train_splits/{audio_file.replace('.wav', '.mp4')}",
            f"./audio_data/Emotion/{audio_file}",
        )
    for audio_file in data["MELD"]["test"]:
        mp4_to_wav_with_av(
            f"MELD.Raw/output_repeated_splits_test/{audio_file.replace('.wav', '.mp4')}",
            f"./audio_data/Emotion/{audio_file}",
        )


def common_voice():
    # Gender and Language use common voice
    os.makedirs("./audio_data/Gender", exist_ok=True)
    os.makedirs("./audio_data/Language", exist_ok=True)
    data = json.load(open("all_common_voice_audios.json"))
    for lang in tqdm(
        data, desc="Processing common voice languages", dynamic_ncols=True
    ):
        for split in tqdm(
            data[lang], desc="Processing splits", dynamic_ncols=True, leave=False
        ):
            tqdm.write(f"Processing {lang} {split}")
            ds = load_dataset(
                "mozilla-foundation/common_voice_17_0",
                lang,
                split=split,
                streaming=True,
                trust_remote_code=True,
            )
            for row in ds:
                file_name = row["path"].replace("/", "_").replace(".mp3", ".wav")
                if file_name in data[lang][split]:
                    for attr_dir in data[lang][split][file_name]:
                        new_path = f"./audio_data/{attr_dir}/{file_name}"
                        soundfile.write(
                            new_path,
                            row["audio"]["array"],
                            row["audio"]["sampling_rate"],
                        )


def dynamic_superb():

    spoof_name = "DynamicSuperb/SpoofDetection_ASVspoof"

    def get_audio_filename(example: dict) -> str:
        if example["audio"]["path"] is not None:
            audio_filename = (
                example["audio"]["path"].split("/")[-1].split(".")[0] + ".wav"
            )
        else:
            audio_filename = example["file"].split("/")[-1].split(".")[0] + ".wav"
        return audio_filename

    data = json.load(open("all_dynamic_superb.json"))
    for track in tqdm(data, desc="Processing DynamicSuperb tracks", dynamic_ncols=True):
        track_dir = (
            spoof_name if track.startswith(spoof_name) else track.split("-Fold")[0]
        )
        audio_dir = f"./audio_data/{track_dir}"

        ds = load_dataset(track, split="test", streaming=True, trust_remote_code=True)
        for example in ds:
            audio_filename = get_audio_filename(example)
            curr = {
                "file": audio_filename,
                "question": example["instruction"].strip(),
                "answer": example["label"].strip(),
            }
            if curr in data[track]:
                os.makedirs(audio_dir, exist_ok=True)
                soundfile.write(
                    f"{audio_dir}/{audio_filename}",
                    example["audio"]["array"],
                    example["audio"]["sampling_rate"],
                )


if __name__ == "__main__":
    for func in [dynamic_superb]:
        print(f"Processing {func.__name__}...")
        func()
