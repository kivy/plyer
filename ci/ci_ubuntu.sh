#!/bin/sh
set -ex

dependencies()
{
  # install default packages
  sudo apt-get update && \
  sudo apt-get -y --force-yes install \
  build-essential \
  openjdk-8-jdk \
  lshw \
  wget \
  git \
  && apt-get -y autoremove \
  && apt-get -y clean

  # generate user folder locations (Pictures, Downloads, ...)
  xdg-user-dirs-update

  # install PIP
  python -V
  python -m pip install --upgrade pip

  # install dev packages
  python -m pip install \
  --upgrade \
  --requirement devrequirements.txt
  python -m pip install pyjnius

  python -m pip install .
}

deployment_dependencies()
{
  python -m pip install --upgrade pip

  pip install setuptools wheel twine
}

# pep8 check
style()
{
  python -m pycodestyle "$(pwd)" \
  --exclude=pep8.py,compat.py,utils.py \
  --ignore=E402,W503

  touch "$(pwd)/__init__.py"

  python -m pylint \
  --jobs=0 \
  --disable=C0103,C0111,C0123,C0200,C0325,C0411,C0412,C1801,E0203,E0401 \
  --disable=E0602,E0611,E0711,E1003,E1101,E1102,R0201,R0205,R0801,R0903 \
  --disable=R0912,R0914,R1702,R1705,R1710,R1711,R1714,W0101,W0109 \
  --disable=W0201,W0212,W0221,W0223,W0401 \
  --disable=W0613,W0614 \
  "$(pwd)"
}

tests()
{
  # tests and coverage for plyer package
  python -m coverage run \
  --source plyer \
  -m unittest discover \
  --start-directory plyer/tests \
  --top-level-directory . \
  --failfast

  coverage report -m

  # submit coverage report from tests to coveralls.io
  # requires: REPO_TOKEN, SERVICE_NAME, JOB_ID, PULL_REQUEST
  coveralls || true
}

deploy()
{
  # deploy to PyPI
  python setup.py sdist bdist_wheel
  python -m twine upload dist/*
}
