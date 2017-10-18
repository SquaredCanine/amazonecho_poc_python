import mysql.connector
import os

username = os.environ('db_username')
location = os.environ('db_location')
name = os.environ('db_name')
port = os.environ('db_port')
password = os.environ('db_password')
global cnx, cursor
cnx = None
cursor = None


def initialize():
    global cnx, cursor
    cnx = mysql.connector.connect(user=username, password=password, port=port, host=location, database=name)
    cursor = cnx.cursor()


def add_journey():
    global cursor,cnx
    query = ("SELECT * FROM mydb.Journey")
    cursor.execute(query)
    for element in cursor:
        print(element)
    cnx.close()

