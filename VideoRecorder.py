import datetime
import numpy as np
import os, glob, time
import cv2
import threading
import scheduler as sched
import APIConsumer as api
import CloudStorageFunctions as cloudStorage
import manageFiles as fileManager
import ConfigLoader as cfgLoader
configFile = cfgLoader.getINIConfiguration()

def videoUploader(saveDirectory, videoData, videoResponse):
    try:
        cloudStorage.upload_blob('my-new-videos-prueba2211-bucket-test', saveDirectory, videoData['filename'])
    except:
        print("Error de conexion al subir el video,",videoData['videoNumber'])
        print("Contacte con el admin F")
    else:
        print("actualizando data.")
        api.updateVideoStatusReady(videoResponse['id'], videoData['filename'], videoData['videoNumber'], videoData['store'], videoData['shoppingCenter'])
        print("Borrando video...")
        fileManager.eraseFileInFolder(videoData['filename'], configFile['VIDEO']['Directory'])
# Funcion que obtiene una grabacion desde una url, y
# escribe el archivo de salida en formato .avi
# Entradas: Int con numero de video actual, string con fecha actual e int con cantidad de frames por segundo
# Salidas: Boolean indicando si el proceso se llevo a cabo correctamente
def videoRecorder(nVideo, today, store, shoppingCenter, cameraID, cameraIP):
    #Se crean las variables necesarias para procesar cada video.
    nFrames = int(configFile['VIDEO']['VideoFrameRate'])
    maxLength = int(configFile['VIDEO']['MaxVideoLength'])
    # Se obtiene nuevamente la fecha, solo que ademas con la hora actual
    now = datetime.datetime.now()
    videoDate = now.strftime("%d-%m-%Y")
    startTime = now.strftime("%H-%M-%S")
    endTime = (now + datetime.timedelta(0, maxLength)).strftime("%H-%M-%S")
    # Se genera el nombre del archivo de salida
    recordDirectory = './' + configFile['VIDEO']['Directory'] + '/'+today+"/"
    filename = str(nVideo) + '_' + cameraID +'_' + shoppingCenter + '_' + store + '_' + videoDate + '_' + startTime + '_' + endTime + '.avi'
    saveDirectory = recordDirectory + filename
    # Se comienza a capturar el streaming del video
    cap = cv2.VideoCapture(cameraIP)
    if not cap:
        print("!!! Failed VideoCapture: invalid parameter!")
        return False
    cap.set(cv2.CAP_PROP_FPS, nFrames)
    # Se define el codec y se crea el objeto de tipo VideoWriter
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
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
    dataVideo = {"filename": filename, "videoNumber" : nVideo, "store": store, "shoppingCenter": shoppingCenter}
    videoResponse = api.createVideoData(filename, nVideo, store, shoppingCenter)
    #Se inicia subida de video.
    t = threading.Thread(target = videoUploader, args = (saveDirectory, dataVideo, videoResponse))
    t.start()
    return True


def startRecording(store, shoppingCenter, cameraID, cameraIP):
    # Se obtiene fecha actual para generar la carpeta correspondiente
    today = datetime.datetime.now()
    dt_string = today.strftime("%d-%m-%Y")
    # Se setean los parametros iniciales
    nVideo = 1
    # Si la carpeta no existe, se crea
    if(not os.path.isdir('./' + configFile['VIDEO']['Directory'])):
        os.mkdir('./' + configFile['VIDEO']['Directory'])
        os.mkdir('./' + configFile['VIDEO']['Directory'] + '/' +dt_string)
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
    # Mientras no existan problemas al grabar y queden partes por grabar,
    # se llama a la funcion videoRecorder
    r = True
    runningStatus = sched.getRunningStatus()
    while ( (runningStatus) and (r) ):
        r = videoRecorder(nVideo, dt_string, store, shoppingCenter, cameraID, cameraIP)
        runningStatus = sched.getRunningStatus()
        nVideo += 1

def recordCameras():
    csvFile = cfgLoader.getCSVFile()
    if(csvFile['result']):
        sched.startCameraRecording()
        cameraData = fileManager.readCameraCSV(csvFile['path'])
        threads = []
        for row in cameraData.itertuples():
            #row[1] = Store. row[2] = shoppingCenter. row[3] = cameraID. row[4] = cameraIP.
            thread = threading.Thread(target = startRecording, args = (row[1], row[2], row[3], row[4],))
            threads.append(thread)
            thread.start()
    else:
        print('file not found.')

def main():

    sched.scheduleCameraRecording(recordCameras, configFile['VIDEO']['startTime'], configFile['VIDEO']['endTime'])
    while 1:
        sched.run_pending()
        time.sleep(1)
        
main()
