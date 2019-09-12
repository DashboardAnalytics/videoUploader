import json
import requests
import base64

baseUrl = 'http://127.0.0.1:8080/controlTables/'

def createVideoData(videoData):

    response = requests.post(baseUrl + 'create', data = videoData)

    data = response.json()

    return data

def getVideoDataByName(videoName):

    response = requests.get(baseUrl + 'getVideoName', data = {'videoName': videoName})
    data = response.json()

    return data

def updateVideoStatus(videoName, status):

    response = requests.post(baseUrl + 'updateStatus', data = {'videoName': videoName, 'status': status})
    data = response.json()

    return data

def eraseVideoFromDB(videoName):

    response = requests.post(baseUrl + 'eraseAll')

    data = response.json()

    return data
