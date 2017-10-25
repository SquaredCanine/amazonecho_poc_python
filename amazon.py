import requests

base_url = 'https://api.amazon.com/user/profile?access_token='


def get_user_data(acces_token):
    full_url = '{0}{1}'.format(base_url, acces_token)
    print(full_url)
    response = requests.get(full_url)
    return response.json()
