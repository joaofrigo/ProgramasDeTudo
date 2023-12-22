-- SHOW TABLES;
-- SHOW VARIABLES LIKE 'secure_file_priv';
-- SHOW GRANTS FOR 'joão marcos'@'localhost';
-- SHOW VARIABLES LIKE 'config_file';
-- select * from movies;
-- select * from ratings;
-- SELECT * FROM genome_scores;
-- SELECT * FROM genome_tags;
-- ELECT * FROM tags;


DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS genome_scores;
DROP TABLE IF EXISTS genome_tags;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
	userId INT PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS movies (
    movieId INT PRIMARY KEY,
    titles varchar(250),
    genres varchar(120) -- tags colocadas pelos usuarios
);

CREATE TABLE IF NOT EXISTS ratings  (
	userId INT, FOREIGN KEY (userId) REFERENCES users(userId), -- usuário que votou no filme
    movieId INT, FOREIGN KEY (movieId) REFERENCES movies(movieId), -- filme que foi votado
	rating FLOAT, -- rating do filme
    timestamp INT -- momento que foi feito tal rating
);

CREATE TABLE IF NOT EXISTS tags (
	userId INT, FOREIGN KEY (userId) REFERENCES users(userId), -- usuário que colocou a tag
    movieId INT, FOREIGN KEY (movieId) REFERENCES movies(movieId), -- filme que recebeu a tag
    tag varchar(120), -- tag colocada
    timestamp INT -- momento que foi colocada tal tag
);

CREATE TABLE IF NOT EXISTS genome_tags ( -- As tags que estão no genome-scores
	tagId INT PRIMARY KEY,
    tag varchar(120)
);

CREATE TABLE IF NOT EXISTS genome_scores (
	movieId INT, FOREIGN KEY (movieId) REFERENCES movies(movieId), -- filme que temos o score sobre
    tagId INT, FOREIGN KEY (tagId) REFERENCES genome_tags(tagId), --  a tag que nos referimos
    relevance double -- a relevância dessa tag para o filme específico. (bruxas não tem muito a ver com toy story, tag de genome score baixo)
);

DROP TABLE IF EXISTS tmp_users;
CREATE TEMPORARY TABLE tmp_users (userId INT); -- importante para pegar todos os ID de usuários distintos.
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ratings.csv'
INTO TABLE tmp_users
FIELDS TERMINATED BY ',' -- Delimitador de campo no arquivo CSV, cada vírgula uma coluna.
ENCLOSED BY '"' -- Caractere de aspas que envolve valores de campo, permite que filmes com vírgula sejam adequadamente importados.
LINES TERMINATED BY '\n' -- Delimitador de linha no arquivo CSV, cada fim de linha, uma nova linha.
IGNORE 1 ROWS -- Ignora a primeira linha (cabeçalho)
(userId, @movieId, @rating, @timestamp); -- Mapeia apenas a coluna userId ignorando as outras. No caso, cria variáveis temporarias para cada coluna.

INSERT INTO users (userId) -- insiro todos os userId que são diferentes do tmp_users e coloca dentro da tabela users.
SELECT DISTINCT userId from tmp_users;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/movies.csv'
INTO TABLE movies
FIELDS TERMINATED BY ',' -- Delimitador de campo no arquivo CSV, cada vírgula uma coluna.
ENCLOSED BY '"' -- Caractere de aspas que envolve valores de campo, permite que filmes com vírgula sejam adequadamente importados.
LINES TERMINATED BY '\n' -- Delimitador de linha no arquivo CSV, cada fim de linha, uma nova linha.
IGNORE 1 ROWS; -- Ignora a primeira linha (cabeçalho).

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ratings.csv'
INTO TABLE ratings
FIELDS TERMINATED BY ',' -- Delimitador de campo no arquivo CSV, cada vírgula uma coluna.
ENCLOSED BY '"' -- Caractere de aspas que envolve valores de campo, permite que filmes com vírgula sejam adequadamente importados.
LINES TERMINATED BY '\n' -- Delimitador de linha no arquivo CSV, cada fim de linha, uma nova linha.
IGNORE 1 ROWS; -- Ignora a primeira linha (cabeçalho).

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/tags.csv'
INTO TABLE tags
FIELDS TERMINATED BY ',' -- Delimitador de campo no arquivo CSV, cada vírgula uma coluna.
ENCLOSED BY '"' -- Caractere de aspas que envolve valores de campo, permite que filmes com vírgula sejam adequadamente importados.
LINES TERMINATED BY '\n' -- Delimitador de linha no arquivo CSV, cada fim de linha, uma nova linha.
IGNORE 1 ROWS; -- Ignora a primeira linha (cabeçalho).

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/genome-tags.csv'
INTO TABLE genome_tags
FIELDS TERMINATED BY ',' -- Delimitador de campo no arquivo CSV, cada vírgula uma coluna.
ENCLOSED BY '"' -- Caractere de aspas que envolve valores de campo, permite que filmes com vírgula sejam adequadamente importados.
LINES TERMINATED BY '\n' -- Delimitador de linha no arquivo CSV, cada fim de linha, uma nova linha.
IGNORE 1 ROWS; -- Ignora a primeira linha (cabeçalho).

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/genome-scores.csv'
INTO TABLE genome_scores
FIELDS TERMINATED BY ',' -- Delimitador de campo no arquivo CSV, cada vírgula uma coluna.
ENCLOSED BY '"' -- Caractere de aspas que envolve valores de campo, permite que filmes com vírgula sejam adequadamente importados.
LINES TERMINATED BY '\n' -- Delimitador de linha no arquivo CSV, cada fim de linha, uma nova linha.
IGNORE 1 ROWS; -- Ignora a primeira linha (cabeçalho).

-- select * from movies;
