DROP TABLE IF EXISTS movie_ratings;

CREATE TABLE IF NOT EXISTS movie_ratings (
    id varchar(255),
    averageRating float,
    numVotes int
);

SHOW VARIABLES LIKE 'secure_file_priv'; 
-- importante que esteja dentro dessa pasta para que o arquivo seja encontrado e o mysql workbench aceite o arquivo vindo dessa fonte

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/data.tsv'
INTO TABLE movie_ratings
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT * FROM movie_ratings;
