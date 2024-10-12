-- Country table
CREATE TABLE Country (
    countryCode CHAR(3) NOT NULL PRIMARY KEY,
    name VARCHAR(56)
);

-- Athlete table
CREATE TABLE Athlete (
    athleteID CHAR(7) NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    birthdate DATE,
    gender CHAR(1) NOT NULL,
    countryCode CHAR(3) NOT NULL,
    FOREIGN KEY (countryCode) REFERENCES Country(countryCode)
);

-- Medallist table
CREATE TABLE Medallist (
    athleteID CHAR(7) NOT NULL PRIMARY KEY,
    numMedals INT NOT NULL CHECK (numMedals >= 1),
    numGold INT,
    numSilver INT,
    numBronze INT,
    FOREIGN KEY (athleteID) REFERENCES Athlete(athleteID)
);

-- Sport table
CREATE TABLE Sport (
    sportID CHAR(3) NOT NULL PRIMARY KEY,
    name VARCHAR(21)
);

-- Venue table
CREATE TABLE Venue (
    venueID CHAR(4) NOT NULL PRIMARY KEY,
    name VARCHAR(50),
    capacity INT
);

-- Event table
CREATE TABLE Events (
    eventID VARCHAR(16) NOT NULL PRIMARY KEY,
    name VARCHAR(50),
    date DATETIME,
    sportID CHAR(3),
    venueID CHAR(4),
    FOREIGN KEY (sportID) REFERENCES Sport(sportID),
    FOREIGN KEY (venueID) REFERENCES Venue(venueID)
);

-- competesIn table
CREATE TABLE CompetesIn (
    athleteID CHAR(7) NOT NULL,
    eventID VARCHAR(16) NOT NULL,
    athleteRank CHAR(1) NOT NULL,
    PRIMARY KEY (athleteID, eventID),
    FOREIGN KEY (athleteID) REFERENCES Athlete(athleteID) ON DELETE CASCADE,
    FOREIGN KEY (eventID) REFERENCES Events(eventID) ON DELETE CASCADE
);