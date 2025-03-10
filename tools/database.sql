ALTER USER 'root'@'localhost' IDENTIFIED BY 'mogumogu';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE DATABASE eternal;
USE eternal;

CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int NOT NULL,
  `user_id` int NOT NULL,
  `duration` int NOT NULL,
  `cooldown` int NOT NULL,
  `endtime` date NOT NULL,
  `clients` int NOT NULL,
  `api_key` varchar(255) DEFAULT NULL
);

INSERT INTO users VALUES ('admin', 'admin', 0, 1, 0, 0, "2040-06-18", -1, '');