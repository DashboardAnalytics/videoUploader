import configparser

#Funcion simple, que carga un archivo de configuración, que facilita ciertas configuraciones al usuario final.
def getINIConfiguration():

    config = configparser.ConfigParser()
    config.read('configuration.ini')

    return config

#Funcion que obtiene la lista de camaras existentes en el archivo de configuración.
def getListOfCameras():

    config = configparser.ConfigParser()
    config.read('configuration.ini')

    cameraList = config['CAMERAS']['CameraUrlList'].split(',')

    return cameraList
