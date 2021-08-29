/*
In 8.sql, write a SQL query to list the names of all people who starred in Toy Story.
    Your query should output a table with a single column for the name of each person.
    You may assume that there is only one movie in the database with the title Toy Story.
*/

SELECT people.name AS 'TOY STORY CAST'
FROM   people
       INNER JOIN stars
               ON people.id = stars.person_id
       INNER JOIN movies
               ON movies.id = stars.movie_id
WHERE  movies.title = 'Toy Story';