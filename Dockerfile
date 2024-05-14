# syntax=docker/dockerfile:1

FROM python:3.11.8

WORKDIR /synaps

COPY ./requirements.txt ./synaps/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./synaps/requirements.txt

COPY ./app /synaps/app
COPY ./resources /synaps/resources
COPY ./init.py /synaps/init.py
COPY ./main.py /synaps/main.py
COPY ./run.sh /synaps/run.sh

CMD ["sh", "./run.sh"]
