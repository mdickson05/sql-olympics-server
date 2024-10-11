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
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# default landing page  
@app.route('/')
def home():
    return render_template('index.html')

# test connection via api route
@app.route('/api/test_connection')
def test_connection():
    connection = create_db_connection()
    if connection is not None and connection.is_connected():
        connection.close()  # Close the connection
        return "Connection to the database was successful!"
    else:
        return "Failed to connect to the database. Check terminal for error code."

if __name__ == '__main__':
    app.run(debug=True)