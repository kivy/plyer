#!/bin/sh
set -vex

if [ "$1" = "py2" ]
then
    PYTHON=$(which python)
elif [ "$1" = "py3" ] || [ "$1" = "pep8" ]
then
    PYTHON=$(which python3.5)
else
    exit 1
fi

# pep8 check
if [ "$2" = "style" ]
then
    $PYTHON -m pycodestyle "$(pwd)" \
        --exclude=pep8.py,compat.py,utils.py \
        --ignore=E402,W503
    touch "$(pwd)/__init__.py"
    $PYTHON -m pylint "$(pwd)"
    exit 0
fi

# tests
nosetests \
    --exe \
    --stop \
    --nocapture \
    --with-coverage \
    --cover-package=plyer \
    $APP_DIR/plyer/tests
