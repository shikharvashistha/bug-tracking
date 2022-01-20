FROM postgres:latest

FROM python:latest

WORKDIR /bug

COPY ./requirements.txt /bug/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bug/requirements.txt

COPY ./src/ /bug/src/

RUN cd src/
#RUN uvicorn main:app --port=8000 --reload
EXPOSE 8080