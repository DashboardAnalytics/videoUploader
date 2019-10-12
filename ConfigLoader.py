import configparser

#Funcion simple, que carga un archivo de configuración, que facilita ciertas configuraciones al usuario final.
def getINIConfiguration():

    config = configparser.ConfigParser()
    config.read('configuration.ini')

    return config

def getCSVFile():
    config = configparser.ConfigParser()
    config.read('configuration.ini')

    if('CAMERAS' in config):
        if('CameraCSV' in config['CAMERAS']):
            csvPath = config['CAMERAS']['CameraCSV']
            return {'path': csvPath, 'result': True}
        else:
            return {'path': "", 'result': False}
    else:
        return {'path': "", 'result': False}

#Funcion que obtiene la lista de camaras existentes en el archivo de configuración.
def getListOfCameras():

    config = configparser.ConfigParser()
    config.read('configuration.ini')
    if('CAMERAS' in config):
        if('CameraUrlList' in config['CAMERAS']):
            cameraList = config['CAMERAS']['CameraUrlList'].split(',')
            return cameraList
        return []
    return []
