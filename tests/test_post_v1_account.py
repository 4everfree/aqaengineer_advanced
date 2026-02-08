import requests
import random

def test_post_v1_account():

    protocol = "http"
    host = "5.63.153.31"
    port = 5051
    api_url = f'{protocol}://{host}:{port}/v1'

    account_url = f'{api_url}/account'
    number = random.randint(0,10000)
    login = f"scarface_test{number}"
    password = f"abc{number*3}cba"
    json_data = {
        "login": login,
        "email": f"{login}@mail.ru",
        "password": password
    }

    response = requests.post(url=account_url, data=json_data)
    print(response.json())

    # get the letter
    params = {
        'limit': 50
    }

    mail_port = 5025
    mail_url = f"{protocol}://{host}:{mail_port}/api/v2/messages"
    response = requests.get(url=mail_url,params=params)

    # activate with token
    token = ""
    response = requests.put(url=f"{account_url}/{token}")

    # authorize
    login_url = f"{account_url}/login"

    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = requests.post(url=login_url)