import json
import os
import unittest
from io import StringIO
from unittest.mock import patch

from local import local
from sensitibot.parser import parse_args


class TestLocal(unittest.TestCase):
    def test_no_dataset_files_found(self):
        # Construct the absolute file path of the test files directory
        test_files_dir = os.path.join(os.path.dirname(__file__), "test_filess")

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function
            result = local.process_local(test_files_dir)

            # The result should be None
            self.assertEqual(result, None)

            # The function should print the error message
            output = stdout.getvalue().strip()
            self.assertEqual(
                output, f'Searching directory {test_files_dir}:\n\nNo dataset files found')

    def test_dataset_files_found_with_path(self):
        # Construct the absolute file path of the test files directory
        test_files_dir = os.path.join(os.path.dirname(__file__), "test_files")

        # Get the expected file paths
        file_paths = json.loads(expected_output)["repositories"][0]["files"]

        # Make the expected file paths absolute
        expected_file_paths = [os.path.join(os.path.dirname(__file__), file)
                               for file in file_paths]

        # Execute the function and get the output
        result = local.process_local(test_files_dir)
        result_file_paths = result["repositories"][0]["files"]

        # The result matches the expected output
        self.assertEqual(result_file_paths, expected_file_paths)

    def test_dataset_files_found_no_path(self):
        # Get the expected file paths
        file_paths = json.loads(expected_output)["repositories"][0]["files"]

        # Make the expected file paths absolute
        expected_file_paths = [os.path.join(os.path.dirname(__file__), file)
                               for file in file_paths]

        # Execute the function and get the output
        result = local.process_local()
        result_file_paths = result["repositories"][0]["files"]

        # The result doesn't match beacuse the path is different
        self.assertNotEquals(result_file_paths, expected_file_paths)


if __name__ == '__main__':
    unittest.main()

# Expected outputs
expected_output = '''{
    "repositories": [
        {
            "files": [
                "test_files\\\\access\\\\access_file_1.accdb",
                "test_files\\\\access\\\\access_file_2.accdb",
                "test_files\\\\access\\\\access_file_3.accdb",
                "test_files\\\\clean\\\\clean.csv",
                "test_files\\\\csv\\\\csv_file_1.csv",
                "test_files\\\\csv\\\\csv_file_2.csv",
                "test_files\\\\csv\\\\csv_file_3.csv",
                "test_files\\\\excel\\\\excel_file_1.xlsx",
                "test_files\\\\excel\\\\excel_file_2.xlsx",
                "test_files\\\\excel\\\\excel_file_3.xlsx",
                "test_files\\\\json\\\\json_file_1.json",
                "test_files\\\\json\\\\json_file_2.json",
                "test_files\\\\json\\\\json_file_3.json",
                "test_files\\\\json\\\\json_array\\\\json_array_file_1.json",
                "test_files\\\\json\\\\json_array\\\\json_array_file_2.json",
                "test_files\\\\json\\\\json_array\\\\json_array_file_3.json",
                "test_files\\\\json\\\\json_lines\\\\json_lines_file_1.jsonl",
                "test_files\\\\json\\\\json_lines\\\\json_lines_file_2.jsonl",
                "test_files\\\\json\\\\json_lines\\\\json_lines_file_3.jsonl",
                "test_files\\\\tsv\\\\tsv_file_1.tsv",
                "test_files\\\\tsv\\\\tsv_file_2.tsv",
                "test_files\\\\tsv\\\\tsv_file_3.tsv"
            ],
            "name": "local"
        }
    ]
}'''
