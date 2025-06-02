#!/bin/bash

DOCKER_TAG='interwebs-speed'

echo '🛑 remove service'
docker stop $DOCKER_TAG
docker rm $DOCKER_TAG

echo '🔨 build service'
docker build -t $DOCKER_TAG .

echo '✅ run service'
docker run -d \
    -v ./data:/data \
    --name $DOCKER_TAG \
    $DOCKER_TAG \
    analyze
