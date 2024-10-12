-- Drop competesIn table first (child table)
DROP TABLE IF EXISTS CompetesIn;

-- Drop Medallist table next (child table)
DROP TABLE IF EXISTS Medallist;

-- Drop Events table (child table)
DROP TABLE IF EXISTS Events;

-- Drop Athlete table (parent table)
DROP TABLE IF EXISTS Athlete;

-- Drop Venue table (no dependencies)
DROP TABLE IF EXISTS Venue;

-- Drop Sport table (no dependencies)
DROP TABLE IF EXISTS Sport;

-- Drop Country table (no dependencies)
DROP TABLE IF EXISTS Country;