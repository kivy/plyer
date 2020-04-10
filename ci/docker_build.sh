#!/bin/sh

# build docker images from Travis matrix
if [ "$TRAVIS_OS_NAME" = "linux" ] && [ "$DOCK" = "1" ]
then
    docker build \
        --tag plyer:py3 \
        --file ci/docker/Dockerfile.$IMAGE.py3 \
        "$(pwd)"

    # style image that inherits layers from Python 3 image
    if [ "$RUN" = "style" ]
    then
        docker build \
            --tag plyer:style \
            --file ci/docker/Dockerfile.$IMAGE.style \
            "$(pwd)"
    fi
fi
