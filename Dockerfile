# syntax=docker/dockerfile:1

FROM python:3.11.8

WORKDIR /tikta

COPY ./requirements.txt ./tikta/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./tikta/requirements.txt

COPY ./app /tikta/app
COPY ./resources /tikta/resources
COPY ./init.py /tikta/init.py
COPY ./main.py /tikta/main.py
COPY ./run.sh /tikta/run.sh

CMD ["sh", "./run.sh"]
