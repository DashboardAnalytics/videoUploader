import schedule
import time

runningStatus = False

def stopCameraRecording():
    runningStatus = False

def startCameraRecording(job, startTime, endTime):

    runningStatus = True
    schedule.every().day.at(startTime).do(job)
    schedule.every().day.at(endTime).do(stopCameraRecording)

def run_pending():
    schedule.run_pending()

def getRunningStatus():
    return runningStatus
