import os

from reader import reader


def processLocal(directory=None):
    files = getFilesRecursively(directory)

    result = reader.processFiles(files)

    return result


def getFilesRecursively(directory):
    if directory == None:
        directory = "./"

    result = {"repositories": [{"name": "local", "types": []}]}

    # Types of files to be considered
    csv_files = []

    for root, directories, files in os.walk(directory):
        for filename in files:

            if filename.endswith('.csv'):
                filepath = os.path.join(root, filename)
                csv_files.append(filepath)

    result["repositories"][0]["types"] = {
        "type": "csv_files", "files": csv_files}

    return result
