from services.api_mailhog import MailHogApi
from services.dm_api_account import DMAPIAccount
from tests.config import Config
from helpers.account_helper import AccountHelper

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

def test_post_v1_account_login(account_helper, create_user_data):

    login = create_user_data.login
    password = create_user_data.password
    email = create_user_data.email
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
