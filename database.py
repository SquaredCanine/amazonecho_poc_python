import mysql.connector

def test():
    cnx = mysql.connector.connect(user='REDACTED', password='REDACTED', port='REDACTED', host='REDACTED', database='REDACTED')
    cursor = cnx.cursor()
    query= ("SELECT * FROM mydb.Journey")
    cursor.execute(query)
    for element in cursor:
        print(element)
    cnx.close()


if __name__ == '__main__':
    test()
