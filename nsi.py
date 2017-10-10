import requests

base_url = 'https://www.nsinternational.nl/api/v1.1/'
price_and_time_request_url = 'connections/'
stationname_request_url = 'stations/'


def get_price_and_time_response(origincode, destinationcode, date, time, amount_of_passengers, juncture):
    passengers = 'passengers='
    timetype = '&timetype=' + juncture

    for x in range(0, amount_of_passengers):
        passengers += 'A,'

    response = requests.get(base_url +
                            price_and_time_request_url +
                            origincode + '/' +
                            destinationcode + '/' +
                            date + '/' +
                            time + '/' +
                            '/outbound?' +
                            passengers +
                            timetype)
    return response.json()


def get_stationname_response(name):
    name = '?name=' + name

    response = requests.get(base_url + stationname_request_url + name)
    return response.json()
