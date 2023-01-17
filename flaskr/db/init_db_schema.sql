DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS reviews;

CREATE TABLE users (
  user_id TEXT UNIQUE NOT NULL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL,
  is_worker NUMBER(1)
);

CREATE TABLE orders (
  order_id TEXT UNIQUE NOT NULL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  address_from TEXT NOT NULL,
  address_to TEXT NOT NULL,
  created_by TEXT NOT NULL,
  time_start DATETIME NOT NULL,
  time_finish DATETIME NOT NULL,
  assigned_to TEXT,
  completed NUMBER(1),
  FOREIGN KEY (created_by) REFERENCES users(user_id), 
  FOREIGN KEY (assigned_to) REFERENCES users(user_id) 
);

CREATE TABLE reviews (
  review_id TEXT UNIQUE NOT NULL PRIMARY KEY,
  author_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  grade NUMBER(10) NOT NULL,
  comment TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users(user_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);