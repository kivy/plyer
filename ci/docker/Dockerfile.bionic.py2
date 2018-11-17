FROM ubuntu:bionic-20180821

ENV APP_DIR=/app
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

# install default packages
RUN apt-get update && \
    apt-get -y --force-yes install \
    build-essential \
    python-setuptools \
    python-dev \
    openjdk-8-jdk \
    lshw \
    wget \
    git \
    && apt-get -y autoremove \
    && apt-get -y clean

# generate user folder locations (Pictures, Downloads, ...)
RUN xdg-user-dirs-update

# install PIP
RUN wget https://bootstrap.pypa.io/2.6/get-pip.py -O get-pip2.py
RUN python -V && \
    python get-pip2.py && \
    rm get-pip2.py && \
    python -m pip install --upgrade pip

# install dev packages
COPY devrequirements.txt .
RUN python -m pip install \
        --upgrade \
        --requirement devrequirements.txt
RUN python -m pip install pyjnius

COPY . $APP_DIR
COPY ./ci/entrypoint.sh $APP_DIR
RUN python -m pip install .
ENTRYPOINT ["/app/entrypoint.sh", "py2"]
