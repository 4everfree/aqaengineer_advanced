import requests
from requests import Response

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope_response import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):


    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response: bool = True,
    ):
        """
         Authenticate via credentials
        :param validate_response:
        :param login_credentials:
        :return:
        """
        response = self.post(
            path="/v1/account/login",
            json=login_credentials.model_dump(exclude_none=True, by_alias=True),
        )
        if validate_response:
            UserEnvelope(**response.json())
        return response

    def delete_v1_account_login(
            self,
            **kwargs
    ) -> Response:
        """
        Logout via token
        :param headers:
        :return:
        """
        response = self.delete(
            path="/v1/account/login",
            **kwargs
        )
        assert response.status_code == 204, f"Log out не удался"
        return response

    def delete_v1_account_login_all(
            self,
            **kwargs
    ) -> Response:
        """
        Logout via token
        :param headers:
        :return:
        """
        response = self.delete(
            path="/v1/account/login/all",
            **kwargs
        )
        assert response.status_code == 204, f"Log out на всех устройствах не удался"
        return response