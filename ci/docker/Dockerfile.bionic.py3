FROM ubuntu:bionic-20180821

ENV APP_DIR=/app
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

# install default packages
RUN apt-get update && \
    apt-get -y --force-yes install \
    build-essential \
    python3-setuptools \
    python3.6-dev \
    openjdk-8-jdk \
    lshw \
    wget \
    git \
    && apt-get -y autoremove \
    && apt-get -y clean

# generate user folder locations (Pictures, Downloads, ...)
RUN xdg-user-dirs-update

# install PIP
RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip3.py
RUN python3.6 -V && \
    python3.6 get-pip3.py && \
    rm get-pip3.py && \
    python3.6 -m pip install --upgrade pip

# install dev packages
COPY devrequirements.txt .
RUN python3.6 -m pip install \
        --upgrade \
        --requirement devrequirements.txt
RUN python3.6 -m pip install pyjnius

COPY . $APP_DIR
COPY ./ci/entrypoint.sh $APP_DIR
RUN python3.6 -m pip install .
ENTRYPOINT ["/app/entrypoint.sh", "py3"]
