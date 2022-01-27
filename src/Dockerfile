FROM python:latest

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./ ./

EXPOSE 8000

ENTRYPOINT python3 main.py