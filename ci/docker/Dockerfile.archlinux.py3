FROM base/archlinux

ENV APP_DIR=/app
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

# install default packages
RUN pacman -Fy && \
    pacman -Sy && \
    yes |pacman -Sy \
    gcc \
    extra/python \
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
RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip3.py
RUN python -V && \
    python get-pip3.py && \
    rm get-pip3.py && \
    python -m pip install --upgrade pip

# install dev packages
COPY devrequirements.txt .
RUN python -m pip install \
        --upgrade \
        --requirement devrequirements.txt
RUN python -m pip install pyjnius

COPY . $APP_DIR
COPY ./ci/entrypoint.sh $APP_DIR
ENV PYTHON=/usr/bin/python
ENTRYPOINT ["/app/entrypoint.sh", "env"]
