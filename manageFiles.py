import os
import pandas as pd
import datetime

def checkFileInFolder(filename):

    if(os.path.exists(filename)):
        return True
    else:
        return False


def eraseFileInFolder(file):

    if(checkFileInFolder(file)):
        os.remove(file)
        return True
    else:
        return False

def checkCameraCSVFile(filepath):
    if(os.path.exists(filepath)):
        return True
    else:
        return False

def readCameraCSV(csv_path):
    if(checkCameraCSVFile(csv_path)):
        data = pd.read_csv(csv_path, sep=';')
        return data
    else:
        return []
