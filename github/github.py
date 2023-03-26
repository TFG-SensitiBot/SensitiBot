import sys
import requests
import os

import urllib
from reader import reader

api_url = 'https://api.github.com'
raw_url = 'https://raw.githubusercontent.com'
headers = {}


def processGitHub(owner, repository=None, branch=None):
    files = {}
    if repository == None:
        files = getFilesFromRepositories(owner)
    else:
        files = {"repositories": [
            getFilesFromRepository(owner, repository, branch)]}

    result = reader.processFiles(files)

    return result


def getRateLimit():
    TOKEN = os.getenv("GITHUB_TOKEN", default=None)

    if TOKEN != None:
        headers['Authorization'] = f'Bearer {TOKEN}'

    response = requests.get(f'{api_url}/rate_limit', headers=headers)
    json_data = response.json()
    return json_data


def getFilesFromRepositories(owner):
    TOKEN = os.getenv("GITHUB_TOKEN", default=None)

    if TOKEN != None:
        headers['Authorization'] = f'Bearer {TOKEN}'

    response = requests.get(f'{api_url}/users/{owner}/repos', headers=headers)
    if not response.ok:
        error = response.json()
        error_message = error.get('message')
        print(f'Error: Github User or Organization {error_message}')
        sys.exit(1)  # exit with non-zero exit code

    json_repos = response.json()

    result = {"repositories": []}

    for repository in json_repos:
        result_repository = getFilesFromRepository(
            owner, repository["name"], repository["default_branch"])
        
        if result_repository == None:
            continue

        result["repositories"].append(result_repository)

    return result


def getFilesFromRepository(owner, repository, branch=None):
    TOKEN = os.getenv("GITHUB_TOKEN", default=None)

    if TOKEN != None:
        headers['Authorization'] = f'Bearer {TOKEN}'

    # In case the branch is not specified, we need to get the default branch
    if branch == None:
        response = requests.get(
            f'{api_url}/repos/{owner}/{repository}', headers=headers)
        if not response.ok:
            error = response.json()
            error_message = error.get('message')
            print(f'Error: Repository {error_message}')
            sys.exit(1)  # exit with non-zero exit code

        json_repo = response.json()
        branch = json_repo["default_branch"]

    response = requests.get(
        f'{api_url}/repos/{owner}/{repository}/git/trees/{branch}?recursive=1', headers=headers)
    if not response.ok:
        error = response.json()
        error_message = error.get('message')
        if error_message == "Git Repository is empty.":
            return None

        print(f'Error: Repository {error_message}')
        sys.exit(1)  # exit with non-zero exit code

    json_files = response.json()

    result_repository = {"name": repository, "types": []}

    # Types of files to be considered
    csv_files = []

    for file in json_files["tree"]:
        if (file["type"] == "blob"):

            if file["path"].endswith(".csv"):
                csv_files.append(
                    urllib.parse.quote(f'{raw_url}/{owner}/{repository}/master/{file["path"]}', safe=':/.'))

    result_repository["types"] = {"type": "csv_files", "files": csv_files}

    return result_repository
