#!/bin/sh

if [ "$TRAVIS_OS_NAME" = "osx" ]
then
    source env/bin/activate
    pip install --editable .
    coverage run \
        --source ./plyer \
        -m unittest discover \
            --start-directory ./plyer/tests \
            --top-level-directory . \
            --failfast
    coverage report -m
fi
