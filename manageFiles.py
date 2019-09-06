import os
import ConfigLoader as cfgLoader

def checkFileInFolder(filename, folder):

    if(os.path.exists(folder)):
        if(os.path.exists(folder + '/' + filename)):
            return True
        else:
            return False
    else:
        return False

def eraseFileInFolder(filename):

    today = datetime.now()
    dt_string = today.strftime("%d-%m-%Y")
    directory = './' + cfgLoader.getINIConfiguration()['VIDEO']['Directory'] + '/' + dt_string

    if(checkFileInFolder(filename, directory)):
        os.remove(directoty + '/' + filename)
        return True
    else:
        return False
