from flask import Flask, render_template
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
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Athlete")
            athletes = cursor.fetchall()
            return render_template('athletes.html', athletes=athletes)
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return "Error connecting to the database"

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