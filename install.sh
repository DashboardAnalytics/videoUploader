#!/bin/bash

apt-get update

apt-get install -y python3

apt-get install -y python3-pip

apt-get install -y libsm6 libxext6 libxrender-dev

pip3 install opencv-python

pip3 install schedule

pip3 install requests

pip3 install google-api-python-client

pip3 install google-cloud-storage

pip3 install pandas

git clone https://github.com/DashboardAnalytics/videoUploader.git

cd videoUploader

git pull

python3 videoUploader.py
