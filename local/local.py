import os

from reader import reader


def process_local(directory=None, deep_search=False):
    """
    Initiates the process of getting the files from the local repository.

    Args:
        directory (str): The directory to search.
        deep_search (bool): If true, the content of the files will be analyzed.

    Returns:
        dict: The result of getting the files.
    """
    files = get_files_recursively(directory)

    if files == None:
        return None

    result = reader.process_files(files, deep_search)

    return result


def get_files_recursively(directory):
    """
    Gets the files from the local directory.

    Args:
        directory (str): The directory to search.

    Returns:
        dict: The files from the local directory.
    """
    if directory == None:
        directory = "./"

    result = {"repositories": [{"name": "local", "files": []}]}

    for root, _, files in os.walk(directory):
        for filename in files:

            if filename.endswith('.csv'):
                filepath = os.path.join(root, filename)
                result["repositories"][0]["files"].append(filepath)

    # Only return the result if there are files of any type
    if len(result["repositories"][0]["files"]) == 0:
        return None

    return result
