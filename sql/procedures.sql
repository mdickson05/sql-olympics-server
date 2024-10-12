-- Stored Procedure 1: Get Athlete Performance Summary
-- Given an athlete ID, this procedure will show total events, their best rank, and their medal distribution (if any)
DROP PROCEDURE IF EXISTS GetAthletePerformanceSummary;
DELIMITER //
CREATE PROCEDURE GetAthletePerformanceSummary(
    IN p_athleteID CHAR(7)
)
BEGIN
    DECLARE totalEvents INT;
    DECLARE bestRank CHAR(1);
    
    -- Get total number of events
    SELECT COUNT(*) INTO totalEvents
    FROM CompetesIn
    WHERE athleteID = p_athleteID;
    
    -- Get best rank
    SELECT MIN(athleteRank) INTO bestRank
    FROM CompetesIn
    WHERE athleteID = p_athleteID;
    
    -- Output the summary
    SELECT 
        a.name, 
        c.name AS country,
        totalEvents AS eventsParticipated,
        bestRank,
        IFNULL(m.numGold, 0) AS goldMedals,
        IFNULL(m.numSilver, 0) AS silverMedals,
        IFNULL(m.numBronze, 0) AS bronzeMedals,
        IFNULL(m.numMedals, 0) AS totalMedals
    FROM Athlete a
    LEFT JOIN Medallist m ON a.athleteID = m.athleteID
    JOIN Country c ON a.countryCode = c.countryCode
    WHERE a.athleteID = p_athleteID;
END 
//
DELIMITER ;

-- Stored Procedure 2: AnalyseCountryPerformance
-- Given a country code, this procedure will show the name of the country, 
-- their total number of medals + distribution, as well as the average age of their participants
-- and and overall performance rating based on their medal count

DROP PROCEDURE IF EXISTS AnalyzeCountryPerformance;

DELIMITER //
CREATE PROCEDURE AnalyzeCountryPerformance(
    IN p_countryCode CHAR(3)
)
BEGIN
    -- Declarations
    DECLARE totalMedals INT DEFAULT 0;
    DECLARE goldMedals INT DEFAULT 0;
    DECLARE silverMedals INT DEFAULT 0;
    DECLARE bronzeMedals INT DEFAULT 0;
    DECLARE totalAthletes INT DEFAULT 0;
    DECLARE numMedalists INT DEFAULT 0;
    DECLARE avgAge DECIMAL(5,2);
    DECLARE performanceRating VARCHAR(20);

    -- Calculate total medals and counts
    SELECT 
        IFNULL(SUM(m.numMedals), 0),
        IFNULL(SUM(m.numGold), 0),
        IFNULL(SUM(m.numSilver), 0),
        IFNULL(SUM(m.numBronze), 0),
        COUNT(DISTINCT a.athleteID),
        COUNT(DISTINCT CASE WHEN m.numMedals > 0 THEN a.athleteID END),
        AVG(TIMESTAMPDIFF(YEAR, a.birthdate, '2024-07-26'))
    INTO
        totalMedals, goldMedals, silverMedals, bronzeMedals, 
        totalAthletes, numMedalists, avgAge
    FROM Athlete a
    LEFT JOIN Medallist m ON a.athleteID = m.athleteID
    WHERE a.countryCode = p_countryCode;

    -- Calculate performance rating
    IF totalMedals >= 10 AND goldMedals >= 5 THEN
        SET performanceRating = 'Excellent';
    ELSEIF totalMedals > 5 THEN
        SET performanceRating = 'Good';
    ELSEIF totalMedals > 0 THEN
        SET performanceRating = 'Average';
    ELSE
        SET performanceRating = 'Poor';
    END IF;

    -- Output country summary
    SELECT 
        c.name AS countryName, 
        totalMedals, 
        goldMedals, 
        silverMedals, 
        bronzeMedals,
        totalAthletes, 
        numMedalists, 
        ROUND(avgAge, 2) AS averageAge,
        performanceRating
    FROM Country c
    WHERE c.countryCode = p_countryCode;
END 
//
DELIMITER ;


-- Analyse Country Performance
CALL AnalyzeCountryPerformance('AUS');

-- Summarise the performance of Ariarne Titmus (1946150)
CALL GetAthletePerformanceSummary("1946150");