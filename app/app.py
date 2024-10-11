from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Creates connection to the specified database
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='db_21549225',
            user='me',
            password='myUserPassword'
        )
        return connection # if connection is successful, will return
    except Error as e:
        raise e  # Raise the error; upto functions to handle locally.

# Default landing page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/error')
def error_page():
    error_message = request.args.get('error', 'An unknown error occurred')
    return render_template('error.html', error_message=error_message)

# Athletes page
# I would like to fetch the athlete details using api routes 
# But that would make my website too complicated and out of scope
@app.route('/athletes')
def athletes():    
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True) # create new cursor that maps rows to columns, easier access
        cursor.execute("SELECT * FROM Athlete")
        athletes = cursor.fetchall() # fetches all rows
        return render_template('athletes.html', athletes=athletes)
    except Error as e: # any database errors will be caught and printed
        return redirect(url_for('error_page', error=str(e)))
    finally: # will run regardless of errors.
        if connection.is_connected():
            cursor.close()
            connection.close()

# Route to add a new athlete
# Uses two methods - GET to access webpage, POST to actually insert the values
@app.route('/add_athlete', methods=['GET', 'POST'])
def add_athlete():
    # IF the request is a GET request, will redirect to add_athlete page without issue
    if request.method == 'GET':
        return render_template('add_athlete.html') 
    # Otherwise, if we are trying to submit a request to add an athlete to the DB (i.e. a POST)
    else:
        # retrieve these variables from the JSON body
        athleteID = request.form['athleteID']
        name = request.form['name']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        countryCode = request.form['countryCode']
        # retrieve a connection
        try:
            connection = create_db_connection()
            cursor = connection.cursor() # cursor allows for parameterised input
            query = "INSERT INTO Athlete (athleteID, name, birthdate, gender, countryCode) VALUES (%s, %s, %s, %s, %s)"
            values = (athleteID, name, birthdate, gender, countryCode)
            cursor.execute(query, values) # executes the command via parameterised input - prevents SQL injection
            connection.commit() # SAVES the changes to the database
            return redirect(url_for('athletes')) # redirects to athletes table to see changes
        except Error as e: # any database errors will be caught
            return redirect(url_for('error_page', error=str(e)))
        finally: # will run regardless of errors.
            if connection.is_connected():
                cursor.close()
                connection.close()

# Route to update an athlete
@app.route('/update_athlete/<athleteID>', methods=['GET', 'POST'])
# double route methods for webpage retrieval (GET) and form submission (POST)
def update_athlete(athleteID):
    try:
        connection = create_db_connection() # tries to connect to the database
        cursor = connection.cursor(dictionary=True) # create new cursor that maps rows to columns, easier access
        if request.method == 'POST':
            # retrieve variables from JSON form
            name = request.form['name']
            birthdate = request.form['birthdate']
            gender = request.form['gender']
            countryCode = request.form['countryCode']
            
            # updates the values in the database using parameterised input
            query = "UPDATE Athlete SET name=%s, birthdate=%s, gender=%s, countryCode=%s WHERE athleteID=%s"
            values = (name, birthdate, gender, countryCode, athleteID)
            cursor.execute(query, values)
            connection.commit()
            # redirects back to table
            return redirect(url_for('athletes'))
        else:
            # fetch the athlete
            cursor.execute("SELECT * FROM Athlete WHERE athleteID=%s", (athleteID,))
            athlete = cursor.fetchone() # only fetch ONE athlete from the SELECT statement (should only be one as unique key)
            # render the update_athlete webpage
            return render_template('update_athlete.html', athlete=athlete)
    except Error as e:
        return redirect(url_for('error_page', error=str(e)))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    

# Route to delete an athlete
@app.route('/delete_athlete/<athleteID>')
def delete_athlete(athleteID):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Athlete WHERE athleteID=%s", (athleteID,))
        connection.commit()
        return redirect(url_for('athletes'))
    except Error as e:
        return redirect(url_for('error_page', error=str(e)))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# executes the query via supplied name
@app.route('/execute_query/<query_name>')
def execute_query(query_name):
    queries = {
        'athletes_born_after_2000': """
            SELECT name, birthdate 
            FROM Athlete
            WHERE birthdate >= '2000-01-01'
        """,
        'athletes_starting_with_a': """
            SELECT name, gender 
            FROM Athlete 
            WHERE name LIKE 'A%'
        """,
        'events_in_august': """
            SELECT name, date
            FROM Events
            WHERE date > '2024-08-01' AND date < '2024-08-31'
        """,
        'events_after_dinner': """
            SELECT name, date
            FROM Events
            WHERE TIME(date) > '17:00:00'
        """,
        'gold_medal_winners': """
            SELECT a.name, m.numMedals
            FROM Athlete a 
            JOIN Medallist m ON a.athleteID = m.athleteID
            WHERE m.numGold >= 1
        """,
        'num_athletes_per_event': """
            SELECT e.name, COUNT(ci.athleteID) AS numParticipants
            FROM Events e
            JOIN CompetesIn ci ON e.eventID = ci.eventID
            GROUP BY e.name
            ORDER BY numParticipants DESC
        """,
        'total_medals_by_country': """
            SELECT ci.name, ci.countryCode, 
                SUM(m.numGold) AS totalGold, 
                SUM(m.numSilver) AS totalSilver, 
                SUM(m.numBronze) AS totalBronze, 
                SUM(m.numMedals) AS totalMedals
            FROM Country ci
            JOIN Athlete a ON ci.countryCode = a.countryCode
            JOIN Medallist m ON a.athleteID = m.athleteID
            GROUP BY ci.name, ci.countryCode
            ORDER BY totalMedals DESC
        """,
        'oldest_swimmers': """
            SELECT a.name, 
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
        """,
        'events_with_diff_countries': """
            SELECT e.name AS eventName, 
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
        """,
        'most_events_swimmer': """
            SELECT a.name AS athlete_name, 
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
        """,
        'age_difference_events': """
            SELECT e.name AS eventName, 
                MAX(DATEDIFF(e.date, a.birthdate) / 365.25) - MIN(DATEDIFF(e.date, a.birthdate) / 365.25) AS age_difference
            FROM Events e
            JOIN CompetesIn ci ON e.eventID = ci.eventID
            JOIN Athlete a ON ci.athleteID = a.athleteID
            GROUP BY e.eventID, e.name
            HAVING age_difference > 10
            ORDER BY age_difference DESC;
        """
    }
    
    if query_name not in queries:
        return jsonify({'error': 'Query not found'}), 404
    
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries[query_name])
        results = cursor.fetchall()
        return jsonify(results)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# route for the query_execution page
@app.route('/query_execution')
def query_execution():
    return render_template('query_execution.html')
   

# test connection - made for testing whether the database was actually working
@app.route('/test_connection')
def test_connection():
    try:
        connection = create_db_connection()
        connection.close()
        return "Connection to the database was successful!"
    except Error:
        return "Failed to connect to the database"

if __name__ == '__main__':
    app.run(debug=True)