import unittest
from importlib.metadata import version
from io import StringIO
from unittest.mock import patch

from sensitibot.parser import parse_args


class TestParser(unittest.TestCase):
    def test_no_subcommand(self):
        # Prepare test input
        args = []

        # Redirect stdout to capture the printed help message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit):
                parse_args(args)

            # Check the printed help message
            help_output = stdout.getvalue().strip()
            expected_output = no_subcommand_help_dialog

            self.assertEqual(help_output, expected_output)

    def test_no_subcommand_help_argument(self):
        # Prepare test input
        args = ['--help']

        # Redirect stdout to capture the printed help message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit):
                parse_args(args)

            # Check the printed help message
            help_output = stdout.getvalue().strip()
            expected_output = no_subcommand_help_dialog

            self.assertEqual(help_output, expected_output)

    def test_no_subcommand_version_argument(self):
        # Prepare test input
        args = ['-v']

        # Redirect stdout to capture the printed version message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit):
                parse_args(args)

                print(stdout.getvalue())

            # Check the printed version message
            version_output = stdout.getvalue().strip()
            expected_output = f"sensitibot {version('SensitiBot')}"
            self.assertEqual(version_output, expected_output)

    def test_wrong_sucommand(self):
        # Prepare test input
        args = ['subcommand']

        # Redirect stderr to capture the error message
        with patch('sys.stderr', new=StringIO()) as stderr:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit) as cm:
                parse_args(args)

            # Check the error message
            error_output = stderr.getvalue().strip()
            expected_output = wrong_subcommand_dialog
            self.assertEqual(error_output, expected_output)

            # Check the exit code
            self.assertEqual(cm.exception.code, 2)

    def test_wrong_argument(self):
        # Prepare test input
        args = ['--argument']

        # Redirect stderr to capture the error message
        with patch('sys.stderr', new=StringIO()) as stderr:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit) as cm:
                parse_args(args)

            # Check the error message
            error_output = stderr.getvalue().strip()
            expected_output = wrong_argument_dialog
            self.assertEqual(error_output, expected_output)

            # Check the exit code
            self.assertEqual(cm.exception.code, 2)


class TestGitHubParser(unittest.TestCase):
    def test_github_subcommand_help_argument(self):
        # Prepare test input
        args = ['github', '--help']

        # Redirect stdout to capture the printed help message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit):
                parse_args(args)

            # Check the printed help message
            help_output = stdout.getvalue().strip()
            expected_output = github_subcommand_help_dialog

            self.assertEqual(help_output, expected_output)

    def test_github_subcommand_with_user(self):
        # Prepare test input
        args = ['github', 'username']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'github')
            self.assertEqual(result.user, 'username')
            self.assertIsNone(result.repository)
            self.assertIsNone(result.branch)
            self.assertIsNone(result.token)
            self.assertFalse(result.deep_search)
            self.assertFalse(result.wide_search)

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case

    def test_github_subcommand_with_no_user(self):
        # Prepare test input
        args = ['github']

        # Redirect stderr to capture the error message
        with patch('sys.stderr', new=StringIO()) as stderr:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit) as cm:
                parse_args(args)

            # Check the error message
            error_output = stderr.getvalue().strip()
            expected_output = github_subcommand_no_user
            self.assertEqual(error_output, expected_output)

            # Check the exit code
            self.assertEqual(cm.exception.code, 2)

    def test_github_subcommand_with_repository(self):
        # Prepare test input
        args = ['github', 'username', '-r', 'repository']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'github')
            self.assertEqual(result.user, 'username')
            self.assertEqual(result.repository, 'repository')
            self.assertIsNone(result.branch)
            self.assertIsNone(result.token)
            self.assertFalse(result.deep_search)
            self.assertFalse(result.wide_search)

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case

    def test_github_subcommand_with_no_repository(self):
        # Prepare test input
        args = ['github', 'username', '-r']

        # Redirect stderr to capture the error message
        with patch('sys.stderr', new=StringIO()) as stderr:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit) as cm:
                parse_args(args)

            # Check the error message
            error_output = stderr.getvalue().strip()
            expected_output = github_subcommand_no_repository
            self.assertEqual(error_output, expected_output)

            # Check the exit code
            self.assertEqual(cm.exception.code, 2)

    def test_github_subcommand_with_branch(self):
        # Prepare test input
        args = ['github', 'username', '-r', 'repository', '-b', 'branch']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'github')
            self.assertEqual(result.user, 'username')
            self.assertEqual(result.repository, 'repository')
            self.assertEqual(result.branch, 'branch')
            self.assertIsNone(result.token)
            self.assertFalse(result.deep_search)
            self.assertFalse(result.wide_search)

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case

    def test_github_subcommand_with_no_branch(self):
        # Prepare test input
        args = ['github', 'username', '-r', 'repository', '-b']

        # Redirect stderr to capture the error message
        with patch('sys.stderr', new=StringIO()) as stderr:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit) as cm:
                parse_args(args)

            # Check the error message
            error_output = stderr.getvalue().strip()
            expected_output = github_subcommand_no_branch
            self.assertEqual(error_output, expected_output)

            # Check the exit code
            self.assertEqual(cm.exception.code, 2)

    def test_github_subcommand_with_token(self):
        # Prepare test input
        args = ['github', 'username', '-t', 'token']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'github')
            self.assertEqual(result.user, 'username')
            self.assertIsNone(result.repository)
            self.assertIsNone(result.branch)
            self.assertEqual(result.token, 'token')
            self.assertFalse(result.deep_search)
            self.assertFalse(result.wide_search)

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case

    def test_github_subcommand_with_no_token(self):
        # Prepare test input
        args = ['github', 'username', '-t']

        # Redirect stderr to capture the error message
        with patch('sys.stderr', new=StringIO()) as stderr:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit) as cm:
                parse_args(args)

            # Check the error message
            error_output = stderr.getvalue().strip()
            expected_output = github_subcommand_no_token
            self.assertEqual(error_output, expected_output)

            # Check the exit code
            self.assertEqual(cm.exception.code, 2)

    def test_github_subcommand_with_deep(self):
        # Prepare test input
        args = ['github', 'username', '--deep-search']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'github')
            self.assertEqual(result.user, 'username')
            self.assertIsNone(result.repository)
            self.assertIsNone(result.branch)
            self.assertIsNone(result.token)
            self.assertTrue(result.deep_search)
            self.assertFalse(result.wide_search)

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case

    def test_github_subcommand_with_wide(self):
        # Prepare test input
        args = ['github', 'username', '--wide-search']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'github')
            self.assertEqual(result.user, 'username')
            self.assertIsNone(result.repository)
            self.assertIsNone(result.branch)
            self.assertIsNone(result.token)
            self.assertFalse(result.deep_search)
            self.assertTrue(result.wide_search)

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case


