import argparse
from sensitibot.github import *

from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser()

    #parser.add_argument("owner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--local', metavar="PATH", const='./', nargs='?', help='use a local repository (default: current directory)')
    group.add_argument('-g', '--github', metavar='USER', help='use a GitHub repository')
    parser.add_argument('-r', '--repository', metavar='REPO',  help='the repository to use (only if --github is used)')

    args = parser.parse_args()

    if args.github:
        if args.repository:
            data = getFilesFromRepository(args.github, args.repository)

            # Write data to file
            os.makedirs("outputs", exist_ok=True)
            with open('outputs/data.json', 'w') as f:
                f.write(data)
        else:
            data = getFilesFromRepositories(args.github)

            # Write data to file
            os.makedirs("outputs", exist_ok=True)
            with open('outputs/data.json', 'w') as f:
                f.write(data)

    elif args.local:
        if args.local == './' or args.local == None:
            print("Using local repository: current directory")
        else:
            print(f"Using local repository: {args.local}")
