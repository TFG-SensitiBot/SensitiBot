import json
import pandas as pd

def processFiles(files):
    repositories = json.loads(files)

    for repository in repositories:
        csv_files = repositories[repository]["csv_files"]
        readcsvFiles(csv_files)

    return files

def readcsvFiles(files):
    for file in files:
        data = pd.read_csv(file)
        columns = data.columns.values
        print(columns)
        