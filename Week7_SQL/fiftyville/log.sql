-- Keep a log of any SQL queries you execute as you solve the mystery.

/*
Identify:
    1. Who the thief is?
    2. Where the thief escaped to (other than fiftyville)?
    3. Who the thief's accomplice was who helped them escape town?
*/

-- Theft took place on July 28.
-- Theft took place on Chamberlin Street.
SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Chamberlin Street';

/*
Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.
*/
SELECT * FROM courthouse_security_logs WHERE hour = 10 AND minute = 15 AND day = 28 AND month = 7;
SELECT * from interviews WHERE transcript LIKE '%courthouse%';

/*
161 | Ruth | 2020 | 7 | 28 | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away.
If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
*/
SELECT * from courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = 'exit';
/*
id | year | month | day | hour | minute | activity | license_plate
260 | 2020 | 7 | 28 | 10 | 16 | exit | 5P2BI95
261 | 2020 | 7 | 28 | 10 | 18 | exit | 94KL13X
262 | 2020 | 7 | 28 | 10 | 18 | exit | 6P58WS2
263 | 2020 | 7 | 28 | 10 | 19 | exit | 4328GD8
264 | 2020 | 7 | 28 | 10 | 20 | exit | G412CB7
265 | 2020 | 7 | 28 | 10 | 21 | exit | L93JTIZ
266 | 2020 | 7 | 28 | 10 | 23 | exit | 322W7JE
267 | 2020 | 7 | 28 | 10 | 23 | exit | 0NTHK55
*/

SELECT name FROM people WHERE license_plate IN (SELECT license_plate from courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = 'exit') ORDER BY name;
/*
Initial suspect list:
Amber
Danielle
Elizabeth
Ernest
Evelyn
Patrick
Roger
Russell
*/

/*
162 | Eugene | 2020 | 7 | 28 | I don't know the thief's name, but it was someone I recognized.
Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
*/
SELECT * FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Fifer Street' AND transaction_type = 'withdraw';
/*
id | account_number | year | month | day | atm_location | transaction_type | amount
246 | 28500762 | 2020 | 7 | 28 | Fifer Street | withdraw | 48
264 | 28296815 | 2020 | 7 | 28 | Fifer Street | withdraw | 20
266 | 76054385 | 2020 | 7 | 28 | Fifer Street | withdraw | 60
267 | 49610011 | 2020 | 7 | 28 | Fifer Street | withdraw | 50
269 | 16153065 | 2020 | 7 | 28 | Fifer Street | withdraw | 80
288 | 25506511 | 2020 | 7 | 28 | Fifer Street | withdraw | 20
313 | 81061156 | 2020 | 7 | 28 | Fifer Street | withdraw | 30
336 | 26013199 | 2020 | 7 | 28 | Fifer Street | withdraw | 35
*/

SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Fifer Street' AND transaction_type = 'withdraw')) ORDER BY name;
/*
New suspect list:
Bobby
Danielle
Elizabeth
Ernest
Madison
Roy
Russell
Victoria
*/

/*
163 | Raymond | 2020 | 7 | 28 | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute.
In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
The thief then asked the person on the other end of the phone to purchase the flight ticket.
*/
SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60;
/*
id | caller | receiver | year | month | day | duration
221 | (130) 555-0289 | (996) 555-8899 | 2020 | 7 | 28 | 51
224 | (499) 555-9472 | (892) 555-8872 | 2020 | 7 | 28 | 36
233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
251 | (499) 555-9472 | (717) 555-1342 | 2020 | 7 | 28 | 50
254 | (286) 555-6063 | (676) 555-6554 | 2020 | 7 | 28 | 43
255 | (770) 555-1861 | (725) 555-3243 | 2020 | 7 | 28 | 49
261 | (031) 555-6622 | (910) 555-3251 | 2020 | 7 | 28 | 38
279 | (826) 555-1652 | (066) 555-9701 | 2020 | 7 | 28 | 55
281 | (338) 555-6650 | (704) 555-2131 | 2020 | 7 | 28 | 54
*/

SELECT * FROM flights WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = 'Fiftyville') AND day = 29 AND month = 7 AND hour < 12 ORDER BY hour ASC LIMIT 1;
/*
id | origin_airport_id | destination_airport_id | year | month | day | hour | minute
36 | 8 | 4 | 2020 | 7 | 29 | 8 | 20
*/

SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = 'Fiftyville') AND day = 29 AND month = 7 AND hour < 12 ORDER BY hour ASC LIMIT 1));
/*
Current suspect list:
Bobby
Danielle
Doris
Edward
Ernest
Evelyn
Madison
Roger
*/

SELECT name FROM people
WHERE license_plate IN (SELECT license_plate from courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = 'exit')
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Fifer Street' AND transaction_type = 'withdraw'))
AND phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60)
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = 'Fiftyville') AND day = 29 AND month = 7 AND hour < 12 ORDER BY hour ASC LIMIT 1));
/*
Current Suspect List:
Ernest
*/

SELECT city FROM airports WHERE id in (SELECT destination_airport_id FROM flights WHERE origin_airport_id IN (SELECT id FROM airports WHERE city = 'Fiftyville') AND day = 29 AND month = 7 AND hour < 12 ORDER BY hour ASC LIMIT 1);
/*
Where the thief escaped to (other than fiftyville)?
London
*/

SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60 AND caller IN (SELECT phone_number FROM people WHERE name = 'Ernest'));
/*
Who the thief's accomplice was who helped them escape town?
Berthold
*/