FROM python:latest

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./ ./

CMD ["uvicorn", "main:app", "--reload"]
EXPOSE 8000