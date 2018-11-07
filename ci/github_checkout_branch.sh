#!/bin/sh

# use real branch name instead of detached HEAD
# unless the job is created for a GitHub Pull Request
if [ "$TRAVIS_PULL_REQUEST_BRANCH" = "" ]
then
    git checkout $TRAVIS_BRANCH
fi
