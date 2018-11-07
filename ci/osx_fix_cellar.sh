#!/bin/sh

# uninstall old GNUpg, install new one and add Brew
# 'Cellar' folder to the path (contains binaries)
if [ "$TRAVIS_OS_NAME" = "osx" ]
then
    brew uninstall gnupg
    brew install gnupg2
    sudo ln -sv /usr/local/Cellar/gnupg /usr/local/Cellar/gpg || true
    sudo ln -sv /usr/local/Cellar/gnupg /usr/local/Cellar/gpg2 || true
    export PATH=$PATH:/usr/local/Cellar
fi
