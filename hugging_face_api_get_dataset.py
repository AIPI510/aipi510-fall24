"""
## Assignment Info

Team: XKJX

Team Members:
  - Xiaoquan Kong
  - Jinglong Xiong

Topic: Using Hugging Face API for getting datasets

Video: https://drive.google.com/file/d/1lORgPMHKmjmzlkpEHNj5AGFQEXfi7t_y/view?usp=sharing

## Function description

This is a Python script to download datasets from the Hugging Face Hub.
It allows you to specify the dataset name, choose a configuration, and download specific splits or the entire dataset.
The downloaded dataset is then saved to a specified directory on your local machine.


## install dependencies

```bash
pip install datasets==2.21.0
pip install click==8.1.7
```

## How to use it?

The script provides a command-line interface to download datasets.
You can specify the dataset name, the desired split (e.g., `train`, `test`, `validation`, or `all`),
and the directory where you want to save the dataset.

### Command Syntax

```bash
python hugging_face_api_get_dataset.py [DATASET_NAME] [OPTIONS]
```

following documentation contains more concrete examples for this.

### Arguments

- `DATASET_NAME`: The name of the dataset to download from the Hugging Face Hub. This argument is required.

### Options

- `--split`: The dataset split to download. You can specify `train`, `test`, `validation`, or `all` (default: `all`).
- `--save_dir`: The directory where the dataset should be saved. If not provided, it defaults to the name of the dataset.

### Examples

1. Download the entire dataset:

   ```bash
   python hugging_face_api_get_dataset.py lmsys/toxic-chat --split all --save_dir ./lmsys-toxic-chat
   ```

   This command will download all splits of the "lmsys/toxic-chat" dataset and save them in the `./lmsys-toxic-chat` directory.

2. Download only the training split:

   ```bash
   python hugging_face_api_get_dataset.py lmsys/toxic-chat --split train --save_dir ./lmsys-toxic-chat-train
   ```

   This command will download only the training split of the "lmsys/toxic-chat" dataset and save it in the `./lmsys-toxic-chat-train` directory.

3. Download a dataset with multiple configurations:

   If a dataset has multiple configurations, the tool will list all available configurations and prompt you to select one.
   The dataset will then be downloaded according to your selection.

### Error Handling

- If the specified save directory already exists, the tool will prompt you to choose a different directory or delete the existing one.
- If an invalid configuration or split is selected, the tool will notify you and exit.

## Test coverage

This tool has been tested in python 3.9 and 3.10 by hand.
"""

import os
import click
from datasets import load_dataset, get_dataset_config_names


@click.command()
@click.argument("dataset_name")
@click.option(
    "--split",
    default="all",
    help='The dataset split to download, e.g., "all", "train", "test", "validation". Defaults to "all".',
)
@click.option(
    "--save_dir",
    default=None,
    help="Directory to save the dataset. Defaults to dataset_name.",
)
def download_dataset(dataset_name, split, save_dir):
    """
    CLI tool to download datasets from the Hugging Face Hub.

    DATASET_NAME: The name of the data set to download.
    """
    try:
        # Set default save directory to dataset_name if not provided
        if save_dir is None:
            save_dir = dataset_name

        # Check if the save directory already exists
        if os.path.exists(save_dir):
            click.echo(
                f"Directory '{save_dir}' already exists. Please choose a different save directory or delete the existing one.",
                err=True,
            )
            return

        # Get all available configs for the dataset
        configs = get_dataset_config_names(dataset_name)
        if configs:
            click.echo(f"Available configurations for '{dataset_name}':")
            for i, config in enumerate(configs):
                click.echo(f"{i + 1}. {config}")

            # Ask user to select a configuration
            config_choice = click.prompt(
                f"Enter the number of the configuration to download (1-{len(configs)})",
                type=int,
            )
            if config_choice < 1 or config_choice > len(configs):
                click.echo(
                    f"Invalid selection. Please choose a number between 1 and {len(configs)}.",
                    err=True,
                )
                return
            config_name = configs[config_choice - 1]
            click.echo(f"Selected configuration: {config_name}")
        else:
            config_name = None

        if split == "all":
            dataset = load_dataset(
                dataset_name, name=config_name, trust_remote_code=True
            )
            for split_name in dataset.keys():
                split_save_dir = os.path.join(save_dir, split_name)
                dataset[split_name].save_to_disk(split_save_dir)
                click.echo(
                    f"Split '{split_name}' downloaded and saved to '{split_save_dir}'."
                )
        elif split:
            dataset = load_dataset(
                dataset_name, name=config_name, split=split, trust_remote_code=True
            )
            dataset.save_to_disk(save_dir)
            click.echo(
                f"Dataset '{dataset_name}' ({split} split) downloaded and saved to '{save_dir}'."
            )
        else:
            dataset = load_dataset(
                dataset_name, name=config_name, trust_remote_code=True
            )
            dataset.save_to_disk(save_dir)
            click.echo(
                f"Dataset '{dataset_name}' downloaded and saved to '{save_dir}'."
            )

    except Exception as e:
        click.echo(f"Error downloading dataset: {e}", err=True)


if __name__ == "__main__":
    download_dataset()
