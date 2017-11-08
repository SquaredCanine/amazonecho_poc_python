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


def get_journey_identifier(uid):
    initialize()
    global cursor, cnx
    query = "SELECT max(identifier) FROM Journey WHERE UID = %s"
    cursor.execute(query, (uid,))
    for element in cursor:
        return element[0] + 1
    return 1


def add_journey(selectedjourney, UID, selectedclass):
    initialize()
    global cursor, cnx
    origincode = selectedjourney['origin']['code']
    destinationcode = selectedjourney['destination']['code']
    departuretime = selectedjourney['origin']['departure']['planned'].split()[1].replace(':', '')
    departuredate = selectedjourney['origin']['departure']['planned'].split()[0].replace('-', '')
    orderprice = selectedjourney['offers'][selectedclass]['salesPrice']['amount']
    identifier = get_journey_identifier(UID)
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


def add_user(uid, name, email):
    initialize()
    global cursor, cnx
    query = 'INSERT INTO Users (UID, name, email) VALUES (%s, %s, %s)'
    cursor.execute(query, (uid, name, email))
    cnx.commit()
    cnx.close()


def add_composition(uid, number_of_passengers):
    remove_composition(uid)
    global cnx, cursor
    initialize()
    query = "INSERT INTO Composition (UID, numberOfPassengers) VALUES (%s, %s)"
    cursor.execute(query, (uid, number_of_passengers))
    cnx.commit()
    cnx.close()


def remove_composition(uid):
    global cnx, cursor
    initialize()
    query = "DELETE FROM Composition WHERE UID = %s"
    cursor.execute(query, (uid, ))
    cnx.commit()
    cnx.close()


def get_composition(uid):
    global cnx, cursor
    initialize()
    query = 'SELECT numberOfPassengers FROM Composition WHERE UID= %s'
    cursor.execute(query, (uid, ))
    for element in cursor:
        return element[0]
    return 1
