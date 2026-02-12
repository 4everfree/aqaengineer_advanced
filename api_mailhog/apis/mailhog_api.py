import requests


class MailhogApi:

    def __init__(
            self,
            host,
            headers=None,
    ):
        self.host = host
        self.headers = headers

    def get_api_v2_messages(
            self,
            limit: int = 50,
    ):
        """
        Get user's emails
        :return:
        """
        params = {
            'limit': limit
        }

        response = requests.get(
            url=f"{self.host}/api/v2/messages",
            params=params,
            verify=False
        )
        print(response.status_code)
        print(response.text)
        return response
