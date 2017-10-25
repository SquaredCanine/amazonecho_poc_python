import mysql.connector
import os

username = os.environ['db_username']
location = os.environ['db_location']
name = os.environ['db_name']
port = os.environ['db_port']
password = os.environ['db_password']
global cnx, cursor
cnx = None
cursor = None


def initialize():
    global cnx, cursor
    cnx = mysql.connector.connect(user=username, password=password, port=port, host=location, database=name)
    cursor = cnx.cursor()


def get_journey_identifier(UID):
    initialize()
    global cursor, cnx
    query = "SELECT max(identifier) FROM Journey WHERE UID = %s"
    cursor.execute(query, (UID, ))
    for element in cursor:
        print(element[0])
    cnx.close
    return element[0]


def add_journey(selectedjourney, UID, selectedclass):
    initialize()
    global cursor, cnx
    origincode = selectedjourney['origin']['code']
    destinationcode = selectedjourney['destination']['code']
    departuretime = selectedjourney['origin']['departure']['planned'].split()[1].replace(':', '')
    departuredate = selectedjourney['origin']['departure']['planned'].split()[0].replace('-', '')
    orderprice = selectedjourney['offers'][selectedclass]['salesPrice']['amount']
    identifier = get_journey_identifier(UID)
    identifier += 1
    query = "INSERT INTO Journey (UID, identifier, originCode, destinationCode, departuretime, departuredate,orderprice) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (UID, identifier, origincode, destinationcode, departuretime, departuredate, orderprice))
    cnx.commit()
    cnx.close()


def get_user_email(uid):
    initialize()
    global cursor, cnx
    query = "SELECT email FROM Users WHERE UID= %s"
    cursor.execute(query, (uid, ))
    for element in cursor:
        return element[0]
    cnx.close()
    return False
