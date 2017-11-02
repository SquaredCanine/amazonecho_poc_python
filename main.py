"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import time
import database
import nsi
import mailclient
import amazon
from datetime import datetime, timedelta

calc_time = datetime.now() + timedelta(hours=2)
current_date = calc_time.strftime('%Y%m%d')
current_time = calc_time.strftime('%H%M')
global journeyhasbeenselected
journeyhasbeenselected = False
global possible_connections
possible_connections = []
global unique_ns_id
unique_ns_id = ''

# --------------- Helper Functions ---------------------------------------------


def add_user(access_token, UID):
    response = amazon.get_user_data(access_token)
    database.add_user(UID, response['name'], response['email'])

# --------------- Helpers that build all of the responses ----------------------


def delegate_directive(intent):
    delegate = {
        'type': 'Dialog.Delegate',
        'updatedIntent': intent
    }
    print(delegate)
    return delegate


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_simple_response(speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': speechlet_response
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def build_dialog(intent):
    return {
        'version': '1.0',
        'response': {
            'directives': [
                delegate_directive(intent)
            ],
            'shouldEndSession': 'false'
        },
        'sessionAttributes': {}
    }


def link_account_card():
    return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'Go to your alexa app to link this skill'
            },
            'card': {
                'type': 'LinkAccount'
            },
            'shouldEndSession': True
        }


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_traveler_response(intent, session):
    destination = intent['slots']['toCity']['value']
    origin = intent['slots']['fromCity']['value']
    output = 'You have chosen ' + origin + ' as your place of departure. And you want to go to ' + destination + '. '
    if 'value' in intent['slots']['date']:
        date = intent['slots']['date']['value']
        output += 'On ' + date + ". "
    if 'value' in intent['slots']['juncture']:
        juncture = intent['slots']['juncture']['value']
        arrival = True if juncture == 'arrival' else False
    if 'value' in intent['slots']['time']:
        chosentime = intent['slots']['time']['value']

    timetable = nsi.get_price_and_time_response(origin, destination, current_date, current_time, 2, 'departure')

    if not timetable:
        alternative = 'Your selected origin or destination is wrong, please try again.'
        return build_simple_response(build_speechlet_response('card', alternative, 'Are you there?', 'true'))

    all_connections = timetable['data']['connections']
    global unique_ns_id
    unique_ns_id = timetable['data']['uid']
    global possible_connections
    counter = 0
    for element in all_connections:
        if element['status'] == 'bookable':
            possible_connections.append(element)
            if len(possible_connections) >= 3:
                break

    if not possible_connections:
        alternative = 'There are no trains available, try a different date'
        return build_simple_response(build_speechlet_response('card', alternative, 'Are you there?', 'true'))

    output += 'There are ' + str(len(possible_connections)) + ' options available. '
    ordinal_number_list = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']
    counter = 0
    for element in possible_connections:
        output += 'The ' + ordinal_number_list[counter] + ' option is arrival at ' + \
                      element['destination']['arrival']['planned'].split()[1] + '. '
        counter += 1
    if counter == 0:
        output = "There are no options available, try choosing a different date"
        return build_simple_response(build_speechlet_response('card', output, 'Are you there?', 'true'))
    else:
        output += "Which option do you choose?"
        global journeyhasbeenselected
        journeyhasbeenselected = True
    reprompt = 'If you want to cancel the order just say exit.'
    return build_simple_response(build_speechlet_response('card', output, reprompt, 'false'))


def get_choose_intent_response(intent, session):
    global possible_connections
    option = int(intent['slots']['option']['value'])
    outputtext = 'You have chosen option ' + str(option) + '. '
    option -= 1
    if option < 0:
        option = 0
    elif option > 2:
        option = 2
    if len(possible_connections) - 1 > option:
        option = 0
    selected_journey = possible_connections[option]
    print(selected_journey)
    response = nsi.provisional_booking_request(unique_ns_id, selected_journey, 0, 2)
    gotourl = 'https://www.nsinternational.nl/en/traintickets#/passengers/' + response['data']['dnrId'] + '?signature=' \
              + response['data']['signature']
    print(gotourl)
    database.add_journey(selected_journey, session['user']['userId'], 0)
    user_email = database.get_user_email(session['user']['userId'])
    mailclient.set_destination(user_email)
    mailclient.set_body(selected_journey, gotourl)
    mailclient.send_mail()

    outputtext += 'You will depart at ' + selected_journey['origin']['departure']['planned'].split()[1] + \
                  ', from ' + selected_journey['origin']['name'] + \
                  '. Your journey will be ' + str(selected_journey['duration']['hours']) + ' hours and ' + \
                  str(selected_journey['duration']['minutes']) + ' minutes long. ' \
                                                                 ' And you will arrive on ' + \
                  selected_journey['destination']['arrival']['planned'].split()[1] + \
                  ' at ' + selected_journey['destination']['name'] + '. '
    outputtext += 'Go to your email to finish the booking. '
    return build_simple_response(build_speechlet_response('card', outputtext, 'Are you there?', 'true'))


def get_cheapest_option(intent, session):
    print('hello')



def get_location_intent_response(intent, session):
    print('hello')


def get_composition_intent_response(intent, session):
    print('hello')


# --------------- Events ------------------


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    print(intent_request)

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    dialogstate = intent_request['dialogState']
    print(intent_name)
    print(intent)
    print(session)
    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()

    if dialogstate == 'STARTED' or dialogstate == 'IN_PROGRESS':
        return build_dialog(intent)

    if intent_name == "Traveler":
        return get_traveler_response(intent, session)
    elif intent_name == "Cheapest":
        return get_cheapest_option(intent, session)
    elif intent_name == "LocationIntent":
        return get_location_intent_response(intent, session)
    elif intent_name == "CompositionIntent":
        return get_composition_intent_response(intent, session)
    elif intent_name == "ChooseIntent" and journeyhasbeenselected:
        return get_choose_intent_response(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    global possible_connections, journeyhasbeenselected
    possible_connections = []
    journeyhasbeenselected = False


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    print(event)
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.df22d8e8-7b48-4d1a-b370-d0601cddcaee"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if not event['session']['user']['accessToken']:
        return build_simple_response(link_account_card())
    elif not database.get_user_email(event['session']['user']['userId']):
        add_user(event['session']['user']['accessToken'], event['session']['user']['userId'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
