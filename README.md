# 🍶 SAKE: Towards Editing Auditory Attribute Knowledge of Large Audio-Language Models

[![](https://img.shields.io/badge/arxiv-2510.16917-brightgreen)](https://arxiv.org/abs/2510.16917)

This is the official Github repository for the paper [SAKE: Towards Editing Auditory Attribute Knowledge of Large Audio-Language Models](https://arxiv.org/abs/2510.16917). The repository currently contains the dataset presented in the paper. More details will be added soon.

## Dataset
We introduce **SAKE**, the first benchmark for auditory attribute knowledge editing in LALMs. SAKE convers four auditory attributes: speaker gender, speaker emotion, spoken language, and animal sounds. The benchmark consists of 4000 training instances and 1200 testing instances.

For the audio files used in the dataset, please refer to the instructions in `audio_downloader/README.md` to download them.

The full dataset can found under `data/` directory. The structure is as follows:
```
SAKE
|-- data
|   |-- train                       # Training set
|   |   |-- ALL_train.json          # All data in the training set that we used for training in the paper
|   |   |-- ALL_val.json            # All data in the training set that we used for validation in the paper
|   |   |-- {attribute}.json        # All data targeting {attribute} in the training set
|   |-- test
|   |   |-- single_editing          # Testing set for single editing
|   |   |   |-- {attribute}.json    # All data targeting {attribute} in the testing set
|   |   |-- sequential_editing      # Testing set for sequential editing
|   |   |   |-- all_sequences.json  # All ten sequences for sequential editing in the testing set
|   |   |   |-- sequences
|   |   |   |   |-- seq_{0-9}.json  # Individual editing sequence for sequential editing in the testing set, and each sequence contains ten editing instances
```

Each editing instance in the dataset is represented as a JSON object with the following format:
```json
{
    "file": "audio file name",
    "original_answer": "original attribute label",
    "edited_answer": "target attribute label after editing",
    "reliability_question": "question used for reliability evaluation",
    "generality": [
        {
            "file": "audio file name",
            "question": "question used for generality evaluation",
            "answer": "expected answer"
        }, ...
    ],
    "locality": {
        "audio": [
            {
                "track": "the auditory attribute",
                "file": "audio file name",
                "question": "question used for audio locality evaluation",
                "answer": "expected answer"
            }, ...
        ],
        "text": [
            {
                "question": "question used for text locality evaluation",
                "answer": "ground truth answer from MMAU"
            }
        ]
    },
    "portability": {
        "audio": {
            "file": "audio file name",
            "question": "question used for audio portability evaluation",
            "answer": "expected answer"
        }
    }
}
```
More details about some of the metric:
- Generality: It should contain three questions to evaluate the generality of the editing, which are type 1, 2, and 3 as described in the paper.
- Audio Locality: It should contain four questions to evaluate the audio locality of the editing, which are type 1, 2, 3, and 4 as described in the paper. For speaker gender editing, however, it only includes three questions, which are type 1, 3, and 4, since type 2 audio locality is not applicable.
- Text Locality: It should contain one question to evaluate the text locality of the editing.