import json
import unittest
from io import StringIO
from unittest.mock import patch

from github import github


class TestGitHubAPI(unittest.TestCase):
    def test_bad_credentials(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            with self.assertRaises(Exception) as cm:
                github.process_github("codicero", None, None, "token")

                # Check the error message
                self.assertEqual(cm.exception.message,
                                 'Error: Bad credentials')

                # The function should print the error message
                output = stdout.getvalue().strip()
                self.assertEqual(
                    output, f'Searching repositories for codicero:\nError: Bad credentials')

    def test_user_not_found(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            with self.assertRaises(Exception) as cm:
                github.process_github("this-user-does-not-exist")

                # Check the error message
                self.assertEqual(cm.exception.message,
                                 "Error: Github User or Organization Not Found")

                # The function should print the error message
                output = stdout.getvalue().strip()
                self.assertEqual(
                    output, f'Searching repositories for codicer:\nError: Github User or Organization Not Found')

    def test_repository_not_found(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            with self.assertRaises(Exception) as cm:
                github.process_github("codicero", "test-dataset")

                # Check the error message
                self.assertEqual(cm.exception.message,
                                 "Error: Repository Not Found")

                # The function should print the error message
                output = stdout.getvalue().strip()
                self.assertEqual(
                    output, f'Searching repository codicero/test-dataset:\nError: Repository Not Found')

    def test_branch_not_found(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            with self.assertRaises(Exception) as cm:
                github.process_github("codicero", "test-dataset", "branch")

                # Check the error message
                self.assertEqual(cm.exception.message,
                                 "Error: Repository Not Found")

                # The function should print the error message
                output = stdout.getvalue().strip()
                self.assertEqual(
                    output, f'Searching repository codicero/test-dataset:\nError: Repository Not Found')


class TestGitHub(unittest.TestCase):
    def test_github_user(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = github.process_github("codicero")
            self.assertEqual(result, json.loads(github_user))

            # The function should print the number of repositories found
            output = stdout.getvalue().strip()
            self.assertIn(
                "Searching repositories for codicero:\n\t2 public repositories found", output)

    def test_github_repository(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = github.process_github("codicero", "test-data")
            self.assertEqual(result, json.loads(github_user))

    def test_github_branch(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = github.process_github("codicero", "test-data", "master")
            self.assertEqual(result, json.loads(github_user))

    def test_no_dataset_files_found(self):
        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = github.process_github("codicero", "data-suite")
            self.assertEqual(result, None)

            # The function should print the error message
            output = stdout.getvalue().strip()
            self.assertEqual(
                output, f'Searching repository codicero/data-suite:\n\nNo dataset files found')


if __name__ == '__main__':
    unittest.main()


# Expected outputs
github_user = '''{
    "repositories": [
        {
            "files": [
                "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_1.csv",
                "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_2.csv",
                "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_3.csv",
                "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_1.xlsx",
                "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_2.xlsx",
                "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_3.xlsx",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_1.json",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_2.json",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_3.json",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_file_1.json",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_file_2.json",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_file_3.json",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_1.jsonl",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_2.jsonl",
                "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_3.jsonl",
                "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_1.tsv",
                "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_2.tsv",
                "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_3.tsv"
            ],
            "name": "test-data"
        }
    ]
}'''

github_repository = '''{
    "files": [
        "https://raw.githubusercontent.com/codicero/test-data/master/access/access_file_1.accdb",
        "https://raw.githubusercontent.com/codicero/test-data/master/access/access_file_2.accdb",
        "https://raw.githubusercontent.com/codicero/test-data/master/access/access_file_3.accdb",
        "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_1.csv",
        "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_2.csv",
        "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_3.csv",
        "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_1.xlsx",
        "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_2.xlsx",
        "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_3.xlsx",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_1.json",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_2.json",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_3.json",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_file_1.json",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_file_2.json",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_file_3.json",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_1.jsonl",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_2.jsonl",
        "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_3.jsonl",
        "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_1.tsv",
        "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_2.tsv",
        "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_3.tsv"
    ],
    "name": "test-data"
}'''
