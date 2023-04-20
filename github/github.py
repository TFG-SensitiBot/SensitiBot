import os
import sys
import urllib

import requests
from tqdm import tqdm

from reader import reader

api_url = 'https://api.github.com'
raw_url = 'https://raw.githubusercontent.com'
headers = {}
multipleRepositories = False


def processGitHub(owner, repository=None, branch=None, token=None):
    global multipleRepositories
    TOKEN = os.getenv("GITHUB_TOKEN", default=None)
    if token != None:
        TOKEN = token

    if TOKEN != None:
        headers['Authorization'] = f'Bearer {TOKEN}'

    files = {}
    result = {}
    if repository == None:
        multipleRepositories = True
        files = getFilesFromRepositories(owner)
    else:
        print(f'Searching repositoriy {owner}/{repository}:')
        files = getFilesFromRepository(owner, repository, branch)
        if files != None:
            files = {"repositories": [files]}

    if files == None:
        sys.exit(1)  # exit with non-zero exit code

    result = reader.processFiles(files)

    return result


def getRateLimit():
    response = requests.get(f'{api_url}/rate_limit', headers=headers)
    json_data = response.json()
    return json_data["rate"]["remaining"]


def getFilesFromRepositories(owner):
    print(f'Searching repositories for {owner}:')

    json_repos = {}
    per_page = 100
    count = per_page
    page = 1
    while count == per_page:
        response = requests.get(
            f'{api_url}/users/{owner}/repos?page={page}&per_page={per_page}', headers=headers)
        if not response.ok:
            error = response.json()
            error_message = error.get('message')
            if error_message == "Not Found":
                print(f'Error: Github User or Organization {error_message}')
                sys.exit(1)  # exit with non-zero exit code
            elif error_message == "Bad credentials":
                print("Error: Bad credentials")
                sys.exit(1)  # exit with non-zero exit code
            elif "API rate limit exceeded" in error_message:
                if page == 1:   # If the first request has already exceeded the rate limit, we can't continue
                    print(
                        "API rate limit exceeded, could not analyze GitHub user or organization.")
                    return None
                else:           # If the rate limit has been exceeded after the first request, we can continue with the repositories already found
                    print(
                        "API rate limit exceeded, not all repositories will be analyzed.")
                    break

        if page == 1:
            json_repos = response.json()
        else:
            json_repos.extend(response.json())
        page += 1
        count = len(response.json())

    print(f'\t{len(json_repos)} public repositories found\n')

    result = {"repositories": []}

    number_of_repos = len(json_repos)
    remaining = getRateLimit()
    if remaining <= number_of_repos:
        number_of_repos = remaining
        print(
            f'Warning: Only {number_of_repos} repositories will be analyzed, because the GitHub API rate limit has been exceeded.')

    pbar = tqdm(range(0, number_of_repos),
                desc="Reading repositories", ncols=200, unit=" repo", bar_format="Reading repository {n_fmt}/{total_fmt} |{bar:20}| r:{desc}")
    for i in pbar:
        repository = json_repos[i]
        pbar.set_description(repository["name"])
        result_repository = getFilesFromRepository(
            owner, repository["name"], repository["default_branch"])

        if result_repository == None:
            continue

        result["repositories"].append(result_repository)

    return result


def getFilesFromRepository(owner, repository, branch=None):
    # In case the branch is not specified, we need to get the default branch
    if branch == None:
        branch = getDefaultBranchOfRepository(owner, repository)

    response = requests.get(
        f'{api_url}/repos/{owner}/{repository}/git/trees/{branch}?recursive=1', headers=headers)
    if not response.ok:
        error = response.json()
        error_message = error.get('message')
        if error_message == "Not Found":
            if multipleRepositories:
                return None
            else:
                print(f'Error: Repository {error_message}')
                sys.exit(1)  # exit with non-zero exit code
        elif error_message == "Bad credentials":
            print("Error: Bad credentials")
            sys.exit(1)  # exit with non-zero exit code
        elif error_message == "Git Repository is empty.":
            return None
        elif "API rate limit exceeded" in error_message:
            print("API rate limit exceeded")
            return None

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


def getDefaultBranchOfRepository(owner, repository):
    response = requests.get(
        f'{api_url}/repos/{owner}/{repository}', headers=headers)
    if not response.ok:
        error = response.json()
        error_message = error.get('message')
        if error_message == "Not Found":
            if multipleRepositories:
                return None
            else:
                print(f'Error: Repository {error_message}')
                sys.exit(1)  # exit with non-zero exit code
        elif error_message == "Bad credentials":
            print("Error: Bad credentials")
            sys.exit(1)  # exit with non-zero exit code
        elif "API rate limit exceeded" in error_message:
            print(
                "API rate limit exceeded, not all repositories have been analyzed.")
            return None

    json_repo = response.json()
    return json_repo["default_branch"]
