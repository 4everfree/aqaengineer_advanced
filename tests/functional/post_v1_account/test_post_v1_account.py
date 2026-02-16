import random

import structlog.processors

from helpers.account_helper import AccountHelper
from services.dm_api_account import DMAPIAccount
from services.api_mailhog import MailHogApi
from restclient.configuration import Configuration as MailhogConfiguration
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

def test_post_v1_account():

    main_host = f"{Config.PROTOCOL}://{Config.BASE_URL}"
    api_host = f"{main_host}:{Config.API_PORT}"
    mail_host = f"{main_host}:{Config.MAIL_PORT}"

    dm_api_configuration = DmApiConfiguration(api_host)
    mailhog_configuration = MailhogConfiguration(mail_host)

    account = DMAPIAccount(configuration=dm_api_configuration)
    mail = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mail)

    number = random.randint(0, 10000)
    login = f"scarface_test{number}"
    password = f"abc{number * 3}cba"
    email = f"{login}@mail.ru"

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

