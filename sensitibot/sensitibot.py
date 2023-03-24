import argparse
import os
from github import github
from local import local

def main():
    parser = argparse.ArgumentParser()

    #parser.add_argument("owner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--local', metavar="PATH", const='./', nargs='?', help='use a local repository (default: current directory)')
    group.add_argument('-g', '--github', metavar='USER', help='use a GitHub repository')
    parser.add_argument('-r', '--repository', metavar='REPO',  help='the repository to use (only if --github is used)')
    parser.add_argument('-b', '--branch', metavar='BRANCH', help='the branch to use (only if --repository is used)')

    args = parser.parse_args()

    data = ""

    if args.github:
        data = github.processGitHub(args.github, args.repository, args.branch)

    elif args.local:
        data = local.processLocal(args.local)
    
    # Write data to file
    os.makedirs("outputs", exist_ok=True)
    with open('outputs/data.json', 'w') as f:
        f.write(data)
        