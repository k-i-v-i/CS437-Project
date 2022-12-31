CREATE DATABASE users;

CREATE TABLE `user` (
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `user`
  ADD PRIMARY KEY (`userid`);

INSERT INTO `user` ( `name`,  `password`) VALUES
( 'Jhon smith', 'smith@webdamn.com', '123'),
( 'Adam William', 'adam@webdamn.com', '123');
