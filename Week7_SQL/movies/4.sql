/*
In 4.sql, write a SQL query to determine the number of movies with an IMDb rating of 10.0.
    Your query should output a table with a single column and a single row (not including the header) containing the number of movies with a 10.0 rating.
*/

SELECT COUNT(movies.title) AS 'TOTAL NUMBER OF MOVIES WITH 10.0 RATING'
FROM   movies
       INNER JOIN ratings
               ON movies.id = ratings.movie_id
WHERE  ratings.rating = 10.0;