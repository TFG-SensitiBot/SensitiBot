import os

import pandas as pd


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
    positive_columns = file["positive_columns"] if "positive_columns" in file else dict(
    )

    try:
        data = pd.read_csv(filename, comment='#', sep=None,
                           engine='python', skip_blank_lines=True, dtype=str)
    except Exception as e:
        error = {"file": filename, "error": str(e)}

    columns = data.columns.values
    for column in columns:
        if column in positive_headers or column in list(positive_columns.keys()):
            data = data.drop(column, axis=1)

    base_filename, extension = os.path.splitext(filename)

    if not replace_files:
        base_filename = base_filename + "_clean"

    new_filename = base_filename + extension
    data.to_csv(new_filename, index=False)
