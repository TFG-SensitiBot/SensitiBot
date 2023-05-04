import itertools


def analize_headers(name, headers):
    """
    Analyzes the headers of a file.

    Args:
        name (str): The name of the file.
        headers (list): The headers of the file.

    Returns:
        list: The headers that may have sensitive information.
    """
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
