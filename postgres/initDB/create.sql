CREATE TABLE IF NOT EXISTS orders(
  order_id varchar(10),
  priority int,
  type varchar(50),
  posted_by varchar(50),
  assigned_to varchar(50),
  status varchar(50),
  summary varchar(50),
  description varchar(50),
  deadline int,
  created_date varchar(50),
  closed_date varchar(50),
  PRIMARY KEY( order_id )
);

CREATE TABLE IF NOT EXISTS logs(
  created_by varchar(50),
  order_id varchar(10),
  event varchar(50),
  created_date varchar(50),
  closed_date varchar(50)
);

CREATE TABLE IF NOT EXISTS users(
    user_id int,
    name varchar(50),
    email varchar(50)
);