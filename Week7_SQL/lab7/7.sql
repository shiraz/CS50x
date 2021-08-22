/*
In 7.sql, write a SQL query that returns the average energy of songs that are by Drake.
    Your query should output a table with a single column and a single row containing the average energy.
    You should not make any assumptions about what Drake’s artist_id is.
*/
SELECT AVG(songs.energy) AS 'DRAKE SONGS AVERAGE ENERGY' FROM songs INNER JOIN artists ON songs.artist_id = artists.id WHERE artists.name = 'Drake';