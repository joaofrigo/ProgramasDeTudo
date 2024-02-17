SELECT * FROM movie_ratings ORDER BY id DESC LIMIT 1;

DELETE FROM movie_ratings
WHERE id = '3';

SELECT * FROM movie_ratings WHERE id != 1;
SELECT * FROM movie_ratings

UPDATE movie_ratings
SET averageRating = 20, numVotes = 40
WHERE id = '1';
