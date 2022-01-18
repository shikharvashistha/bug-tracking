# pull latest postgres image
FROM postgres:latest
#run postgres on port 5432
EXPOSE 5432
#run postgres with a name
CMD ["postgres"]

FROM python:3.9

WORKDIR /bug

COPY ./requirements.txt /bug/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bug/requirements.txt

COPY ./src/ /bug/src/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
