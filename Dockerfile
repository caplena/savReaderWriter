FROM --platform=linux/amd64 python:3.11

WORKDIR /app/

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN set -e; \
    apt-get update; \
    apt-get -y install locales; \
    echo 'C.UTF-8 UTF-8' > /etc/locale.gen; \
    echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen; \
    echo 'de_DE.cp1252 CP1252' >> /etc/locale.gen; \
    locale-gen

COPY . .

RUN python -m pip install tox
RUN python setup.py install

CMD tox -e py311
