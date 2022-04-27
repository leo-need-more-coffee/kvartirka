FROM ubuntu
FROM python
RUN mkdir /api
WORKDIR /api
ADD . /api
RUN ls -a
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip \
    && apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

