CREATE TABLE IF NOT EXISTS statistical_records (
  id INT NOT NULL AUTO_INCREMENT,
  date DATE NOT NULL,
  respondent INT NOT NULL,
  sex INT NOT NULL,
  age INT NOT NULL,
  weight DECIMAL(26, 18) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY date_respondent (date, respondent),
  KEY ix_statistical_records_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/statistical_records.csv'
IGNORE INTO TABLE statistical_records
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@dummy, @date_str, respondent, sex, age, weight)
SET date = STR_TO_DATE(@date_str, '%Y%m%d');
