import datetime
import numpy as np
import os, glob, time
import ConfigLoader as cfgLoader
import cv2
import APIConsumer as api
import CloudStorageFunctions as cloudStorage

configFile = cfgLoader.getINIConfiguration()
# Funcion que obtiene una grabacion desde una url, y
# escribe el archivo de salida en formato .avi
# Entradas: Int con numero de video actual, string con fecha actual e int con cantidad de frames por segundo
# Salidas: Boolean indicando si el proceso se llevo a cabo correctamente
def videoRecorder(nVideo, today, url):
    #Se crean las variables necesarias para procesar cada video.
    nFrames = int(configFile['VIDEO']['VideoFrameRate'])
    maxLength = int(configFile['VIDEO']['MaxVideoLength'])
    localShop = configFile['SHOPPING']['Shop']
    shopping = configFile['SHOPPING']['ShoppingCenter']
    # Se obtiene nuevamente la fecha, solo que ademas con la hora actual
    now = datetime.datetime.now()
    videoDate = now.strftime("%d-%m-%Y")
    startTime = now.strftime("%H-%M-%S")
    endTime = (now + datetime.timedelta(0, maxLength)).strftime("%H-%M-%S")
    # Se genera el nombre del archivo de salida
    recordDirectory = './' + configFile['VIDEO']['Directory'] + '/'+today+"/"
    filename = str(nVideo) + '_' + shopping + '_' + localShop + '_' + videoDate + '_' + startTime + '_' + endTime + '.avi'
    saveDirectory = recordDirectory + filename
    # Se comienza a capturar el streaming del video
    cap = cv2.VideoCapture(url)
    if not cap:
        print("!!! Failed VideoCapture: invalid parameter!")
        return False
    cap.set(cv2.CAP_PROP_FPS, nFrames)
    # Se define el codec y se crea el objeto de tipo VideoWriter
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # Se comunica a la API que se grabará un video.
    api.createVideoData({'videoName': filename, 'status': 1, 'videoNumber': nVideo, 'store': localShop, 'ShoppingCenter': shopping})
    # Se empieza a grabar el video.
    out = cv2.VideoWriter(saveDirectory,cv2.VideoWriter_fourcc('M','J','P','G'), nFrames, (frame_width,frame_height))

    aux2 = 0
    aux = 0
    while aux < (maxLength*nFrames):
        # Se lee frame a frame
        ret, frame = cap.read()
        # Si se produce un error al leer el frame, se detiene el proceso
        if type(frame) == type(None):
            print("!!! Couldn't read frame!")
            return False
        # Se escribe el frame en el archivo de salida
        if(aux2 % nFrames == 0):
            out.write(frame)
            aux += 1
        aux2 += 1
    # Se liberan los recursos de captura y de escritura
    cap.release()
    out.release()
    #Se crea video en la DB.
    api.createVideoData(filename, nVideo, localShop, shopping)
    #Se inicia subida de video.
    cloudStorage.upload_blob('my-new-videos-prueba2211-bucket-test', saveDirectory, filename)
    return True


def startRecording(url):
    # Se obtiene fecha actual para generar la carpeta correspondiente
    today = datetime.datetime.now()
    dt_string = today.strftime("%d-%m-%Y")
    # Se setean los parametros iniciales
    nVideo = 1
    n = int(input("Cantidad de partes: "))
    # Si la carpeta no existe, se crea
    if(not os.path.isdir('./' + configFile['VIDEO']['Directory'])):
        os.mkdir('./' + configFile['VIDEO']['Directory'])
        if(not os.path.isdir('./' + configFile['VIDEO']['Directory'] + '/' +dt_string)):
            os.mkdir('./' + configFile['VIDEO']['Directory'] + '/' +dt_string)
    # Si ya existe, es probable que ya existan videos, por lo que
    # se obtiene el nombre del ultimo video creado para continuar con
    # la serie
    else:
        directory = './' + configFile['VIDEO']['Directory'] + '/' +dt_string + "/*"
        listOfFiles = glob.glob(directory)
        # Se comprueba que existan archivos adentro de la carpeta
        if(len(listOfFiles) != 0):
            latestFile = max(listOfFiles, key=os.path.getctime)
            # Se busca el caracter n, donde en la posicion siguiente
            # se tiene el numero del video
            nVideo = int(latestFile.split('\\')[-1].split('_')[0])+1
            # Se modifica n para que corresponda con la cantidad
            # de partes que se desea grabar
            n = n + nVideo - 1
    # Mientras no existan problemas al grabar y queden partes por grabar,
    # se llama a la funcion videoRecorder
    r = True
    while ((nVideo<=n) and (r)):
        print ("Recording video Nº "+str(nVideo)+"...")
        r = videoRecorder(nVideo, dt_string, url)
        nVideo += 1


def main():
    cameraUrls = cfgLoader.getListOfCameras()
    print(cameraUrls)
    for url in cameraUrls:
        startRecording(url)
main()
