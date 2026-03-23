import requests

from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data: dict[str, str],
    ):
        """
        Register a new user
        :param json_data:
        :return:
        """
        response = self.post(
            path="/v1/account",
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token: str,
    ):
        """
        Activate a registered user
        :param token:
        :return:
        """
        response = self.put(
            path=f"/v1/account/{token}"
        )
        return response

    def put_v1_account_email(
            self,
            json_data: dict[str, str],
    ):
        """
        Change a registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path="/v1/account/email",
            json=json_data
        )
        return response

    def get_v1_account(
                self,
                **kwargs,
        ):
            """
            Get a registered user
            :param self:
            :param kwargs:
            :return:
            """
            response = self.get(
                path="/v1/account",
                **kwargs
            )
            return response

    def put_v1_account_password(
            self,
            json_data: dict[str, str],
            headers: dict[str, str],
    ):
        """
        Change a registered user email
        :param headers:
        :param json_data:
        :return:
        """
        response = self.put(
            path="/v1/account/password",
            json=json_data,
            headers=headers
        )
        return response

    def post_v1_account_password(
            self,
            json_data: dict[str, str],
    ):
        """
        Reset a registered user password
        :param json_data:
        :return:
        """
        response = self.post(
            path="/v1/account/password",
            json=json_data
        )
        return response