#!/bin/sh

# manual download of get-pip.py on OSX because TLS1.2+ is required
# source: pyfound.blogspot.com/2017/01/time-to-upgrade-your-python-tls-v12.html
# install pip, virtualenv and plyer deps to virtualenv
if [ "$TRAVIS_OS_NAME" = "osx" ]
then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

    if [ "$PY" = "3" ]
    then
        sudo python3 get-pip.py
    else
        sudo python get-pip.py
    fi

    if [ "$PY" = "3" ]
    then
        pip3 install --user virtualenv
        python3 -m virtualenv env
    else
        pip install --user virtualenv
        python -m virtualenv env
    fi

    # activate virtualenv
    source env/bin/activate

    # install requirements from PyPI
    pip install --upgrade --requirement devrequirements.txt

    # install PyOBJus from source (master branch)
    pip install https://github.com/kivy/pyobjus/zipball/master
fi
