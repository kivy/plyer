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
    $PYTHON -m pylint --disable=R0205 "$(pwd)"
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
