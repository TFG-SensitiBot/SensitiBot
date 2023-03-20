import argparse
from sensitibot.github import *

from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("owner")

    args = parser.parse_args()

    data = getFilesFromRepositories(args.owner)

    # Write data to file
    os.makedirs("outputs", exist_ok=True)
    with open('outputs/data.json', 'w') as f:
        f.write(data)
