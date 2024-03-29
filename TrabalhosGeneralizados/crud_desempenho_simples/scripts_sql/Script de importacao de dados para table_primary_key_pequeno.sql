DROP TABLE IF EXISTS movie_ratings_primary_key_pequeno;

CREATE TABLE IF NOT EXISTS movie_ratings_primary_key_pequeno (
    id varchar(255) PRIMARY KEY,
    averageRating float,
    numVotes int
);

SHOW VARIABLES LIKE 'secure_file_priv';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/data_pequeno.csv'
INTO TABLE movie_ratings_primary_key_pequeno
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT * FROM movie_ratings_primary_key_pequeno;
SELECT id FROM movie_ratings_primary_key_pequeno ORDER BY id DESC LIMIT 1;

