import structlog

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMAPIAccount
from tests.config import Config
from helpers.account_helper import AccountHelper

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

def test_put_v1_account_email(account_helper, create_user_data):
    login, password, email = account_helper.create_user_data()

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

    email = create_user_data
    account_helper.update_account_email(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password, status_code=403)
    account_helper.activate_user(login)
    account_helper.user_login(login=login, password=password)

