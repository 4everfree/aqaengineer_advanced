import random

import structlog

from dm_api_account.apis.login_api import LoginApi
from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi

from tests.config import Config

from tests.utils.utils import Utils

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

def test_put_v1_account_email():

    main_host = f"{Config.PROTOCOL}://{Config.BASE_URL}"
    api_host = f"{main_host}:{Config.API_PORT}"
    mail_host = f"{main_host}:{Config.MAIL_PORT}"
    login_api = LoginApi(api_host)
    account_api = AccountApi(api_host)
    mail_api = MailhogApi(mail_host)

    number = random.randint(0, 10000)
    email, login, password = create_user_data(number)

    reg_json = {
        "login": login,
        "email": email,
        "password": password
    }

    response = account_api.post_v1_account(json_data=reg_json)
    assert response.status_code == 201, f"Пользователь {login} не был создан \n Response: {response.json()}"

    # get the letter
    response = mail_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # activate with token
    token = Utils.get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # activate user
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"Пользователь {login} не был активирован \n Response: {response.json()}"

    # authorize
    auth_json = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_data=auth_json)
    assert response.status_code == 200, f"Пользователь {login} не смог авторизоваться \n Response: {response.json()}"

    #change email
    number = random.randint(0, 10000)
    email, _, _ = create_user_data(number)
    reg_json = {
        "login": login,
        "password": password,
        "email": email,
    }

    response = account_api.put_v1_account_email(json_data=reg_json)
    assert response.status_code == 200, f"EMail не изменился \n Response: {response.json()}"

    # try to authorize
    response = login_api.post_v1_account_login(json_data=auth_json)
    assert response.status_code == 403, f"Пользователь {login} не смог авторизоваться \n Response: {response.json()}"

    # get the letter
    response = mail_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены"

    # get the activation token
    token = Utils.get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # activate user
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"Пользователь {login} не был активирован \n Response: {response.json()}"

    # authorize
    response = login_api.post_v1_account_login(json_data=auth_json)
    assert response.status_code == 200, f"Пользователь {login} не смог авторизоваться \n Response: {response.json()}"


def create_user_data(number: int) -> tuple[str, str, str]:
    login = f"scarface_test{number}"
    password = f"abc{number * 3}cba"
    email = f"{login}@mail.ru"
    return email, login, password
