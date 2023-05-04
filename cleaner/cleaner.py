from tqdm import tqdm

from cleaner import csv_cleaner


def process_cleaner(files):
    generate_clean_files = input(
        "\nDo you want to generate clean files? (yes/no) ")
    while generate_clean_files.lower() not in ("yes", "no"):
        generate_clean_files = input("Please enter either 'yes' or 'no': ")
    if generate_clean_files.lower() == "yes":
        clean_files(files)


def clean_files(files):
    """
    Initiates the process of cleaning the files.

    Args:
        files (dict): The files to clean.
        replace_files (bool): If true, the files will be replaced by the clean ones.

    Returns:
        None.
    """
    repository = files["repositories"][0]

    # pbar = tqdm(repository["files"],
    #             desc="Cleaning files", ncols=300, unit=" repo", bar_format="\tCleaning file {n_fmt}/{total_fmt} |{bar:20}| f:{desc}")
    for file in repository["files"]:
        # pbar.set_description(file["name"][-50:])
        clean_file(file)


def clean_file(file):
    """
    Cleans the file.

    Args:
        file (str): The file to clean.

    Returns:
        None.
    """
    print("\nCleaning file: " + file["name"])

    matches = ""

    if "positive_headers" in file:
        for positive_header in file['positive_headers']:
            matches = f"{matches}\tHeader {positive_header} may contain sensible data\n"

    if "positive_columns" in file:
        for positive_column, positive_fields in file['positive_columns'].items():
            matches = f"{matches}\tColumn: {positive_column}:\tDetected fields: {positive_fields}\n"

    print(matches)

    clean, replace = ask_clean_file()

    if clean:
        if file["name"].endswith('.csv'):
            csv_cleaner.clean_csv_file(file, replace)


def ask_clean_file():
    """
    Asks the user if he wants to clean the file.

    Args:
        None.

    Returns:
        bool: True if the user wants to clean the file, False otherwise.
        bool: True if the user wants to replace the file, False otherwise.
    """
    ask_clean = input("Do you want to clean this file? (yes/no) ")
    while ask_clean.lower() not in ("yes", "no"):
        ask_clean = input("Please enter either 'yes' or 'no': ")
    if ask_clean.lower() == "yes":

        replace_files = input(
            "Do you want to replace the files? (yes/no) ")
        while replace_files.lower() not in ("yes", "no"):
            replace_files = input("Please enter either 'yes' or 'no': ")
        if replace_files.lower() == "yes":

            replace_files_2 = input(
                "Are you sure you want to replace the files? (yes/no) ")
            while replace_files_2.lower() not in ("yes", "no"):
                replace_files_2 = input(
                    "Please enter either 'yes' or 'no': ")
            if replace_files_2.lower() == "yes":
                return True, True
            else:
                return True, False
        else:
            return True, False
    else:
        return False, False
