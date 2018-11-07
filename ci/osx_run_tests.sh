#!/bin/sh

if [ "$TRAVIS_OS_NAME" = "osx" ]
then
    source env/bin/activate
    pip install --editable .
    nosetests \
        --stop \
        --nocapture \
        ./plyer/tests
fi
