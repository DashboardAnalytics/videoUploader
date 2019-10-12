import schedule
import time

runningStatus = False

def stopCameraRecording():
    print('Recording time ended.\r\n')
    global runningStatus
    runningStatus = False

def scheduleCameraRecording(job, startTime, endTime):

    schedule.every().day.at(startTime).do(job)
    schedule.every().day.at(endTime).do(stopCameraRecording)

def startCameraRecording():
    print('Recording Time Started.\r\n')
    global runningStatus
    runningStatus = True

def run_pending():
    schedule.run_pending()

def getRunningStatus():
    global runningStatus
    return runningStatus
