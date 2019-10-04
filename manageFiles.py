import os
import pandas as pd
import datetime

def checkFileInFolder(filename, folder):

    if(os.path.exists(folder)):
        if(os.path.exists(folder + '/' + filename)):
            return True
        else:
            return False
    else:
        return False


def eraseFileInFolder(filename):

    today = datetime.datetime.now()
    dt_string = today.strftime("%d-%m-%Y")
    directory = './' + cfgLoader.getINIConfiguration()['VIDEO']['Directory'] + '/' + dt_string

    if(checkFileInFolder(filename, directory)):
        os.remove(directory + '/' + filename)
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
