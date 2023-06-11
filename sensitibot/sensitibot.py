import sys

from cleaner import cleaner
from github import github
from local import local
from renderer import renderer
from sensitibot import parser


def main():

    args = parser.parse_args(None)

    result = ""
    name = ""

    if args.command == 'github':
        name = args.user
        try:
            result = github.process_github(
                args.user, args.repository, args.branch, args.token, args.deep_search, args.wide_search)
        except github.GitHubAPIException as exception:
            print(f'{exception}\n')
            sys.exit(1)  # exit with non-zero exit code

    if args.command == 'local':
        name = "local"
        result = local.process_local(
            args.path, args.deep_search, args.wide_search)

    if result == None:
        print("")
        sys.exit(1)  # exit with non-zero exit code

    renderer.show_result_as_text(result, name, args.deep_search)

    if args.command == 'local':
        cleaner.process_cleaner(result)

    print("")
