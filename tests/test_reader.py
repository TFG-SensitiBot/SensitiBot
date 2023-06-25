import json
import os
import unittest
from io import StringIO
from unittest.mock import patch

from reader import reader


class TestReaderGitHub(unittest.TestCase):
    def test_github_read_no_deep(self):
        # Load the files to analyze
        files = json.loads(github_dirty)

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = reader.process_files(files, False, True)
            self.assertEqual(result, json.loads(github_no_deep))

    def test_github_read_with_deep(self):
        # Load the files to analyze
        files = json.loads(github_dirty)

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = reader.process_files(files, True, True)
            self.assertEqual(result, json.loads(github_with_deep))

    def test_github_all_clean(self):
        # Load the files to analyze
        files = json.loads(github_clean)

        # Redirect stdout to capture the error message
        with patch('sys.stdout', new=StringIO()) as stdout:

            # Execute the function and assert the output
            result = reader.process_files(files, True, True)
            self.assertEqual(result, None)

            # The function should print the error message
            output = stdout.getvalue().strip()
            self.assertIn(f'Your files are clean!', output)


class TestReaderLocal(unittest.TestCase):
    def test_local_read_no_deep(self):
        # Load the files to analyze
        files = json.loads(local_dirty)

        # Make the file paths absolute
        files["repositories"][0]["files"] = [
            os.path.join(os.path.dirname(__file__), file.replace("\\\\", "\\")) for file in files["repositories"][0]["files"]
        ]

        # Load the expected output
        expected_output = json.loads(local_no_deep)

        new_expected_files = []
        for file in expected_output["repositories"][0]["files"]:
            file["name"] = os.path.join(os.path.dirname(
                __file__), file["name"].replace("\\\\", "\\"))
            new_expected_files.append(file)

        expected_output["repositories"][0]["files"] = new_expected_files

        # Execute the function and assert the output
        result = reader.process_files(files, False, True)
        self.assertEqual(result, expected_output)

    def test_local_read_with_deep(self):
        # Load the files to analyze
        files = json.loads(local_dirty)

        # Make the file paths absolute
        files["repositories"][0]["files"] = [
            os.path.join(os.path.dirname(__file__), file.replace("\\\\", "\\")) for file in files["repositories"][0]["files"]
        ]

        # Load the expected output
        expected_output = json.loads(local_with_deep)

        new_expected_files = []
        for file in expected_output["repositories"][0]["files"]:
            file["name"] = os.path.join(os.path.dirname(
                __file__), file["name"].replace("\\\\", "\\"))
            new_expected_files.append(file)

        expected_output["repositories"][0]["files"] = new_expected_files

        # Execute the function and assert the output
        result = reader.process_files(files, True, True)
        self.assertEqual(result, expected_output)

    def test_local_all_clean(self):
        # Load the files to analyze
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
github_dirty = '''{
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

github_clean = '''{
    "repositories": [
        {
            "files": [
                "https://raw.githubusercontent.com/RingoML/AISS-2021-L9-G05-josmarluq/master/examples/rest-assured-itest-java/src/test/resources/greeting-schema.json",
                "https://raw.githubusercontent.com/RingoML/AISS-2021-L9-G05-josmarluq/master/examples/rest-assured-itest-java/src/test/resources/message.json",
                "https://raw.githubusercontent.com/RingoML/AISS-2021-L9-G05-josmarluq/master/examples/rest-assured-itest-java/src/test/resources/products-schema.json",
                "https://raw.githubusercontent.com/RingoML/AISS-2021-L9-G05-josmarluq/master/examples/rest-assured-itest-java/src/test/resources/store-schema-isbn-required.json",
                "https://raw.githubusercontent.com/RingoML/AISS-2021-L9-G05-josmarluq/master/examples/rest-assured-itest-java/src/test/resources/store-schema.json",
                "https://raw.githubusercontent.com/RingoML/AISS-2021-L9-G05-josmarluq/master/modules/json-schema-validator/src/test/resources/greeting-schema.json",
                "https://raw.githubusercontent.com/RingoML/AISS-2021-L9-G05-josmarluq/master/modules/spring-mock-mvc/src/test/resources/greeting-schema.json"
            ],
            "name": "AISS-2021-L9-G05-josmarluq"
        },
        {
            "files": [
                "https://raw.githubusercontent.com/RingoML/decide/master/loadtest/voters.json"
            ],
            "name": "decide"
        }
    ]
}'''

local_dirty = '''{
    "repositories": [
        {
            "files": [
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

local_clean = '''{
    "repositories": [
        {
            "files": [
                "test_files\\\\clean\\\\clean.csv"
            ],
            "name": "local"
        }
    ]
}'''

# Expected outputs
github_no_deep = '''{
    "repositories": [
        {
            "files": [
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_1.csv",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_2.csv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_3.csv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_1.xlsx",
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
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_2.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
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
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_3.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "iban",
                                "ip"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
                            ]
                        }
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_1.json",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_2.json",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_3.json",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_1.jsonl",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_2.jsonl",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_3.jsonl",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_1.tsv",
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_2.tsv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_3.tsv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                }
            ],
            "name": "test-data"
        }
    ]
}'''

github_with_deep = '''{
    "repositories": [
        {
            "files": [
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_1.csv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_2.csv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/csv/csv_file_3.csv",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_1.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "phone number": [
                                    "phone"
                                ]
                            },
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
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "email": [
                                    "email"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
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
                            "positive_columns": {
                                "email": [
                                    "email"
                                ],
                                "iban": [
                                    "iban"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
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
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_2.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "email": [
                                    "email"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "phone number": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_columns": {
                                "email": [
                                    "email"
                                ],
                                "iban": [
                                    "iban"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
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
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/excel/excel_file_3.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "email": [
                                    "email"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_columns": {
                                "email": [
                                    "email"
                                ],
                                "iban": [
                                    "iban"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "iban",
                                "ip"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "phone number": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
                            ]
                        }
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_1.json",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_2.json",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_array/json_array_file_3.json",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_1.jsonl",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_2.jsonl",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/json/json_lines/json_lines_file_3.jsonl",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_1.tsv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_2.tsv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "https://raw.githubusercontent.com/codicero/test-data/master/tsv/tsv_file_3.tsv",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                }
            ],
            "name": "test-data"
        }
    ]
}'''

local_no_deep = '''{
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
                    "name": "test_files\\\\csv\\\\csv_file_2.csv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\csv\\\\csv_file_3.csv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
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
                    "name": "test_files\\\\excel\\\\excel_file_2.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
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
                    "name": "test_files\\\\excel\\\\excel_file_3.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "iban",
                                "ip"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
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
                    "name": "test_files\\\\json\\\\json_array\\\\json_array_file_2.json",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_array\\\\json_array_file_3.json",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
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
                    "name": "test_files\\\\json\\\\json_lines\\\\json_lines_file_2.jsonl",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_lines\\\\json_lines_file_3.jsonl",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
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
                },
                {
                    "name": "test_files\\\\tsv\\\\tsv_file_2.tsv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\tsv\\\\tsv_file_3.tsv",
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                }
            ],
            "name": "local"
        }
    ]
}'''

local_with_deep = '''{
    "repositories": [
        {
            "files": [
                {
                    "name": "test_files\\\\csv\\\\csv_file_1.csv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "test_files\\\\csv\\\\csv_file_2.csv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\csv\\\\csv_file_3.csv",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "test_files\\\\excel\\\\excel_file_1.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "phone number": [
                                    "phone"
                                ]
                            },
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
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "email": [
                                    "email"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
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
                            "positive_columns": {
                                "email": [
                                    "email"
                                ],
                                "iban": [
                                    "iban"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
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
                    "name": "test_files\\\\excel\\\\excel_file_2.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "email": [
                                    "email"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "phone number": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_columns": {
                                "email": [
                                    "email"
                                ],
                                "iban": [
                                    "iban"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
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
                    "name": "test_files\\\\excel\\\\excel_file_3.xlsx",
                    "positive_sheets": [
                        {
                            "name": "Sheet1",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "email": [
                                    "email"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "dni",
                                "passwords"
                            ]
                        },
                        {
                            "name": "Sheet2",
                            "positive_columns": {
                                "email": [
                                    "email"
                                ],
                                "iban": [
                                    "iban"
                                ],
                                "phone": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "name",
                                "email",
                                "phone",
                                "iban",
                                "ip"
                            ]
                        },
                        {
                            "name": "Sheet3",
                            "positive_columns": {
                                "dni": [
                                    "dni"
                                ],
                                "phone number": [
                                    "phone"
                                ]
                            },
                            "positive_headers": [
                                "firstname",
                                "surname",
                                "phone number",
                                "dni",
                                "password"
                            ]
                        }
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_array\\\\json_array_file_1.json",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_array\\\\json_array_file_2.json",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_array\\\\json_array_file_3.json",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_lines\\\\json_lines_file_1.jsonl",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_lines\\\\json_lines_file_2.jsonl",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\json\\\\json_lines\\\\json_lines_file_3.jsonl",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                },
                {
                    "name": "test_files\\\\tsv\\\\tsv_file_1.tsv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "phone number": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "firstname",
                        "surname",
                        "phone number",
                        "dni",
                        "password"
                    ]
                },
                {
                    "name": "test_files\\\\tsv\\\\tsv_file_2.tsv",
                    "positive_columns": {
                        "dni": [
                            "dni"
                        ],
                        "email": [
                            "email"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "dni",
                        "passwords"
                    ]
                },
                {
                    "name": "test_files\\\\tsv\\\\tsv_file_3.tsv",
                    "positive_columns": {
                        "email": [
                            "email"
                        ],
                        "iban": [
                            "iban"
                        ],
                        "phone": [
                            "phone"
                        ]
                    },
                    "positive_headers": [
                        "name",
                        "email",
                        "phone",
                        "iban",
                        "ip"
                    ]
                }
            ],
            "name": "local"
        }
    ]
}'''
