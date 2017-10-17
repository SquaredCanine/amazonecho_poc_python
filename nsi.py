import requests

base_url = 'https://www.nsinternational.nl/api/v1.1/'
price_and_time_request_url = 'connections/'
stationname_request_url = 'stations/'
provisional_booking_request_url = 'bookings/provision'


def get_price_and_time_response(origincode, destinationcode, date, time, amount_of_passengers, juncture):
    passengers = 'passengers='
    timetype = 'timetype=' + juncture + ''

    passengers += 'A,' * amount_of_passengers
    full_url = '{0}{1}{2}/{3}/{4}/{5}/outbound?{6}&{7}'.format(base_url, price_and_time_request_url, origincode,
                                                               destinationcode, date, time, passengers, timetype)
    print(full_url)
    response = requests.get(full_url)
    return response.json()


def get_stationname_response(name):
    name = '?name=' + name

    response = requests.get(base_url + stationname_request_url + name)
    return response.json()


def provisional_booking_request(uid, selectedjourney, selectedclass, amount_of_passengers):
    userid = uid
    connectionid = selectedjourney['id']
    offerid = selectedjourney['offers'][selectedclass]['id']
    seatreservation = 'true'
    origincode = selectedjourney['origin']['code']
    destinationcode = selectedjourney['destination']['code']
    passengers = 'passengers='
    passengers += 'A,' * amount_of_passengers
    body = {'outbound': {
        'connectionId': connectionid,
        'offerId': offerid,
        'seatReservation': seatreservation
    },
        'passengers': passengers
    }
    full_url = provisional_booking_request_url + userid + '?origin=' + origincode + '&destination=' + destinationcode \
               + '&lang=nl '
    response = requests.post(full_url, body)
    return response.json()
