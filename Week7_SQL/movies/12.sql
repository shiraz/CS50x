/*
In 12.sql, write a SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
    Your query should output a table with a single column for the title of each movie.
    You may assume that there is only one person in the database with the name Johnny Depp.
    You may assume that there is only one person in the database with the name Helena Bonham Carter.
*/

SELECT movies.title AS 'MOVIES STARRING JOHNNY DEPP & HELEN BONHAM CARTER'
FROM   (SELECT movie_id,
               COUNT(movie_id) AS movies_count
        FROM   stars
        WHERE  person_id IN (SELECT id FROM people WHERE name IN ('Johnny Depp', 'Helena Bonham Carter'))
        GROUP  BY movie_id) jd_hbc_movie_ids
       INNER JOIN movies
               ON movies.id = jd_hbc_movie_ids.movie_id
WHERE  movies_count = 2
ORDER  BY movies.title ASC;