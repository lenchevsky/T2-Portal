#!/bin/bash
# @Project:       POS  Tools Portal (PTP)
# @Version:       0.1
# @Author:        Oleg Snegirev <ol.snegirev@gmail.com>
# @Functionality: Local development build script
echo "Removing old container"
if [[ $(docker ps -a | grep ptp_dev_test) ]]; then
    docker rm -f ptp_dev_test
fi

echo "Removing old images"
if [[ $(docker images -a | grep ptp_dev_image) ]]; then
    docker rmi docker.snegirev.ml:443/ptp_dev_image
fi

echo "Building contaner"
docker build -t docker.snegirev.ml:443/ptp_dev_image .

echo "Running container"
docker run --name ptp_dev_test -a stdout -a stdin -i -p 8000:8000 -p 33061:3306 -p 56721:5672  docker.snegirev.ml:443/ptp_dev_image

echo "Stoping old container"
docker stop ptp_dev_test

echo "All done"