CREATE TABLE `logs` (
  'logid' INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `ip` VARCHAR(15) NOT NULL,
  `country` VARCHAR(100) ,
  `network` VARCHAR(255) ,
  'attempt' VARCHAR(100),
  'status' VARCHAR(100),
  'verdict' VARCHAR(100),
  'virustotal' INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `logs`
  ADD PRIMARY KEY (`logid`);