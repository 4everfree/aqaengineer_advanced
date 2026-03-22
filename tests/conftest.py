import random
from collections import namedtuple

import pytest
import structlog.processors

from api_mailhog.apis.mailhog_api import MailhogApi
from helpers.account_helper import AccountHelper
from services.dm_api_account import DMAPIAccount
from restclient.configuration import Configuration as DmApiConfiguration

from tests.config import Config


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

@pytest.fixture
def main_host():
    main_host = f"{Config.PROTOCOL}://{Config.BASE_URL}"
    return main_host

@pytest.fixture
def api_host(main_host):
    api_host = f"{main_host}:{Config.API_PORT}"
    return api_host

@pytest.fixture
def mail_host(main_host):
    mail_host = f"{main_host}:{Config.MAIL_PORT}"
    return mail_host

@pytest.fixture
def account_api(api_host):
    dm_api_configuration = DmApiConfiguration(api_host)
    account_api = DMAPIAccount(configuration=dm_api_configuration)
    return account_api

@pytest.fixture
def mailhog_api(mail_host):
    dm_api_configuration = DmApiConfiguration(mail_host)
    mailhog_api: MailhogApi | None  = MailhogApi(configuration=dm_api_configuration)
    return mailhog_api

@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def create_user_data() -> tuple[str, str, str]:
    number = random.randint(0, 10000)
    login = f"{number}"
    password = f"abc{number * 3}cba"
    email = f"{login}@mail.ru"
    User = namedtuple(
        "User",['login','password','email'])
    return User(login=login, password=password, email=email)

