# bug-tracking
## CI [![Docker Image CI](https://github.com/shikharvashistha/bug-tracking/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/shikharvashistha/bug-tracking/actions/workflows/docker-image.yml)


## Not using docker ? follow these steps
- `sudo docker run --name postgresSQL -e POSTGRES_PASSWORD=123 -p 5432:5432 -d postgres`

### or(if container already created)

- `sudo docker start [container_id]` //container_id is the id of the container sudo docker ps --all //list all containers

- `docker exec -it [container_id] bash`

- `psql -U postgres` //connect to database

- `\l` //list databases

- `\c postgres` //connect to database

- `docker logs -f [container_id]` //to get logs in seperate cli

### Python Dependencies
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
pip install python-multipart
uvicorn main:app --reload

CREATE TABLE bugs(
  bug_id int,
  priority int,
  type varchar(10),
  posted_by varchar(10),
  assigned_to varchar(10),
  status varchar(1),
  summary varchar(50),
  description varchar(50),
  deadline int,
  created_date varchar(50),
  closed_date varchar(50),
  PRIMARY KEY( bug_id )
);

CREATE TABLE logs(
  created_by varchar(50),
  bug_id int,
  event varchar(50),
  created_date varchar(50),
  closed_date varchar(50)
);
INSERT INTO logs(created_by, bug_id, event) VALUES('shikhar', 1, 'Bug Created', '2020-01-01', '2020-01-01');

INSERT INTO bugs(bug_id, priority, type, posted_by, assigned_to, status, description, deadline, created_date, closed_date) VALUES(1, 1, 'Bug', 'shikhar', 'shikhar', 'Open', 'Bug in UI', '2', '2020-01-01', '2020-01-01');
VALUES (2, 3, 'help', 'shikhar', 'shikhar', 'closed', 'help request');

http://127.0.0.1:8000/bug/create/%7B1%7D/%7B3%7D/%7B%22support%22%7D/%7B%22shikharvashistha%22%7D/%7B%22shikharvashistha%22%7D/%7B%22opened%22%7D/%7B%22supportreques%22%7D


/bug/create/{1}/{3}/{"support"}/{"shikhar"}/{"shikhar"}/{"opened"}/{"support request"}

github.com/login?

http://127.0.0.1:8000/bug/create?bug_id=1&priority=3&type=issue&posted_by=shikhar&assigned_to=shikhar&status=opened&description=issue
```
