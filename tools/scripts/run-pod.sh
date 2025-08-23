#!/bin/bash

echo '🧪 start test pod'
kubectl run -i --rm --tty interwebs-speed \
  --image=cassiofariasmachado/interwebs-speed:latest \
  --restart=Never \
  --overrides='{
    "apiVersion": "v1",
    "kind": "Pod",
    "spec": {
      "containers": [{
        "name": "interwebs-speed",
        "image": "cassiofariasmachado/interwebs-speed:latest",
        "imagePullPolicy": "Always",
        "command": ["/bin/sh"],
        "stdin": true,
        "stdinOnce": true,
        "tty": true,
        "volumeMounts": [{
          "mountPath": "/app/data",
          "name": "data"
        }]
      }],
      "volumes": [{
        "name": "data",
        "persistentVolumeClaim": {
          "claimName": "interwebs-speed-data"
        }
      }]
    }
  }'
