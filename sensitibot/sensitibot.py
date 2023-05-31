import argparse
import sys
from importlib.metadata import version

import pkg_resources

from sensitibot import help_formatter
from cleaner import cleaner
from github import github
from local import local
from renderer import renderer


def main():
    parser = argparse.ArgumentParser(
        prog='SensitiBot',
        description='SensitiBot is a tool to analyze datasets for sensitive information.',
        formatter_class=help_formatter.CustomHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + version('SensitiBot'))

    # sensitibot github
    github_parser = subparsers.add_parser(
        'github', formatter_class=help_formatter.CustomHelpFormatter, help='Analyze GitHub repositories')
    github_parser.add_argument('user', type=str, metavar='USER',
                               help='The GitHub user or organization to analyze')
    github_parser.add_argument('-r', '--repository', metavar='REPO',
                               help='Analyze a specific repository')
    github_parser.add_argument('-b', '--branch', metavar='BRANCH',
                               help='Analyze a specific branch (only if repository is specified)')
    github_parser.add_argument('-t', '--token', metavar='TOKEN',
                               help='The GitHub token to use for authentication')
    github_parser.add_argument('--deep-search', action='store_true',
                               help='Analyze content of files')
    github_parser.add_argument('--wide-search', action='store_true',
                               help='Analyze all tables or sheets in Office files')

    # sensitibot local
    local_parser = subparsers.add_parser(
        'local', formatter_class=help_formatter.CustomHelpFormatter, help='Analyze local repository')
    local_parser.add_argument('path', type=str, metavar='PATH',
                              const='./', nargs='?', help='The path to analyze')
    local_parser.add_argument('--deep-search', action='store_true',
                              help='Analyze content of files')
    local_parser.add_argument('--wide-search', action='store_true',
                              help='Analyze all tables or sheets in Office files')

    args = parser.parse_args()

    result = ""
    name = ""

    if args.command == 'github':
        name = args.user
        result = github.process_github(
            args.user, args.repository, args.branch, args.token, args.deep_search, args.wide_search)

    if args.command == 'local':
        name = "local"
        result = local.process_local(
            args.path, args.deep_search, args.wide_search)

    if result == None:
        sys.exit(1)  # exit with non-zero exit code

    renderer.show_result_as_text(result, name, args.deep_search)
    # renderer.show_result_as_html(result)

    if args.command == 'local':
        cleaner.process_cleaner(result)

    print("")