class TestLocalParser(unittest.TestCase):
    def test_local_subcommand_help_argument(self):
        # Prepare test input
        args = ['local', '--help']

        # Redirect stdout to capture the printed help message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit):
                parse_args(args)

            # Check the printed help message
            help_output = stdout.getvalue().strip()
            expected_output = local_subcommand_help_dialog

            self.assertEqual(help_output, expected_output)

    def test_local_subcommand_with_path(self):
        # Prepare test input
        args = ['local', 'path']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'local')
            self.assertEqual(result.path, 'path')

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case

    def test_local_subcommand_with_no_path(self):
        # Prepare test input
        args = ['local']

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:
            # Execute the function
            result = parse_args(args)

            # Check the parsed result
            self.assertEqual(result.command, 'local')
            self.assertIsNone(result.path)

            # Check the printed output
            output = stdout.getvalue().strip()
            self.assertEqual(output, '')  # No output expected for this case

    def test_wrong_argument(self):
        # Prepare test input
        args = ['local', '--argument']

        # Redirect stderr to capture the error message
        with patch('sys.stderr', new=StringIO()) as stderr:
            # Execute the function and assert the output
            with self.assertRaises(SystemExit) as cm:
                parse_args(args)

            # Check the error message
            error_output = stderr.getvalue().strip()
            expected_output = wrong_argument_dialog
            self.assertEqual(error_output, expected_output)

            # Check the exit code
            self.assertEqual(cm.exception.code, 2)


if __name__ == '__main__':
    unittest.main()

# Expected output for the help dialog of the main parser
no_subcommand_help_dialog = """usage: sensitibot [-h] [-v] {github,local} ...

SensitiBot is a tool to analyze datasets for sensitive information.

positional arguments:
  {github,local}
    github        analyze GitHub repositories
    local         analyze local repository

optional arguments:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit"""

wrong_subcommand_dialog = """usage: sensitibot [-h] [-v] {github,local} ...

sensitibot: error: argument command: invalid choice: 'subcommand' (choose from 'github', 'local')"""

wrong_argument_dialog = """usage: sensitibot [-h] [-v] {github,local} ...

sensitibot: error: unrecognized arguments: --argument"""


# Expected output for the help dialog of the GitHub subparser
github_subcommand_help_dialog = """usage: sensitibot github [-h] [-r REPO] [-b BRANCH] [-t TOKEN] [--deep-search] [--wide-search] USER

positional arguments:
  USER                      the GitHub user or organization to analyze

optional arguments:
  -h, --help                show this help message and exit
  -r, --repository  REPO    analyze a specific repository
  -b, --branch      BRANCH  analyze a specific branch (only if repository is specified)
  -t, --token       TOKEN   the GitHub token to use for authentication
  --deep-search             analyze content of files
  --wide-search             analyze all tables or sheets in Office files"""

github_subcommand_no_user = """usage: sensitibot github [-h] [-r REPO] [-b BRANCH] [-t TOKEN] [--deep-search] [--wide-search] USER

sensitibot github: error: the following arguments are required: USER"""

github_subcommand_no_repository = """usage: sensitibot github [-h] [-r REPO] [-b BRANCH] [-t TOKEN] [--deep-search] [--wide-search] USER

sensitibot github: error: argument -r/--repository: expected one argument"""

github_subcommand_no_branch = """usage: sensitibot github [-h] [-r REPO] [-b BRANCH] [-t TOKEN] [--deep-search] [--wide-search] USER

sensitibot github: error: argument -b/--branch: expected one argument"""

github_subcommand_no_token = """usage: sensitibot github [-h] [-r REPO] [-b BRANCH] [-t TOKEN] [--deep-search] [--wide-search] USER

sensitibot github: error: argument -t/--token: expected one argument"""


# Expected output for the help dialog of the local subparser
local_subcommand_help_dialog = """usage: sensitibot local [-h] [--deep-search] [--wide-search] [PATH]

positional arguments:
  PATH           The path to analyze

optional arguments:
  -h, --help     show this help message and exit
  --deep-search  analyze content of files
  --wide-search  analyze all tables or sheets in Office files"""
