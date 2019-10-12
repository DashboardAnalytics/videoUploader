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

printf "\n\n***Sistema instalado correctamente!***\n\n"

printf "\nDesea configurar gcloud? (Y/N)\n"

read option

if [ $option == "Y"]
then
    apt-get install -y lsb-core

    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

    apt-get update && apt-get install -y google-cloud-sdk

    apt-get install -y google-cloud-sdk-app-engine-python

    gcloud init

    gcloud iam service-accounts keys create ~/key.json \
    --iam-account test@dashboard-analytics-255717.iam.gserviceaccount.com
