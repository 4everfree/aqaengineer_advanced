import random
import structlog

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMAPIAccount
from tests.config import Config
from helpers.account_helper import AccountHelper

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_post_v1_account_login():

    main_host = f"{Config.PROTOCOL}://{Config.BASE_URL}"

    api_host = f"{main_host}:{Config.API_PORT}"
    dm_api_configuration = DmApiConfiguration(api_host)

    mail_host = f"{main_host}:{Config.MAIL_PORT}"
    mailhog_configuration = MailhogConfiguration(mail_host)

    account = DMAPIAccount(configuration=dm_api_configuration)
    mail = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mail)

    login, password, email = account_helper.create_user_data()

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
