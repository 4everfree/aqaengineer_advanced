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
        :param registration:
        :return:
        """
        response = self.post(
            path="/v1/account",
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def put_v1_account_token(
            self,
            token: str,
            validate_response: bool = True,
    ):
        """
        Activate a registered user
        :param validate_response:
        :param token:
        :return:
        """
        response = self.put(
            path=f"/v1/account/{token}"
        )
        if validate_response:
            UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            registration: Registration,
    ):
        """
        Change a registered user email
        :param registration:
        :return:
        """
        response = self.put(
            path="/v1/account/email",
            json=registration.model_dump(exclude_none=True, by_alias=True)
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
            UserEnvelope(**response.json())
            return response

    def put_v1_account_password(
            self,
            update_password: UserUpdatedPassword,
    ):
        """
        Change a registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path="/v1/account/password",
            json=update_password.model_dump(exclude_none=True, by_alias=True)
        )
        UserEnvelope(**response.json())
        return response

    def post_v1_account_password(
            self,
            user_password: UserPassword,
    ):
        """
        Reset a registered user password
        :param user_password:
        :return:
        """
        response = self.post(
            path="/v1/account/password",
            json=user_password.model_dump(exclude_none=True, by_alias=True)
        )
        assert response.status_code == 200
        return response