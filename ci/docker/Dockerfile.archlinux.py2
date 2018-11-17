FROM base/archlinux

ENV APP_DIR=/app
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

# install default packages
RUN pacman -Fy && \
    pacman -Sy && \
    yes |pacman -Sy \
    gcc \
    python2 \
    jdk-openjdk \
    lshw \
    wget \
    apparmor \
    xdg-user-dirs \
    && yes |pacman -Rns $(pacman -Qtdq) ||true \
    && yes |pacman -Sc

# generate user folder locations (Pictures, Downloads, ...)
RUN xdg-user-dirs-update

# install PIP
RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
RUN python2 -V && \
    python2 get-pip.py && \
    rm get-pip.py && \
    python2 -m pip install --upgrade pip


# install dev packages
COPY devrequirements.txt .
RUN python2 -m pip install \
        --upgrade \
        --requirement devrequirements.txt
RUN python2 -m pip install pyjnius

COPY . $APP_DIR
COPY ./ci/entrypoint.sh $APP_DIR
RUN python2 -m pip install .
ENV PYTHON=/usr/bin/python2
ENTRYPOINT ["/app/entrypoint.sh", "env"]
