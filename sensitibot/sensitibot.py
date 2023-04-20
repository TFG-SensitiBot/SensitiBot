import argparse
import sys

from github import github
from local import local
from renderer import renderer


def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument("owner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--local', metavar="PATH", const='./', nargs='?',
                       help='use a local repository (default: current directory)')
    group.add_argument('-g', '--github', metavar='USER',
                       help='use a GitHub repository')
    parser.add_argument('-r', '--repository', metavar='REPO',
                        help='the repository to use (only if --github is used)')
    parser.add_argument('-b', '--branch', metavar='BRANCH',
                        help='the branch to use (only if --repository is used)')
    parser.add_argument('-t', '--token', metavar='TOKEN',
                        help='the token to use (only if --github is used)')
    parser.add_argument('--deep-search', action='store_true',
                        help='Analyze content of files')

    args = parser.parse_args()

    result = ""

    if args.github:
        result = github.process_github(
            args.github, args.repository, args.branch, args.token, args.deep_search)

    elif args.local:
        result = local.process_local(args.local, args.deep_search)

    if result == None:
        print("No results found")
        sys.exit(1)  # exit with non-zero exit code

    renderer.show_result_as_text(result)

    # html = renderer.render_html_from_template(result)
    # renderer.show_result_as_html(html)
