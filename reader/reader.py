import re

import pandas as pd
from tqdm import tqdm


def processFiles(files):
    repositories = files["repositories"]
    result = {"repositories": []}

    for repository in repositories:
        result_repository = {"name": repository["name"], "types": []}

        if repository["types"]["type"] == "csv_files":
            csv_files = repository["types"]["files"]
            csv_result = readcsvFiles(csv_files)
            result_repository["types"].append(csv_result)

        result["repositories"].append(result_repository)

    return result


def readcsvFiles(files):
    result = {"type": "csv_files", "files": []}
    for file in tqdm(files, desc="Reading csv files", ncols=100, unit=" file"):
        data = pd.read_csv(file, comment='#')

        columns = data.columns.values
        result_headers = analizeHeaders(file, columns)

        result["files"].append(result_headers)

    return result


def analizeHeaders(name, headers):
    terms = ["email", "phone", "iban", "account", "sha", "gpg", "socialSecurity", "creditCard", "debitCard", "name", "surname", "lastname", "firstname", "dni",
             "license", "lecensePlate", "IP", "address", "gps", "coordinates", "location", "password", "secret", "key", "hash"]
    suffixes = ["number", "value", "key"]

    regex = r'^(?:' + '|'.join(terms) + r')(?: ' + '| '.join(suffixes) + r')?$'
    pattern = re.compile(regex)

    result = {}
    correct = []
    error = []
    for header in headers:
        header = header.strip().lower()
        if pattern.match(header):
            error.append(header)
        else:
            correct.append(header)

    result["name"] = name
    result["result_correct"] = correct
    result["result_error"] = error

    return result
