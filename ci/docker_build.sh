#!/bin/sh

# build docker images from Travis matrix
if [ "$TRAVIS_OS_NAME" == "linux" ] && [ -v DOCK ]
then

    # separate images for Python 2
    if [ "$PY" == "2" ]
    then
        docker build \
            --tag plyer:py2 \
            --file docker/Dockerfile.$IMAGE.py2 \
            "$(pwd)/.."

    # separate images for Python 3
    elif [ "$PY" == "3" ]
    then
        docker build \
            --tag plyer:py3 \
            --file docker/Dockerfile.$IMAGE.py3 \
            "$(pwd)/.."

        # style image that inherits layers from Python 3 image
        if [ "$RUN" == "style" ]
        then
            docker build \
                --tag plyer:style \
                --file docker/Dockerfile.$IMAGE.style \
                "$(pwd)/.."
        fi
    fi
fi
