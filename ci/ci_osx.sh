#!/bin/sh

dependencies()
{
  python -m pip install --upgrade pip

  pip install --upgrade -r devrequirements.txt
  pip install https://github.com/kivy/pyobjus/zipball/master
}

tests()
{
  pip install --editable .
  coverage run \
      --source ./plyer \
      -m unittest discover \
          --start-directory ./plyer/tests \
          --top-level-directory . \
          --failfast
  coverage report -m
}
