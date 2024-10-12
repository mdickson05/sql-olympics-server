-- Show the name of all athletes and their corresponding birthdates of all athletes born in or after 2000.
-- NOTE: > in MySQL is >= for date time comparisons
SELECT 
    name, 
    birthdate 
FROM Athlete
WHERE birthdate > '2000-01-01';

-- Select all athletes whose name starts with the letter A
SELECT 
    name, 
    gender 
FROM Athlete 
WHERE name LIKE 'A%';

-- SELECT all events which occured in August
SELECT 
    name, 
    date
FROM Events
WHERE date > '2024-08-01' AND date < '2024-08-31';

-- SELECT all events which occured after dinner has started being served at the Olympic village (5pm)
SELECT 
    name, 
    date
FROM Events
WHERE TIME(date) > '17:00:00';

-- Select the name and the total number of medals of Medallists who won at least one gold medal
SELECT
    a.name, 
    m.numMedals
FROM Athlete a 
JOIN Medallist m ON a.athleteID = m.athleteID
WHERE m.numGold >= 1;

-- Show the number of athletes competing in each event, and order it by number of participants descending
SELECT 
    e.name, 
    COUNT(ci.athleteID) AS numParticipants
FROM Events e
JOIN CompetesIn ci ON e.eventID = ci.eventID
GROUP BY e.name
ORDER BY numParticipants DESC;

-- Show the total number of medals won for each country, with country name and code shown.
SELECT 
    ci.name, 
    ci.countryCode, 
    SUM(m.numGold) AS totalGold, 
    SUM(m.numSilver) AS totalSilver, 
    SUM(m.numBronze) AS totalBronze, 
    SUM(m.numMedals) AS totalMedals
FROM Country ci
JOIN Athlete a ON ci.countryCode = a.countryCode
JOIN Medallist m ON a.athleteID = m.athleteID -- TWO join statements as we need to connect Country with Medallist
GROUP BY ci.name, ci.countryCode
ORDER BY totalMedals DESC;

-- Select the three oldest swimmers, their birthdate age, and the events they are in
SELECT 
    a.name, 
    a.birthdate, 
    TIMESTAMPDIFF(YEAR, a.birthdate, CURDATE()) AS age,
    GROUP_CONCAT(e.name SEPARATOR ', ') as Events
FROM Athlete a
JOIN CompetesIn ci ON a.athleteID = ci.athleteID
JOIN Events e ON ci.eventID = e.eventID
WHERE e.sportID = 'SWM'
GROUP BY a.athleteID
ORDER BY a.birthdate ASC
LIMIT 3;

-- List all events where the gold medalist is from a different country than the silver medalist
SELECT 
    e.name AS eventName, 
    gold.countryName AS goldMedallistCountry, 
    silver.countryName AS silverMedallistCountry
FROM Events e
JOIN (
    SELECT ci.eventID, c.name AS countryName
    FROM CompetesIn ci
    JOIN Athlete a ON ci.athleteID = a.athleteID
    JOIN Country c ON a.countryCode = c.countryCode
    WHERE ci.athleteRank = '1'
) gold ON e.eventID = gold.eventID
JOIN (
    SELECT ci.eventID, c.name AS countryName
    FROM CompetesIn ci
    JOIN Athlete a ON ci.athleteID = a.athleteID
    JOIN Country c ON a.countryCode = c.countryCode
    WHERE ci.athleteRank = '2'
) silver ON e.eventID = silver.eventID
WHERE gold.countryName != silver.countryName;

-- Find the swimmer(s) who has participated in the most events
SELECT 
    a.name AS athlete_name, 
    COUNT(ci.eventID) AS numEvents
FROM Athlete a
JOIN CompetesIn ci ON a.athleteID = ci.athleteID
GROUP BY a.athleteID, a.name
HAVING numEvents = (
    SELECT COUNT(eventID)
    FROM CompetesIn
    GROUP BY athleteID
    ORDER BY COUNT(eventID) DESC
    LIMIT 1
);

-- Find the events where the difference in age between the youngest and oldest competitor is more than 10 years
SELECT 
    e.name AS eventName, 
    MAX(DATEDIFF(e.date, a.birthdate) / 365.25) - MIN(DATEDIFF(e.date, a.birthdate) / 365.25) AS age_difference
FROM Events e
JOIN CompetesIn ci ON e.eventID = ci.eventID
JOIN Athlete a ON ci.athleteID = a.athleteID
GROUP BY e.eventID, e.name
HAVING age_difference > 10
ORDER BY age_difference DESC;
