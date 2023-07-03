import json
import os
import shutil
import unittest
from io import StringIO
from unittest.mock import patch

from cleaner import cleaner
from reader import reader


class TestCleanerNoRewrite(unittest.TestCase):
    """
    Test cases the cleaner (without rewrite).
    """

    @patch('builtins.input', side_effect=['yes', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no'])
    def test_clean_no_rewrite(self, mock_input):
        """
        Cleans the files without rewriting them.
        Then checks if the files were created and if they are clean.
        """
        # Load the files to analyze
        files = json.loads(local_original)

        # Make the file paths absolute
        new_expected_files = []
        for file in files["repositories"][0]["files"]:
            file["name"] = os.path.join(os.path.dirname(
                __file__), file["name"].replace("\\\\", "\\"))
            new_expected_files.append(file)
        files["repositories"][0]["files"] = new_expected_files

        # These are the files that should be created
        expected_files = [
            os.path.join(os.path.dirname(__file__),
                         'test_files\\csv\\csv_file_1_clean.csv'),
            os.path.join(os.path.dirname(__file__),
                         'test_files\\excel\\excel_file_1_clean.xlsx'),
            os.path.join(os.path.dirname(__file__),
                         'test_files\\tsv\\tsv_file_1_clean.tsv'),
            os.path.join(os.path.dirname(
                __file__), 'test_files\\json\\json_array\\json_array_file_1_clean.json'),
            os.path.join(os.path.dirname(
                __file__), 'test_files\\json\\json_lines\\json_lines_file_1_clean.jsonl')
        ]

        # Execute the function and assert the output
        cleaner.process_cleaner(files)
        for file in expected_files:
            self.assertTrue(os.path.isfile(file))

        # Load the created files to analyze
        files = json.loads(local_clean)

        # Make the file paths absolute
        files["repositories"][0]["files"] = [
            os.path.join(os.path.dirname(__file__), file.replace("\\\\", "\\")) for file in files["repositories"][0]["files"]
        ]

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = reader.process_files(files, True, True)
            self.assertEqual(result, None)

            # The function should print the error message
            output = stdout.getvalue().strip()
            self.assertIn(f'Your files are clean!', output)


class TestCleanerWithRewrite(unittest.TestCase):
    """
    Test cases the cleaner (with rewrite).
    """

    @patch('builtins.input', side_effect=['yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes'])
    def test_clean_with_rewrite(self, mock_input):
        """
        Copys the files to a new folder and cleans them.
        Then checks if the files were created and if they are clean.
        """
        # Load the files to analyze
        files = json.loads(local_copied)

        # Make the file paths absolute
        new_expected_files = []
        for file in files["repositories"][0]["files"]:
            file["name"] = os.path.join(os.path.dirname(
                __file__), file["name"].replace("\\\\", "\\"))
            new_expected_files.append(file)
        files["repositories"][0]["files"] = new_expected_files

        # These are the files that should be created
        expected_files = [
            os.path.join(os.path.dirname(__file__),
                         'cleaned_files\\csv\\csv_file_1.csv'),
            os.path.join(os.path.dirname(__file__),
                         'cleaned_files\\excel\\excel_file_1.xlsx'),
            os.path.join(os.path.dirname(__file__),
                         'cleaned_files\\tsv\\tsv_file_1.tsv'),
            os.path.join(os.path.dirname(
                __file__), 'cleaned_files\\json\\json_array\\json_array_file_1.json'),
            os.path.join(os.path.dirname(
                __file__), 'cleaned_files\\json\\json_lines\\json_lines_file_1.jsonl')
        ]

        # Copy the files to clean so they can be rewritten
        os.makedirs(os.path.join(os.path.dirname(__file__),
                    "cleaned_files\\csv"), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__),
                    "cleaned_files\\excel"), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__),
                    "cleaned_files\\json\\json_array"), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__),
                    "cleaned_files\\json\\json_lines"), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__),
                    "cleaned_files\\tsv"), exist_ok=True)
        for file in expected_files:
            shutil.copy2(file.replace("cleaned_files", "test_files"), file)

        # Execute the function and assert the output
        cleaner.process_cleaner(files)
        for file in expected_files:
            self.assertTrue(os.path.isfile(file))

        # Load the created files to analyze
        files = json.loads(local_clean)

        # Make the file paths absolute
        files["repositories"][0]["files"] = [
            os.path.join(os.path.dirname(__file__), file.replace("\\\\", "\\")) for file in files["repositories"][0]["files"]
        ]

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = reader.process_files(files, True, True)
            self.assertEqual(result, None)

            # The function should print the error message
            output = stdout.getvalue().strip()
            self.assertIn(f'Your files are clean!', output)


if __name__ == '__main__':
    unittest.main()


# Inputs
local_clean = '''{
    "repositories": [
        {
            "files": [
                "test_files\\\\csv\\\\csv_file_1_clean.csv",
                "test_files\\\\excel\\\\excel_file_1_clean.xlsx",
                "test_files\\\\json\\\\json_file_1_clean.json",
                "test_files\\\\json\\\\json_array\\\\json_array_file_1_clean.json",
                "test_files\\\\json\\\\json_lines\\\\json_lines_file_1_clean.jsonl",
                "test_files\\\\tsv\\\\tsv_file_1_clean.tsv"
            ],
            "name": "local"
        }
    ]
}'''

local_original = '''{
    "repositories": [
        {
            "files": [
                {
                    "name": "test_files\\\\csv\\\\csv_file_1.csv",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "test_files\\\\excel\\\\excel_file_1.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "iban",
                                "ip"
                            ]
                        }
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_array\\\\json_array_file_1.json",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_lines\\\\json_lines_file_1.jsonl",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "test_files\\\\tsv\\\\tsv_file_1.tsv",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                }
            ],
            "name": "local"
        }
    ]
}'''

local_copied = '''{
    "repositories": [
        {
            "files": [
                {
                    "name": "cleaned_files\\\\csv\\\\csv_file_1.csv",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "cleaned_files\\\\excel\\\\excel_file_1.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "iban",
                                "ip"
                            ]
                        }
                    ]
                },
                {
                    "name": "cleaned_files\\\\json\\\\json_array\\\\json_array_file_1.json",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "cleaned_files\\\\json\\\\json_lines\\\\json_lines_file_1.jsonl",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "cleaned_files\\\\tsv\\\\tsv_file_1.tsv",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                }
            ],
            "name": "local"
        }
    ]
}'''
