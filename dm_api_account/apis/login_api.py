import requests

from restclient.client import RestClient


class LoginApi(RestClient):


    def post_v1_account_login(
            self,
            json_data: dict[str, str | bool],
    ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(
            path="/v1/account/login",
            json=json_data
        )
        print(response.status_code)
        print(response.text)
        return response