-- Import data into the Country table
LOAD DATA LOCAL INFILE 'data/country.csv' 
INTO TABLE Country 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS;  -- Ignore the header row

-- Import data into the sport table
LOAD DATA LOCAL INFILE 'data/sport.csv' 
INTO TABLE Sport
FIELDS TERMINATED BY ',' 
ENCLOSED BY ''
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Import data into venue table
LOAD DATA LOCAL INFILE 'data/venue.csv' 
INTO TABLE Venue
FIELDS TERMINATED BY ',' 
ENCLOSED BY ''
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Import data into athlete table
LOAD DATA LOCAL INFILE 'data/athlete.csv' 
INTO TABLE Athlete
FIELDS TERMINATED BY ',' 
ENCLOSED BY ''
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Import data into events table
LOAD DATA LOCAL INFILE 'data/events.csv' 
INTO TABLE Events
FIELDS TERMINATED BY ',' 
ENCLOSED BY ''
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Import data into medallist table
LOAD DATA LOCAL INFILE 'data/medallist.csv' 
INTO TABLE Medallist
FIELDS TERMINATED BY ',' 
ENCLOSED BY ''
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Import data into competesIn table
LOAD DATA LOCAL INFILE 'data/competesIn.csv' 
INTO TABLE CompetesIn
FIELDS TERMINATED BY ',' 
ENCLOSED BY ''
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

