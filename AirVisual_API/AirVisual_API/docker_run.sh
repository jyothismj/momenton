#!/bin/bash

set -x

docker stop my-running-script
docker rm my-running-script

pwd

docker run \
-e http_proxy=$bamboo_http_proxy \
-e https_proxy=$bamboo_http_proxy \
-e no_proxy=$bamboo_no_proxy \
    -t --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.6.1 \
    ./TestAPIs.py

RV=$?
echo "#####-----RV $RV"
echo "#####-----END $0"
exit $RV
