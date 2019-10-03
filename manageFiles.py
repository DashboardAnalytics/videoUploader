import os
import ConfigLoader as cfgLoader
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

def checkCameraCSVFile():
    if(os.path.exists(cfgLoader.getINIConfiguration()['CAMERAS']['CameraCSV'])):
        return True
    else:
        return False

def readCameraCSV():
    if(checkCameraCSVFile()):
        data = pd.read_csv(cfgLoader.getINIConfiguration()['CAMERAS']['CameraCSV'], sep=';')
        return data
    else:
        return []
