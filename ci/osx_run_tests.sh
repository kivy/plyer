#!/bin/sh

if [ "$TRAVIS_OS_NAME" = "osx" ]
then
    pip install --editable .
    nosetests \
        --stop \
        --nocapture \
        ./plyer/tests
fi
