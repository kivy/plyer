#!/bin/sh
set -vex

if [ "$1" = "py2" ]
then
    PYTHON=$(which python)
elif [ "$1" = "py3" ] || [ "$1" = "pep8" ]
then
    PYTHON=$(which python3.6)
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
    $PYTHON -m pylint \
        --jobs=0 \
        --disable=C0103,C0111,C0123,C0200,C0325,C0411,C0412,C1801,E0203,E0401 \
        --disable=E0602,E0611,E0711,E1003,E1101,E1102,R0201,R0205,R0801,R0903 \
        --disable=R0912,R0914,R1702,R1705,R1710,R1711,R1714,W0101,W0109,W0150 \
        --disable=W0201,W0212,W0221,W0223,W0401,W0511,W0601,W0603 \
        --disable=W0613,W0614 \
        "$(pwd)"
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

# submit coverage report from (nose) tests to coveralls.io
# requires: REPO_TOKEN, SERVICE_NAME, JOB_ID, PULL_REQUEST
coveralls || true

# deploy to PyPI if set in CI with PLYER_DEPLOY variable
if [ "$PLYER_DEPLOY" = "1" ]; then
    $PYTHON setup.py sdist bdist_wheel
    $PYTHON -m twine upload dist/*
fi
