import argparse
import requests
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN", default=None)

parser = argparse.ArgumentParser()

parser.add_argument("owner")

args = parser.parse_args()

url = 'https://api.github.com'

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

def getFilesFromRepositories(owner):
    response = requests.get(f'{url}/users/{owner}/repos', headers=headers)
    json_data_1 = response.json()

    for repo in json_data_1:
        response = requests.get(f'{url}/repos/{owner}/{repo["name"]}/git/trees/{repo["default_branch"]}?recursive=1',headers=headers)
        tree = response.json()

        print(f'{repo["name"]}')
        printTree(tree)
        print("\n")

def printTree(tree):
    for file in tree["tree"]:
        if(file["type"] == "blob"):
            print(f'\t {file["path"]}')

tree = getFilesFromRepositories(args.owner)
