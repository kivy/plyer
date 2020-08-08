#!/bin/sh

if [ "$TRAVIS_OS_NAME" = "linux" ] && [ "$DOCK" = "1" ]
then

    if [ "$RUN" = "unit" ]
    then

        # running coverage report (COVERALLS=1)
        # and even deploy to PyPI (PLYER_DEPLOY=1) if asked for
        if [ "$COVERALLS" = "1" ]
        then
            docker run \
                --interactive \
                --tty \
                --env COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN \
                --env COVERALLS_SERVICE_NAME=travis-ci \
                --env TRAVIS_JOB_ID=$TRAVIS_JOB_ID \
                --env TRAVIS_PULL_REQUEST=$TRAVIS_PULL_REQUEST \
                --env PLYER_DEPLOY=${PLYER_DEPLOY:-"0"} \
                --env TWINE_REPOSITORY=$TWINE_REPOSITORY \
                --env TWINE_REPOSITORY_URL=$TWINE_REPOSITORY_URL \
                --env TWINE_USERNAME=$TWINE_USERNAME \
                --env TWINE_PASSWORD=$TWINE_PASSWORD \
                plyer:py3

        # ordinary tests run
        else
            docker run \
                --interactive \
                --tty \
                plyer:py3
        fi

    elif [ "$RUN" = "style" ]
    then
        docker run \
            --interactive \
            --tty \
            plyer:style
    fi
fi
