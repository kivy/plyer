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

style_dependencies()
{
  python -m pip install --upgrade pip

  pip install flake8
}

style()
{
  python -m flake8 . --show-source
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
}

upload_coverage()
{
  python -m coveralls
}

build()
{
  python setup.py sdist
  python setup.py bdist_wheel --universal
}

deploy()
{
  # deploy to PyPI
  python -m twine upload dist/*
}
