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


if __name__ == '__main__':
    journey = {
      "id" : "6cd3a6e2e64dc4e9422502550d4a8ff7c6dfd56a0a7fc51b9f2e7969eae92415",
      "status" : "bookable",
      "origin" : {
        "name" : "Amsterdam Centraal",
        "alias" : '',
        "country" : "NL",
        "code" : "NLASC",
        "arrival" : '',
        "departure" : {
          "planned" : "2017-10-23 16:17",
          "delay" : 0,
          "platform" : '',
          "updatedPlatform" : ''
        }
      },
      "destination" : {
        "name" : "Paris Nord",
        "alias" : "Parijs Centraal",
        "country" : "FR",
        "code" : "FRPNO",
        "arrival" : {
          "planned" : "2017-10-23 19:35",
          "delay" : 0,
          "platform" : '',
          "updatedPlatform" : ''
        },
        "departure" : ''
      },
      "duration" : {
        "days" : 0,
        "hours" : 3,
        "minutes" : 18,
        "delay" : 'false'
      },
      "transfers" : 0,
      "modalities" : [ {
        "type" : "train",
        "name" : "Thalys",
        "code" : "THA",
        "number" : "9370",
        "facilities" : [ {
          "name" : "Reserveren verplicht",
          "code" : "RP"
        }, {
          "name" : "vervoer fiets niet mogelijk",
          "code" : "NF"
        }, {
          "name" : "Speciale tarieven",
          "code" : "GP"
        }, {
          "name" : "barrijtuig",
          "code" : "BW"
        }, {
          "name" : "heeft een coupé voor minder validen",
          "code" : "97"
        } ]
      } ],
      "messages" : [ ],
      "bndsCode" : "bookable",
      "offers" : [ {
        "id" : "2_MF_201710231617_696bd82f3c534c6ea7e94269d680aaa1defadd531484dcbb1a2ec439c0c713f0",
        "name" : "Second Class",
        "comfortClass" : "2",
        "availability" : 1,
        "salesPrice" : {
          "currency" : "EUR",
          "amount" : "270.00",
          "passenger" : {
            "ageType" : "A",
            "amount" : "135.00"
          },
          "ticket" : {
            "amount" : "270.00",
            "count" : '',
            "passenger" : {
              "ageType" : "A",
              "amount" : "135.00"
            }
          },
          "reservation" : ''
        },
        "tariff" : {
          "returnType" : '',
          "premierClass" : ''
        },
        "benefits" : [ ]
      }, {
        "id" : "1_XX_e654c6c9-1179-49f3-846c-cacf0f5337d6",
        "name" : "Comfort Class",
        "comfortClass" : "1",
        "availability" : -1,
        "salesPrice" : '',
        "tariff" : '',
        "benefits" : ''
      } ]
    }
    selectedclass = 0
    UID = 'test'
    add_journey(journey,UID,selectedclass)