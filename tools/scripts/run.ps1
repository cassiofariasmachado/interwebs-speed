$DOCKER_TAG = 'interwebs-speed'

Write-Host '🛑 remove service'
docker stop $DOCKER_TAG
docker rm $DOCKER_TAG

Write-Host '🔨 build service'
docker build -t $DOCKER_TAG .

Write-Host '✅ run service'
docker run -d `
    -v "$PWD/data:/data" `
    --name $DOCKER_TAG `
    $DOCKER_TAG `
    analyze
