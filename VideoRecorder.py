from datetime import datetime
import numpy as np
import cv2, os, glob, time
    
url='http://192.168.1.107:8081/video.mjpg'

# Funcion que obtiene una grabacion desde una url, y
# escribe el archivo de salida en formato .avi
# Entradas: Int con numero de video actual, string con fecha actual e int con cantidad de frames por segundo
# Salidas: Boolean indicando si el proceso se llevo a cabo correctamente
def videoRecorder(nVideo, today, nFrames):
    # Se obtiene nuevamente la fecha, solo que ademas con la hora actual
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    # Se genera el nombre del archivo de salida
    recordDirectory = './records/'+today+"/"
    filename = recordDirectory+"stream "+dt_string+" n"+str(nVideo)+" fr"+str(5)+".avi"
    # Se comienza a capturar el streaming del video
    cap = cv2.VideoCapture(url)
    if not cap:
        print("!!! Failed VideoCapture: invalid parameter!")
        return False
    cap.set(cv2.CAP_PROP_FPS, nFrames)
    # Se define el codec y se crea el objeto de tipo VideoWriter
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('M','J','P','G'), nFrames, (frame_width,frame_height))

    aux2 = 0
    aux = 0
    while aux < 300:
        # Se lee frame a frame
        ret, frame = cap.read()
        # Si se produce un error al leer el frame, se detiene el proceso
        if type(frame) == type(None):
            print("!!! Couldn't read frame!")
            return False
        # Se escribe el frame en el archivo de salida
        if(aux2 % 5 == 0):
            out.write(frame)
            aux += 1
        aux2 += 1
    # Se liberan los recursos de captura y de escritura
    cap.release()
    out.release()
    return True


def init():
    # Se obtiene fecha actual para generar la carpeta correspondiente
    today = datetime.now()
    dt_string = today.strftime("%d-%m-%Y")
    # Se setean los parametros iniciales
    nVideo = 1
    n = int(input("Cantidad de partes: "))
    nFrames = 5
    # Si la carpeta no existe, se crea
    if(not os.path.isdir('./records/'+dt_string)):
        os.mkdir('./records/'+dt_string)
    # Si ya existe, es probable que ya existan videos, por lo que
    # se obtiene el nombre del ultimo video creado para continuar con
    # la serie 
    else:
        directory = './records/'+dt_string+"/*"
        listOfFiles = glob.glob(directory) 
        # Se comprueba que existan archivos adentro de la carpeta
        if(len(listOfFiles) != 0):
            latestFile = max(listOfFiles, key=os.path.getctime)
            # Se busca el caracter n, donde en la posicion siguiente
            # se tiene el numero del video
            nVideo = int(latestFile[latestFile.find('n')+1]) + 1
            # Se modifica n para que corresponda con la cantidad
            # de partes que se desea grabar
            n = n + nVideo - 1
    # Mientras no existan problemas al grabar y queden partes por grabar,
    # se llama a la funcion videoRecorder
    r = True
    while ((nVideo<=n) and (r)):
        print ("Recording video Nº "+str(nVideo)+"...")    
        r = videoRecorder(nVideo, dt_string, nFrames)
        nVideo += 1
init()
