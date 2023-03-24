import os
import json
from reader import reader

def processLocal(directory=None):
    files = getFilesRecursively(directory)
    
    result = reader.processFiles(files)

    return result



def getFilesRecursively(directory):
    if directory == None:
        directory = "./"

    result = {}

    # Types of files to be considered
    csv_files = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            
            if filename.endswith('.csv'):
                filepath = os.path.join(root, filename)
                csv_files.append(filepath)

    result["local"] = {"csv_files": csv_files}

    return json.dumps(result, indent=4)
