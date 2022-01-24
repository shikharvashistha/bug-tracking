CREATE TABLE IF NOT EXISTS bugs(
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

CREATE TABLE IF NOT EXISTS logs(
  created_by varchar(50),
  bug_id int,
  event varchar(50),
  created_date varchar(50),
  closed_date varchar(50)
);

CREATE TABLE IF NOT EXISTS users(
    user_id int,
    name varchar(50),
    email varchar(50)
);