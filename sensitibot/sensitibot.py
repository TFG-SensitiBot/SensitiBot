import argparse
import json
import os
import subprocess
import tempfile
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

    result = ""

    if args.github:
        result = github.processGitHub(args.github, args.repository, args.branch)

    elif args.local:
        result = local.processLocal(args.local)

    
    data = json.dumps(result, indent=4, sort_keys=True)
    
    # Write result to temp file and open it
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(data)
        f.close()

    if os.name == 'nt':  # For Windows
        subprocess.Popen(["notepad.exe", f.name])
    elif os.name == 'posix':  # For Linux and macOS
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, f.name])
    else:
        raise OSError('Unsupported operating system')
