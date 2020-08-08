FROM fedora:28

ENV APP_DIR=/app
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

# install default packages
# redhat-rpm-config: https://stackoverflow.com/a/34641068/5994041
RUN yum -y install \
    gcc \
    python3-devel \
    java-1.8.0-openjdk \
    java-1.8.0-openjdk-devel \
    lshw \
    wget \
    xdg-user-dirs \
    redhat-rpm-config \
    && yum -y autoremove \
    && yum clean all

# generate user folder locations (Pictures, Downloads, ...)
RUN xdg-user-dirs-update

# install PIP
RUN python3.6 -V && \
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
