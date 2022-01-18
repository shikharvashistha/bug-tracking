# bug-tracking
## CI [![Docker Image CI](https://github.com/shikharvashistha/bug-tracking/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/shikharvashistha/bug-tracking/actions/workflows/docker-image.yml)
## How to run
- `sudo docker run --name postgresSQL -e POSTGRES_PASSWORD=123 -p 5432:5432 -d postgres`

### or

- `sudo docker start [container_id]` //container_id is the id of the container sudo docker ps --all //list all containers

- `docker exec -it [container_id] bash`

- `psql -U postgres` //connect to database

- `\l` //list databases

- `\c postgres` //connect to database

- `docker logs -f [container_id]` //to get logs in seperate cli

### Python Dependencies
python3 -m pip install --upgrade pip

`"uvicorn[standard]", fastapi, psycopg2`

### Run Application
`uvicorn main:app --reload`

## Open Application/docs for SWAGGER UI


## Notes
```
sudo docker pull postgres:latest
sudo docker run --name postgresSQL -e POSTGRES_PASSWORD=123 -p 5432:5432 -d postgres
docker exec -it [container_id] bash
psql -U postgres //connect to database
\l //list databases
\c postgres //connect to database
docker logs -f [container_id] //to get logs in seperate cli
sudo docker ps --all //list all containers

Day 4 2nd half
15-30 minutes slides


python3 -m pip install --upgrade pip
pip install "uvicorn[standard]"
pip install fastapi
pip install psycopg2
uvicorn main:app --reload

CREATE TABLE table_name(
  bug_id int,
  priority int,
  type varchar(10),
  posted_by char(10),
  assigned_to char(10),
  status char(10),
  summary char(50),
  description char(50),
   PRIMARY KEY( bug_id )
);


INSERT INTO bugs(bug_id, priority, type, posted_by, assigned_to, status, description)
VALUES (2, 3, 'help', 'shikhar', 'shikhar', 'closed', 'help request');

http://127.0.0.1:8000/bug/create/%7B1%7D/%7B3%7D/%7B%22support%22%7D/%7B%22shikharvashistha%22%7D/%7B%22shikharvashistha%22%7D/%7B%22opened%22%7D/%7B%22supportreques%22%7D


/bug/create/{1}/{3}/{"support"}/{"shikhar"}/{"shikhar"}/{"opened"}/{"support request"}

github.com/login?

http://127.0.0.1:8000/bug/create?bug_id=1&priority=3&type=issue&posted_by=shikhar&assigned_to=shikhar&status=opened&description=issue
```
