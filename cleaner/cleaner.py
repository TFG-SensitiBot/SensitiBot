import pandas as pd
from tqdm import tqdm
import os


def process_cleaner(files):
    generate_clean_files = input(
        "\nDo you want to generate clean files? (yes/no) ")
    while generate_clean_files.lower() not in ("yes", "no"):
        generate_clean_files = input("Please enter either 'yes' or 'no': ")
    if generate_clean_files.lower() == "yes":

        replace_files = input(
            "\nDo you want to replace the files? (yes/no) ")
        while replace_files.lower() not in ("yes", "no"):
            replace_files = input("Please enter either 'yes' or 'no': ")
        if replace_files.lower() == "yes":

            replace_files_2 = input(
                "\nAre you sure you want to replace the files? (yes/no) ")
            while replace_files_2.lower() not in ("yes", "no"):
                replace_files_2 = input(
                    "Please enter either 'yes' or 'no': ")
            if replace_files_2.lower() == "yes":
                clean_files(files, True)
            else:
                clean_files(files, False)
        else:
            clean_files(files, False)


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

    pbar = tqdm(repository["files"],
                desc="Cleaning files", ncols=300, unit=" repo", bar_format="\tCleaning file {n_fmt}/{total_fmt} |{bar:20}| f:{desc}")
    for file in pbar:
        pbar.set_description(file["name"][-50:])
        clean_file(file, replace_files)


def clean_file(file, replace_files=False):
    """
    Cleans the file.

    Args:
        file (str): The file to clean.

    Returns:
        None.
    """
    if file["name"].endswith('.csv'):
        clean_csv_file(file, replace_files)


def clean_csv_file(file, replace_files=False):
    """
    Cleans the csv files.

    Args:
        files (list): The csv files to clean.
        replace_files (bool): If true, the files will be replaced by the clean ones.

    Returns:
        None.
    """
    filename = file["name"]
    positive_headers = file["positive_headers"] if "positive_headers" in file else [
    ]
    positive_columns = file["positive_columns"] if "positive_columns" in file else [
    ]

    try:
        data = pd.read_csv(filename, comment='#', sep=None, engine='python',
                           encoding='latin-1', skip_blank_lines=True)
    except Exception as e:
        error = {"file": filename, "error": str(e)}

    columns = data.columns.values
    for column in columns:
        if column in positive_headers or column in positive_columns:
            data = data.drop(column, axis=1)

    base_filename, extension = os.path.splitext(filename)

    if not replace_files:
        base_filename = base_filename + "_clean"

    new_filename = base_filename + extension
    data.to_csv(new_filename, index=False)
