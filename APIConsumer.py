import json
import requests
import base64
import time
baseUrl = 'http://127.0.0.1:3000/control-tables/'

apikey = 'C020D7AD82F2F7F1476A8E95D95A39AA34E714EB8277539AF0D8011E1E8CB18D850B5D8DC4678F6E217271D398E635AA119F7FB88F55199A8C3CB4D628CA3DDA';

def createVideoData(filename, videoNumber, store, shoppingCenter):

    videoData = {"video_name": filename, "status": 1, "video_number": videoNumber, "store": store, "shopping_center": shoppingCenter}
    response = requests.post(baseUrl, json = videoData)

    data = response.json()
    return data

def getVideoDataByName(videoName):

    response = requests.get(baseUrl + 'getVideoName', json = {'videoName': videoName})
    data = response.json()

    return data

def updateVideoStatusReady(videoId, filename, videoNumber, store, shoppingCenter):

    videoData = {"video_name": filename, "status": 2, "video_number": videoNumber, "store": store, "shopping_center": shoppingCenter}
    response = requests.put(baseUrl + str(videoId), json = videoData)

def eraseVideosFromDB(videoName):

    response = requests.post(baseUrl + 'eraseAll')

    data = response.json()

    return data
