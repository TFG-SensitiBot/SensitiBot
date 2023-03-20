import requests
import os
import json

api_url = 'https://api.github.com'
raw_url = 'https://raw.githubusercontent.com'
headers = {}

def getRateLimit():
    TOKEN = os.getenv("GITHUB_TOKEN", default=None)

    if TOKEN != None:
        headers['Authorization'] = f'Bearer {TOKEN}'

    response = requests.get(f'{api_url}/rate_limit', headers=headers)
    json_data = response.json()
    return json_data

def getFilesFromRepositories(owner):
    response = requests.get(f'{api_url}/users/{owner}/repos', headers=headers)
    json_repos = response.json()

    repositories = {}

    for repo in json_repos:
        response = requests.get(f'{api_url}/repos/{owner}/{repo["name"]}/git/trees/{repo["default_branch"]}?recursive=1',headers=headers)
        json_files = response.json()
        
        csv_files = []
        for file in json_files["tree"]:
            if(file["type"] == "blob" and file["path"].endswith(".csv")):
                csv_files.append(f'{raw_url}/{owner}/{repo["name"]}/{repo["default_branch"]}/{file["path"]}')

        repositories[repo["name"]] = csv_files

    return json.dumps(repositories)
