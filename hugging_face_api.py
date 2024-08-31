# Using HuggingFace API to download a dataset and save to csv files,
# which are "hugging_face_api_train.csv" and "hugging_face_api_test.csv"
# in the same directory.

import pathlib
from datasets import load_dataset


def main(train_csv_file: pathlib.Path, test_csv_file: pathlib.Path):
    """
    Using HuggingFace API to download a dataset and save to csv files
    """

    # loading dataset
    dataset = load_dataset("lmsys/toxic-chat", "toxicchat0124")

    # dump to csv files
    dataset["train"].to_csv(train_csv_file)
    dataset["test"].to_csv(test_csv_file)


if __name__ == "__main__":
    # get the directory of current python file, which also is the project root dir
    CURRENT_DIR = pathlib.path(__file__).parent

    # execute the main function
    main(
        CURRENT_DIR / "hugging_face_api_train.csv",
        CURRENT_DIR / "hugging_face_api_test.csv",
    )
