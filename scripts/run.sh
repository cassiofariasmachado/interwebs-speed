DOCKER_TAG='interwebs-speed'

echo 'Step 1: Remove service'
docker stop $DOCKER_TAG
docker rm $DOCKER_TAG

echo 'Step 1: Build new service version'
docker build -t $DOCKER_TAG .

echo 'Step 2: Run service'
docker run -d \
    -v /interwebs-speed:/app/csv \
    --name $DOCKER_TAG \
    $DOCKER_TAG
