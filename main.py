#!/usr/bin/env python3
import psycopg2
from flask import Flask, render_template


def db_connect():
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
        print('Database connection opened.')
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def db_close(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed.')


app = Flask(__name__)


@app.route("/")
def get_records():
    # SQL to get records from Postgres
    s = "SELECT * FROM swtypes"

    conn = db_connect()
    cursor = conn.cursor()

    # Error trapping
    try:
        # Execute the SQL
        cursor.execute(s)
        # Retrieve records from Postgres into a Python List
        results = cursor.fetchall()
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("error.html", t_message = t_message)

    # Loop through the resulting list and print each user name, along with a line break:
#    for i in range(len(results)):
#        print('TYPES: ' + str(results[i]))

    # Close the database cursor and connection
    cursor.close()
    db_close(conn)

    return render_template('index.html', results=results)

def index():
    pass
#    return render_template('index.html')