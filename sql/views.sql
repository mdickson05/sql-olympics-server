-- View 1: Athlete Ranks
-- Will contain the id, athleteName, country, and their medal counts for every athlete in Athlete table
DROP VIEW IF EXISTS AthleteRankings;
CREATE VIEW AthleteRankings AS
SELECT 
    a.athleteID as id,
    a.name AS athleteName,
    c.name AS country,
    IFNULL(m.numGold, 0) AS goldMedals,
    IFNULL(m.numSilver, 0) AS silverMedals,
    IFNULL(m.numBronze, 0) AS bronzeMedals,
    IFNULL(m.numMedals, 0) AS totalMedals
FROM Athlete a
LEFT JOIN Medallist m ON a.athleteID = m.athleteID
JOIN Country c ON a.countryCode = c.countryCode
ORDER BY totalMedals DESC;

-- View 2: Event Performance and Statistics
-- For each event, will contain various event related statistics (ID, name, venue, sport, average age + number of participants)
-- As well as various results (winner name, winner's country, top three countries for the event)
DROP VIEW IF EXISTS EventPerformanceStats;
CREATE VIEW EventPerformanceStats AS
SELECT 
    e.eventID,
    e.name AS eventName,
    s.name AS sportName,
    v.name AS venueName,
    COUNT(DISTINCT ci.athleteID) AS numberOfParticipants,
    AVG(TIMESTAMPDIFF(YEAR, a.birthdate, e.date)) AS avgAthleteAge,
    -- Subquery to find event winner
    (SELECT a1.name 
     FROM Athlete a1 
     JOIN CompetesIn ci1 ON a1.athleteID = ci1.athleteID 
     WHERE ci1.eventID = e.eventID AND ci1.athleteRank = '1' 
     LIMIT 1) AS eventWinner,
     
    -- Subquery to find winning country name
    (SELECT c1.name 
     FROM Country c1 
     JOIN Athlete a1 ON c1.countryCode = a1.countryCode 
     JOIN CompetesIn ci1 ON a1.athleteID = ci1.athleteID 
     WHERE ci1.eventID = e.eventID AND ci1.athleteRank = '1' 
     LIMIT 1) AS winningCountry,

    -- Subquery to find topThree countries
    (SELECT GROUP_CONCAT(c2.name ORDER BY c2.name SEPARATOR ', ')
     FROM Country c2
     JOIN Athlete a2 ON c2.countryCode = a2.countryCode
     JOIN CompetesIn ci2 ON a2.athleteID = ci2.athleteID
     WHERE ci2.eventID = e.eventID AND ci2.athleteRank IN ('1', '2', '3')) AS topThreeCountries

FROM Events e
JOIN Sport s ON e.sportID = s.sportID
JOIN Venue v ON e.venueID = v.venueID
LEFT JOIN CompetesIn ci ON e.eventID = ci.eventID
LEFT JOIN Athlete a ON ci.athleteID = a.athleteID
GROUP BY e.eventID, e.name, s.name, v.name
ORDER BY e.date, numberOfParticipants DESC;

-- Select name and number of medals of Australian athletes who won a medal from AthleteRankings
SELECT 
    athleteName, 
    totalMedals 
FROM AthleteRankings 
WHERE country LIKE 'Australia' AND totalMedals > 0;

-- Select the event name, average athlete age, event winners, and the top countries...
SELECT 
    eventName,
    avgAthleteAge,
    eventWinner, 
    topThreeCountries 
-- ... from the new view where the number of participants is 8, and the sport is swimming
FROM EventPerformanceStats 
WHERE numberOfParticipants = 8 AND sportName LIKE 'Swimming';