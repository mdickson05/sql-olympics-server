from flask import Flask, render_template, request, redirect, url_for
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
        print(f"Error connecting to MySQL database: {e}") # will log errors to the console
        return None

# Default landing page
@app.route('/')
def home():
    return render_template('index.html')

# Athletes page
# I would like to fetch the athlete details using api routes 
# But that would make my website too complicated and out of scope
@app.route('/athletes')
def athletes():
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True) # create new cursor that maps rows to columns, easier access
            cursor.execute("SELECT * FROM Athlete")
            athletes = cursor.fetchall() # fetches all rows
            return render_template('athletes.html', athletes=athletes)
        except Error as e: # any database errors will be caught and printed
            print(f"Error: {e}")
        finally: # will run regardless of errors.
            if connection.is_connected():
                cursor.close()
                connection.close()
    return "Error connecting to the database"

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
        connection = create_db_connection()

        if not connection: # if connection fails
            return "Error connecting to the database"
        else:
            try:
                cursor = connection.cursor() # cursor allows for parameterised input
                query = "INSERT INTO Athlete (athleteID, name, birthdate, gender, countryCode) VALUES (%s, %s, %s, %s, %s)"
                values = (athleteID, name, birthdate, gender, countryCode)
                cursor.execute(query, values) # executes the command via parameterised input - prevents SQL injection
                connection.commit() # SAVES the changes to the database
                return redirect(url_for('athletes')) # redirects to athletes table to see changes
            except Error as e: # any database errors will be caught and printed
                print(f"Error: {e}")
            finally: # will run regardless of errors.
                if connection.is_connected():
                    cursor.close()
                    connection.close()

# Route to update an athlete
@app.route('/update_athlete/<athleteID>', methods=['GET', 'POST'])
# double route methods for webpage retrieval (GET) and form submission (POST)
def update_athlete(athleteID):
    connection = create_db_connection() # tries to connect to the database
    if not connection: # if not successful...
        return "Error connecting to the database"
    else:
        try:
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
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    

# Route to delete an athlete
@app.route('/delete_athlete/<athleteID>')
def delete_athlete(athleteID):
    connection = create_db_connection()
    if not connection:
        return "Error connecting to the database"
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Athlete WHERE athleteID=%s", (athleteID,))
            connection.commit()
            return redirect(url_for('athletes'))
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
   

# test connection - made for testing whether the database was actually working
@app.route('/test_connection')
def test_connection():
    connection = create_db_connection()
    if connection is not None and connection.is_connected():
        connection.close()  # Close the connection
        return "Connection to the database was successful!"
    else:
        return "Failed to connect to the database. Check terminal for error code."

if __name__ == '__main__':
    app.run(debug=True)