import itertools
import re

import pandas as pd
from tqdm import tqdm


def processFiles(files):
    repositories = files["repositories"]
    result = {"repositories": []}

    for repository in repositories:
        print(f"\nAnalyzing repository {repository['name']}:")
        result_repository = {
            "name": repository["name"], "types": []}

        if repository["types"]["type"] == "csv_files":
            csv_files = repository["types"]["files"]

            # Only analyze if there are files
            if len(csv_files) == 0:
                print("\tNo csv files found")
            else:
                csv_result = readcsvFiles(csv_files)

                # Only add the file type if there are files with errors
                if len(csv_result["files"]) != 0 or len(csv_result["errors"]) != 0:
                    result_repository["types"].append(csv_result)

        # Only add repository if it has files with errors
        if len(result_repository["types"]) != 0:
            result["repositories"].append(result_repository)

    return result if len(result['repositories']) != 0 else None


def readcsvFiles(files):
    result = {"type": "csv_files", "files": [], "errors": []}
    pbar = tqdm(files,
                desc="Analyzing csv files", ncols=300, unit=" repo", bar_format="\tAnalyzing csv file {n_fmt}/{total_fmt} |{bar:20}| f:{desc}")
    errors = []
    for file in pbar:
        pbar.set_description(file[-50:])

        try:
            data = pd.read_csv(file, comment='#', sep=None, engine='python',
                               encoding='utf-8', skip_blank_lines=True)
        except:
            errors.append(f"Error reading file {file}")
            continue

        columns = data.columns.values
        result_headers = analizeHeaders(file, columns)

        # Only show files that have errors
        if len(result_headers["result_error"]) != 0:
            result["files"].append(result_headers)

    result["errors"] = errors

    return result


def analizeHeaders(name, headers):
    terms = ["email", "phone", "mobile", "iban", "account", "sha", "gpg", "socialsecurity", "creditcard", "debitcard", "card", "name", "surname", "lastname", "firstname", "dni",
             "license", "licenses", "lecenseplates", "ip", "ips", "address", "addresses", "gps", "coordinate", "coordinates", "location", "password", "passwords", "secret", "secrets", "key", "hash"]
    suffixes = ["number", "value", "key"]

    combinations = []
    for term, suffix in itertools.product(terms, suffixes):
        combinations.append(term)
        combinations.append(term + ' ' + suffix)
        combinations.append(term + suffix)

    result = {}
    error = []
    for header in headers:
        header = header.strip().lower()
        if header in combinations:
            error.append(header)

    result["name"] = name
    result["result_error"] = error

    return result
