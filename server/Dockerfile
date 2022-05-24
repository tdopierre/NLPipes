FROM python:3.8

WORKDIR /app
COPY requirements.txt .

RUN ls -lah
RUN pwd
RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install -r requirements.txt

EXPOSE 8001

