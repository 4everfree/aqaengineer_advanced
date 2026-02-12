import requests


class AccountApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(
            self,
            json_data: dict[str, str],
    ):
        """
        Register a new user
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f"{self.host}/v1/account",
            json=json_data
        )
        print(response.status_code)
        print(response.text)
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
        response = requests.put(
            url=f"{self.host}/v1/account/{token}"
        )
        print(response.status_code)
        print(response.text)
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
        response = requests.put(
            url=f"{self.host}/v1/account/email",
            json=json_data
        )
        print(response.status_code)
        print(response.text)
        return response
