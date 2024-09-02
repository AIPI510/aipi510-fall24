"""
Team: XKJX

Team Members:
  - Xiaoquan Kong
  - Jinglong Xiong

Topic: Using Hugging Face API for getting datasets

Video: <TODO: insert a URL here>


## install dependencies

```bash
pip install datasets==2.21.0
pip install click==8.1.7
```

## How to use it?

<TODO>
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
