import itertools
import re

import pandas as pd
from tqdm import tqdm


def process_files(files, deep_search=False):
    repositories = files["repositories"]
    result = {"repositories": []}

    for repository in repositories:
        print(f"\nAnalyzing repository {repository['name']}:")
        result_repository = {
            "name": repository["name"], "types": []}

        for type in repository["types"]:
            if type["type"] == "csv_files":
                csv_files = type["files"]

                # Only analyze if there are files
                if len(csv_files) == 0:
                    print("\tNo csv files found")
                else:
                    csv_result = read_csv_files(csv_files, deep_search)

                    # Only add the file type if there are files with errors
                    if len(csv_result["files"]) != 0 or len(csv_result["errors"]) != 0:
                        result_repository["types"].append(csv_result)

        # Only add repository if it has files with errors
        if len(result_repository["types"]) != 0:
            result["repositories"].append(result_repository)

    return result if len(result['repositories']) != 0 else None


def read_csv_files(files, deep_search=False):
    result = {"type": "csv_files", "files": [], "errors": []}
    pbar = tqdm(files,
                desc="Analyzing csv files", ncols=300, unit=" repo", bar_format="\tAnalyzing csv file {n_fmt}/{total_fmt} |{bar:20}| f:{desc}")
    errors = []
    for file in pbar:
        pbar.set_description(file[-50:])

        try:
            data = pd.read_csv(file, comment='#', sep=None, engine='python',
                               encoding='latin-1', skip_blank_lines=True)
        except Exception as e:
            error = {"file": file, "error": str(e)}
            errors.append(error)
            continue

        result_file = {"name": file}

        headers = data.columns.values
        result_headers = analize_headers(file, headers)

        # Only show headers that have errors
        if len(result_headers) != 0:
            result_file["positive_headers"] = result_headers

        # Only analyze columns if deep_search is enabled
        if deep_search:
            result_columns = analize_columns(file, data, headers)

            # Only show columns that have errors
            if len(result_columns) != 0:
                result_file["positive_columns"] = result_columns

        if len(result_file) != 1:
            result["files"].append(result_file)

    result["errors"] = errors

    return result


def analize_headers(name, headers):
    terms = ["email", "phone", "mobile", "iban", "account", "sha", "gpg", "socialsecurity",
             "creditcard", "debitcard", "card", "name", "surname", "lastname", "firstname", "dni",
             "license", "licenses", "lecenseplates", "ip", "ips", "address", "addresses", "gps",
             "coordinate", "coordinates", "location", "password", "latitud", "latitude", "longitud",
             "longitude", "passwords", "secret", "secrets", "key", "hash"]
    suffixes = ["number", "value", "key"]

    combinations = []
    for term, suffix in itertools.product(terms, suffixes):
        combinations.append(term)
        combinations.append(term + ' ' + suffix)
        combinations.append(term + suffix)

    positive_headers = []
    for header in headers:
        header = header.strip().lower()
        if header in combinations:
            positive_headers.append(header)

    return positive_headers


def analize_columns(name, data, columns):
    positive_columns = []
    number_of_rows = len(data)
    ratio = number_of_rows * 0.1

    for column in columns:
        result_column = {"column": column}

        positive_fields = []

        count = 0
        for index, value in data[column].items():
            result_field = analize_field(str(value))
            if result_field != None:
                count += 1
                positive_fields.append(result_field)

            if count >= ratio:
                break

        result_column["positive_fields"] = list(set(positive_fields))

        if len(result_column["positive_fields"]) != 0:
            positive_columns.append(result_column)

    return positive_columns


def analize_field(field):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    iban_pattern = r'^[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}$'
    phone_pattern = r'^\+?[0-9]{6,}$'
    dni_pattern = r'^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$'

    patterns = {"email": email_pattern, "iban": iban_pattern,
                "phone": phone_pattern, "dni": dni_pattern}

    for type, pattern in patterns.items():
        if re.match(pattern, field):
            return type

    return None
