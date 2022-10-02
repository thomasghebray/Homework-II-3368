#Thomas Ghebray
# CIS 3368 
# Homework 2
from multiprocessing import connection
import flask
from flask import jsonify
from flask import request
from sql import create_connection, execute_query
from sql import execute_read_query
import creds

import mysql.connector
from mysql.connector import Error

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser





# this is how I will be establishing my sql connection
def create_con(hostname, username, userpw, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = username,
            password = userpw,
            database = dbname
        )
        print("\nHello all, welcome to Johnny Dang's Jewlery !")


        # If error found, I would like to print this message
    except Error as e:
        print(f'the error {e} occured')

    return connection




@app.route('/', methods=['GET'])
def home():
    return "<h1> Welcome To My Semi-Functional API! </H1>"




def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")



# Creating connection with my specific destination 

conn = create_con('cis3368fall.csskiywpvfqh.us-east-2.rds.amazonaws.com', 'admin', 'houston713', 'cis3368db')
cursor = conn.cursor(dictionary=True)


# How to retrieve the data using GET

@app.route('/api/gem', methods=['GET'])
def get_gem():
    sql = "SELECT * FROM gem"
    val = []
    users = execute_read_query(conn, sql)
    return users




# PUT
@app.route('/api/gem', methods=['PUT'])
def put_gem():
    # id = int(request.args['id'])
    request_data = request.get_json()
    newtype = request_data['gemtype']
    newcolor = request_data['gemcolor']
    newcarat = request_data['carat']
    newprice = request_data['price']
    sql = 'UPDATE gem SET gemtype = "%s", gemcolor = "%s", carat = "%s", price = "%s" WHERE gemtype = "%s"'
    val = (newtype, newcolor, newcarat, newprice, newtype)
    # This creates my connection
    connection_1 = conn.cursor()
    connection_1.executemany(sql, val)
    conn.commit()
    return "updated sucessfully"

# POST
@app.route('/api/gem', methods=['POST'])
def post_gem():
    request_data = request.get_json()
    newtype = request_data['gemtype']
    newcolor = request_data['gemcolor']
    newcarat = request_data['carat']
    newprice = request_data['price']
    sql = "INSERT INTO gem(gemtype, gemcolor, carat, price) VALUES (%s, %s, %s, %s)" 
    val = [(newtype, newcolor, newcarat, newprice)]
    # execute_query(conn, sql)
    connection_1 = conn.cursor()
    connection_1.executemany(sql, val)
    conn.commit()
    return "added sucessfully"




# DELETE
@app.route('/api/gem', methods=['DELETE'])
def delete_gem():
    request_data = request.get_json()
    id = request_data['id']
    # newtype = request_data['gemtype']
    sql = "DELETE FROM gem WHERE id = '%s'" 
    val = [int(id)]
    # execute_query(conn, sql)
    connection_1 = conn.cursor()
    connection_1.executemany(sql, val)
    conn.commit()
    return "Deleted gem successful"

app.run()


