from json import loads

import requests
import random

from requests import Response


def test_post_v1_account():

    number = random.randint(0,10000)
    login = f"scarface_test{number}"
    password = f"abc{number*3}cba"

    headers = {
        "accept": "*/*",
        "content-Type": "application/json"
    }

    json_data = {
        "login": login,
        "email": f"{login}@mail.ru",
        "password": password
    }
    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь {login} не был создан \n Response: {response.json()}"

    # get the letter
    params = {
        'limit': 50
    }

    response = requests.get(f"http://185.185.143.231:5025/api/v2/messages",params=params, verify=False)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # activate with token
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(user_login)
            print(token)

    assert token is not None, f"Токен для пользователя {login} не был получен"

    #activate user
    response = requests.put(url=f"http://185.185.143.231:5051/v1/account/{token}")
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Пользователь {login} не был активирован \n Response: {response.json()}"

    # authorize
    login_url = f"http://185.185.143.231:5051/v1/account/login"

    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = requests.post(login_url, json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Пользователь {login} не смог авторизоваться \n Response: {response.json()}"