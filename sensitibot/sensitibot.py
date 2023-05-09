import argparse
import sys

from cleaner import cleaner
from github import github
from local import local
from renderer import renderer


def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument("owner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--local', metavar="PATH", const='./', nargs='?',
                       help='search in local repository (default: current directory)')
    group.add_argument('-g', '--github', metavar='USER',
                       help='search in GitHub\'s user')
    parser.add_argument('-r', '--repository', metavar='REPO',
                        help='the repository to use (only if --github is used)')
    parser.add_argument('-b', '--branch', metavar='BRANCH',
                        help='the branch to use (only if --repository is used)')
    parser.add_argument('-t', '--token', metavar='TOKEN',
                        help='the token to use (only if --github is used)')
    parser.add_argument('--deep-search', action='store_true',
                        help='analyze content of files')

    args = parser.parse_args()

    result = ""

    if args.github:
        result = github.process_github(
            args.github, args.repository, args.branch, args.token, args.deep_search)

    elif args.local:
        if args.repository or args.branch or args.token:
            print(
                "usage: sensitibot [-h] (-l [PATH] | -g USER) [-r REPO] [-b BRANCH] [-t TOKEN] [--deep-search]")
            print(
                "sensitibot: error: arguments -r/--repository, -b/--branch and -t--token: not allowed with argument -l/--local")
            sys.exit(1)

        result = local.process_local(args.local, args.deep_search)

    if result == None:
        sys.exit(1)  # exit with non-zero exit code

    renderer.show_result_as_text(result)
    # renderer.show_result_as_html(result)

    if args.local:
        cleaner.process_cleaner(result)
