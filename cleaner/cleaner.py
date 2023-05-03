import pandas as pd
from tqdm import tqdm
import os


def clean_files(files, replace_files=False):
    """
    Initiates the process of cleaning the files.

    Args:
        files (dict): The files to clean.
        replace_files (bool): If true, the files will be replaced by the clean ones.

    Returns:
        None.
    """
    repository = files["repositories"][0]

    for type in repository["types"]:
        if type["type"] == "csv_files":
            csv_files = type["files"]
            clean_csv_files(csv_files, replace_files)


def clean_csv_files(files, replace_files=False):
    """
    Cleans the csv files.

    Args:
        files (list): The csv files to clean.
        replace_files (bool): If true, the files will be replaced by the clean ones.

    Returns:
        None.
    """
    pbar = tqdm(files,
                desc="Cleaning csv files", ncols=300, unit=" repo", bar_format="\tCleaning csv file {n_fmt}/{total_fmt} |{bar:20}| f:{desc}")
    errors = []
    for file in pbar:
        filename = file["name"]
        pbar.set_description(filename[-50:])

        positive_headers = file["positive_headers"] if "positive_headers" in file else [
        ]
        positive_columns = file["positive_columns"] if "positive_columns" in file else [
        ]

        try:
            data = pd.read_csv(file["name"], comment='#', sep=None, engine='python',
                               encoding='latin-1', skip_blank_lines=True)
        except Exception as e:
            error = {"file": file["name"], "error": str(e)}
            errors.append(error)
            continue

        columns = data.columns.values
        for column in columns:
            if column in positive_headers or column in positive_columns:
                data = data.drop(column, axis=1)

        base_filename, extension = os.path.splitext(filename)

        if not replace_files:
            base_filename = base_filename + "_clean"

        new_filename = base_filename + extension
        data.to_csv(new_filename, index=False)
