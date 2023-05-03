import argparse
import sys

from github import github
from local import local
from renderer import renderer
from cleaner import cleaner


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
        print("No results found")
        sys.exit(1)  # exit with non-zero exit code

    renderer.show_result_as_text(result)
    # renderer.show_result_as_html(result)

    if args.local:
        generate_clean_files = input(
            "\nDo you want to generate clean files? (yes/no) ")
        while generate_clean_files.lower() not in ("yes", "no"):
            generate_clean_files = input("Please enter either 'yes' or 'no': ")
        if generate_clean_files.lower() == "yes":

            replace_files = input(
                "\nDo you want to replace the files? (yes/no) ")
            while replace_files.lower() not in ("yes", "no"):
                replace_files = input("Please enter either 'yes' or 'no': ")
            if replace_files.lower() == "yes":

                replace_files_2 = input(
                    "\nAre you sure you want to replace the files? (yes/no) ")
                while replace_files_2.lower() not in ("yes", "no"):
                    replace_files_2 = input(
                        "Please enter either 'yes' or 'no': ")
                if replace_files_2.lower() == "yes":
                    cleaner.clean_files(result, True)
                else:
                    cleaner.clean_files(result, False)
            else:
                cleaner.clean_files(result, False)
