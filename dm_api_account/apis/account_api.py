import requests

from dm_api_account.models.registration import Registration
from dm_api_account.models.user_envelope_response import UserEnvelope
from dm_api_account.models.user_password import UserPassword
from dm_api_account.models.user_updated_password import UserUpdatedPassword
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            registration: Registration,
    ):
        """
        Register a new user
        :param validate_response:
        :param registration:
        :return:
        """
        response = self.post(
            path="/v1/account",
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        assert response.status_code == 201, f"Пользователь {registration.login} не был создан \n Response: {response.json()}"
        return response

    def put_v1_account_token(
            self,
            token: str,
            validate_response: bool = True,
    ) -> UserEnvelope | requests.Response:
        """
        Activate a registered user
        :param validate_response:
        :param token:
        :return:
        """
        response = self.put(
            path=f"/v1/account/{token}"
        )
        assert response.status_code == 200, f"Пользователь не был активирован \n Response: {response.json()}"
        if validate_response:
            UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            registration: Registration,
            validation_response: bool = True,
    ) -> UserEnvelope | requests.Response:
        """
        Change a registered user email
        :param registration:
        :return:
        """
        response = self.put(
            path="/v1/account/email",
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        assert response.status_code == 200, f"EMail не изменился \n Response: {response.json()}"
        if validation_response:
            return UserEnvelope(**response.json())
        return response

    def get_v1_account(
            self,
            validation_response: bool = True,
            **kwargs,
    ) -> UserEnvelope | requests.Response:
        """
        Get a registered user
        :param validation_response:
        :param self:
        :param kwargs:
        :return:
        """
        response = self.get(
            path="/v1/account",
            **kwargs
        )
        if validation_response:
            UserEnvelope(**response.json())
        return response


    def put_v1_account_password(
            self,
            update_password: UserUpdatedPassword,
            validation_response: bool = True,
    ) -> UserEnvelope | requests.Response:
        """
        Change a registered user email
        :param validation_response:
        :param update_password:
        :return:
        """
        response = self.put(
            path="/v1/account/password",
            json=update_password.model_dump(exclude_none=True, by_alias=True)
        )
        assert response.status_code == 200, f"EMail не изменился \n Response: {response.json()}"
        if validation_response:
            UserEnvelope(**response.json())
        return response


    def post_v1_account_password(
            self,
            user_password: UserPassword,
            validation_response: bool = True,
    ) -> UserEnvelope | requests.Response:
        """
        Reset a registered user password
        :param validation_response:
        :param self:
        :param user_password:
        :return:
        """
        response = self.post(
            path="/v1/account/password",
            json=user_password.model_dump(exclude_none=True, by_alias=True)
        )
        assert response.status_code == 200
        if validation_response:
            return UserEnvelope(**response.json())
        return response
