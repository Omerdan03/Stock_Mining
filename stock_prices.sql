CREATE TABLE `stock_price` (
  `date` datetime,
  `stock_name` varchar(255),
  `open_price` float,
  `high_price` float,
  `low_price` float,
  `close_price` float,
  `adj_close_price` float,
  `volume` bigint,
  PRIMARY KEY (date, stock_name)
);

CREATE TABLE `stock_info` (
  `stock_name` varchar(255) PRIMARY KEY,
  `url` varchar(255)
);

--ALTER TABLE `stock_price` ADD FOREIGN KEY (`stock_name`) REFERENCES `stock_info` (`stock_name`);
