#!/bin/sh

# https://github.com/travis-ci/travis-ci/issues/6307
if [ "$TRAVIS_OS_NAME" == "osx" ]
then
    curl -sSL https://rvm.io/mpapis.asc | gpg --import -
    rvm get head
fi
