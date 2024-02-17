DROP TABLE IF EXISTS movie_ratings_primary_key;

CREATE TABLE IF NOT EXISTS movie_ratings_primary_key (
    id varchar(255) PRIMARY KEY,
    averageRating float,
    numVotes int
);

SHOW VARIABLES LIKE 'secure_file_priv';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/data.tsv'
INTO TABLE movie_ratings_primary_key
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT * FROM movie_ratings_primary_key;

