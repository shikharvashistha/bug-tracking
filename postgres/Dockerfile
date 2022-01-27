FROM postgres:latest
ENV POSTGRES_PASSWORD=123
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres
WORKDIR /postgres
COPY ./initDB/create.sql /postgres/initDB/create.sql
COPY launch.sh .
RUN chmod +x launch.sh
EXPOSE 5432
ENTRYPOINT ./launch.sh