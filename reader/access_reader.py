import pandas as pd
import pyodbc

from reader import columns_reader, headers_reader


def read_access_file(file, deep_search=False):
    """
    Analyzes the access file.

    Args:
        files (str): The file to analyze.
        deep_search (bool): If true, the content of the files will be analyzed.

    Returns:
        dict: The result of analyzing the access file.
    """
    try:
        # Establish a connection to the Access database
        conn_str = r"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}".format(file)
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
    except Exception as e:
        error = {"file": file, "error": str(e)}
        return None, error

    tables_to_read = []

    # Query to retrieve table names
    table_names = []
    
    for i in cursor.tables(tableType='Table'):
        table_names.append(i.table_name)

    read_all_tables = ask_read_all_tables(len(table_names))
    if read_all_tables:
        tables_to_read = table_names
    else:
        tables_to_read = ask_which_tables(table_names)

    result_file = {"name": file}

    result_tables = []
    for table_name in tables_to_read:

        # Query to retrieve all records from the table
        query = f"SELECT * FROM {table_name}"
        table_data = pd.read_sql(query, conn)

        result_table = read_table(table_name, table_data, deep_search)

        if result_table != None:
            result_tables.append(result_table)

    if len(result_tables) != 0:
        result_file["positive_tables"] = result_tables

    if len(result_file) == 1:
        return None, None

    conn.close()

    return result_file, None


def read_table(table_name, table_data, deep_search=False):
    result_table = {"name": table_name}

    headers = table_data.columns.values
    result_headers = headers_reader.analize_headers(headers)

    # Only show headers that have errors
    if len(result_headers) != 0:
        result_table["positive_headers"] = result_headers

    # Only analyze columns if deep_search is enabled
    if deep_search:
        result_columns = columns_reader.analize_columns(table_data, headers)

        # Only show columns that have errors
        if len(result_columns) != 0:
            result_table["positive_columns"] = result_columns

    if len(result_table) == 1:
        return None

    return result_table


def ask_read_all_tables(number_of_tables):
    ask_read_all_tables = input(
        f"\n\t\tDo you want to read all ({number_of_tables}) tables? (yes/no): ")
    while ask_read_all_tables.lower() not in ("yes", "no"):
        ask_read_all_tables = input(
            "\t\tPlease enter either 'yes' or 'no': ")
    return ask_read_all_tables.lower() == "yes"


def ask_which_tables(table_names):
    tables_to_read = []

    print("\t\tSelect which tables to read:")

    for table_name in table_names:
        ask_table = input(
            f"\t\tRead table {table_name}? (yes/no): ")

        while ask_table.lower() not in ("yes", "no"):
            ask_table = input(
                "\t\tPlease enter either 'yes' or 'no': ")

        if ask_table.lower() == "yes":
            tables_to_read.append(table_name)

    return tables_to_read
