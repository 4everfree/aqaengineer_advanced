import random

import structlog.processors

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

def test_post_v1_account():

    main_host = f"{Config.PROTOCOL}://{Config.BASE_URL}"
    api_host = f"{main_host}:{Config.API_PORT}"

    dm_api_configuration = DmApiConfiguration(api_host)

    account = DMAPIAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=None)

    login, password, email = account_helper.create_user_data()
    account_helper.register_user(login=login, password=password, email=email)
