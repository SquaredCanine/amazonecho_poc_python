import requests

base_url = 'https://www.nsinternational.nl/api/v1.1/'
price_and_time_request_url = 'connections/'
stationname_request_url = 'stations/'
provisional_booking_request_url = 'bookings/provision/'
alternative_booking_request_url = 'bookings/alternative/'
calendar_date_request_url = 'calendardates/'
calendar_price_request_url = 'calendarprices/'


def get_price_and_time_response(origin, destination, date, time, amount_of_passengers, juncture):
    passengers = 'passengers='
    timetype = 'timetype=' + juncture + ''

    origincode = get_station_name_response(origin)
    destinationcode = get_station_name_response(destination)
    passengers += 'A,' * amount_of_passengers
    full_url = '{0}{1}{2}/{3}/{4}/{5}/outbound?{6}&{7}'.format(base_url, price_and_time_request_url, origincode,
                                                               destinationcode, date, time, passengers, timetype)
    response = requests.get(full_url)
    if response.json()['data']['connections']:
        return response.json()
    else:
        return False


def get_station_name_response(name):
    name = '?name=' + name

    response = requests.get(base_url + stationname_request_url + name)
    try:
        if response.json()['data']['stations'][0]['code']:
            stationcode = response.json()['data']['stations'][0]['code']
            for element in response.json()['data']['stations']:
                if element['type'] == 'top-destination':
                    stationcode = element['code']
            return stationcode
        else:
            return False
    except IndexError:
        return False


def provisional_booking_request(uid, selectedjourney, selectedclass, amount_of_passengers):
    userid = uid
    connectionid = selectedjourney['id']
    offerid = selectedjourney['offers'][selectedclass]['id']
    seatreservation = 'true'
    origincode = selectedjourney['origin']['code']
    destinationcode = selectedjourney['destination']['code']
    passengers = ''
    passengers += 'A,' * amount_of_passengers
    body = {"outbound": {
        "connectionId": connectionid,
        "offerId": offerid,
        "seatReservation": seatreservation
    },
        "passengers": passengers
    }
    full_url = base_url + provisional_booking_request_url + userid + '?origin=' + origincode + '&destination=' + destinationcode \
               + '&lang=nl'
    alternate_url = base_url + alternative_booking_request_url + userid + '?origin=' + origincode + '&destination=' + destinationcode \
               + '&lang=nl'
    response = requests.post(full_url, json={"outbound": {
        "connectionId": connectionid,
        "offerId": offerid,
        "seatReservation": seatreservation
    },
        "passengers": passengers
    })
    if response:
        return response.json()
    else:
        response = requests.post(alternate_url, body)
        return response.json()


def get_calendar_date_response(origin, destination):
    origincode = get_station_name_response(origin)
    destinationcode = get_station_name_response(destination)

    full_url = '{0}{1}{2}/{3}/outbound?lang=nl'.format(base_url, calendar_date_request_url, origincode, destinationcode)
    response = requests.get(full_url)
    return response.json()


def get_calendar_price_response(origin, destination):
    origincode = get_station_name_response(origin)
    destinationcode = get_station_name_response(destination)

    full_url = '{0}{1}{2}/{3}/outbound?lang=nl'.format(base_url, calendar_price_request_url, origincode, destinationcode)
    response = requests.get(full_url)
    return response.json()


class CheapestRequest:

    cheapest_journey_boolean = ''
    origin = ''
    destination = ''
    date = ''
    time = ''
    amount_of_passengers = ''
    juncture = ''
