import random
from json import loads

from requests import Response

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMAPIAccount


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
        response = self.mailhog.mail_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        token = self.get_activation_token_by_login(login=login, response=response)
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

    @staticmethod
    def get_activation_token_by_login(
            login: str,
            response: Response,
    ) -> str | None:
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(user_login)
                print(token)
                return token
        raise AssertionError('No token in the mailbox')

    def create_user_data(
            self
    ) -> tuple[str, str, str]:
        number = self._return_random_number()
        login = f"scarface_test{number}"
        password = f"abc{number * 3}cba"
        email = f"{login}@mail.ru"
        return login, password, email

    @staticmethod
    def _return_random_number():
        return random.randint(0, 10000)