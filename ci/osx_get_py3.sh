#!/bin/sh

# get Py3 because it's not present in any OSX image on Travis
if [ "$TRAVIS_OS_NAME" = "osx" ]
then
    pyftp=https://www.python.org/ftp/python/3.5.4/
    py3pkg=python-3.5.4rc1-macosx10.6.pkg

    if [ "$PY" = "3" ]
    then
        curl -O -L $pyftp$py3pkg
        sudo installer -package $py3pkg -target /
    fi
fi
