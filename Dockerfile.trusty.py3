FROM ubuntu:trusty-20180531

ENV APP_DIR=/app
RUN mkdir $APP_DIR
WORKDIR $APP_DIR
ENV PYTHONPATH=$PYTHONPATH:$(pwd)

# add https://launchpad.net/~deadsnakes for python 3.5
RUN echo 'deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu trusty main'\
    >> /etc/apt/sources.list.d/pythons.list
RUN echo 'deb-src http://ppa.launchpad.net/deadsnakes/ppa/ubuntu trusty main'\
    >> /etc/apt/sources.list.d/pythons.list

# install default packages
RUN apt-get update && \
    apt-get -y --force-yes install \
    python3-setuptools \
    python3.5-dev \
    openjdk-7-jdk \
    lshw \
    wget \
    git \
    && apt-get -y autoremove \
    && apt-get -y clean

# install PIP
RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip3.py
RUN python3.5 -V && \
    python3.5 get-pip3.py && \
    rm get-pip3.py && \
    python3.5 -m pip install --upgrade pip

# install dev packages
COPY devrequirements.txt .
RUN python3.5 -m pip install \
        --upgrade \
        --requirement devrequirements.txt
RUN python3.5 -m pip install \
    https://github.com/kivy/pyjnius/zipball/master

COPY . $APP_DIR
RUN python3.5 -m pip install .
ENTRYPOINT ["/app/entrypoint.sh", "py3"]
