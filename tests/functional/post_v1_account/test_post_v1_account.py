import random

import structlog.processors

from dm_api_account.apis.login_api import LoginApi
from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

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

def test_post_v1_account():

    main_host = f"{Config.PROTOCOL}://{Config.BASE_URL}"

    api_host = f"{main_host}:{Config.API_PORT}"
    dmapi_configuration = DmApiConfiguration(api_host)

    mail_host = f"{main_host}:{Config.MAIL_PORT}"
    mailhog_configuration = MailhogConfiguration(mail_host)

    login_api = LoginApi(configuration=dmapi_configuration)
    account_api = AccountApi(configuration=dmapi_configuration)
    mail_api = MailhogApi(configuration=mailhog_configuration)

    number = random.randint(0, 10000)
    login = f"scarface_test{number}"
    password = f"abc{number * 3}cba"

    json_data = {
        "login": login,
        "email": f"{login}@mail.ru",
        "password": password
    }

    response = account_api.post_v1_account(json_data=json_data)
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
    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f"Пользователь {login} не смог авторизоваться \n Response: {response.json()}"
