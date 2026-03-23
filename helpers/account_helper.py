import random
from json import loads

from retrying import retry
from requests import Response

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMAPIAccount


def retry_if_result_none(result):
    return result is None


class AccountHelper:

    def __init__(
            self,
            dm_account_api: DMAPIAccount,
            mailhog: MailHogApi = None
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            status_code: int = 200,
    ):
        json_data = {
            "login": login,
            "password": password,
            "rememberMe": remember_me
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == status_code, f"Response: {response.json()}"
        return response

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        response = self.register_user(login, password, email)
        response = self.activate_user(login)

        return response

    def activate_user(
            self,
            login: str
    ) -> Response:

        token = self.get_activation_token_by_login(login=login)
        token = token['ConfirmationLinkUrl'].split('/')[-1]
        assert token is not None, f"Токен для пользователя {login} не был получен"

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь {login} не был активирован \n Response: {response.json()}"
        return response

    def update_account_email(
            self,
            login: str,
            password: str,
            email: str
    ) -> Response:
        reg_json = {
            "login": login,
            "password": password,
            "email": email,
        }

        response = self.dm_account_api.account_api.put_v1_account_email(json_data=reg_json)
        assert response.status_code == 200, f"EMail не изменился \n Response: {response.json()}"

        return response

    def register_user(
            self,
            login: str,
            password: str,
            email: str
    ) -> Response:
        json_data = {
            "login": login,
            "email": email,
            "password": password
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь {login} не был создан \n Response: {response.json()}"

        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login: str,
    ) -> str | None:

        response = self.mailhog.get_api_v2_messages()

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                return user_data
        raise AssertionError('No token in the mailbox')

    def auth_client(
            self,
            login: str,
            password: str
    ):

        response = self.dm_account_api.login_api.post_v1_account_login(json_data={"login": login, "password": password})
        token = {
            "x-dm-auth-token": response.headers['X-Dm-Auth-Token']
        }
        self.dm_account_api.account_api.set_headers(headers=token)
        self.dm_account_api.login_api.set_headers(headers=token)
        return token

    def get_user_info(
            self
    ) -> Response:

        response = self.dm_account_api.account_api.get_v1_account()
        return response

    def update_account_password(
            self,
            login: str,
            password: str,
            token: str,
            headers: dict[str, str]
    ) -> str:
        new_password = password + "1"
        update_password = {
            "login": login,
            "token": token,
            "oldPassword": password,
            "newPassword": new_password,
        }

        response = self.dm_account_api.account_api.put_v1_account_password(json_data=update_password, headers=headers)
        assert response.status_code == 200, f"EMail не изменился \n Response: {response.json()}"

        return new_password

    def reset_password(
            self,
            login: str,
            email: str
    ) -> Response:
        json_data = {
            "login": login,
            "email": email,
        }

        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200, f"Пользователь {login} не был создан \n Response: {response.json()}"

        return response

    def get_password_mail_token(self,
        login: str,
    ) -> str:
        response = self.get_activation_token_by_login(login=login)
        return response['ConfirmationLinkUri'].split('/')[-1]

    def change_password(self,
        login: str,
        password: str,
        email: str,
        headers: dict[str, str]
    ) -> str:
        self.reset_password(login=login, email=email)
        new_password_mail_token = self.get_password_mail_token(login=login)
        new_password = self.update_account_password(login=login, password=password, token=new_password_mail_token, headers=headers)
        return new_password
