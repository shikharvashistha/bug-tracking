FROM postgres:latest
ENV POSTGRES_PASSWORD=123
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres
WORKDIR /postgres
COPY ./initDB/create.sql /postgres/initDB/create.sql
EXPOSE 5432