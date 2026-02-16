from json import loads

from requests import Response


class Utils:

    @staticmethod
    def get_activation_token_by_login(
            login: str,
            response: Response,
    ):
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(user_login)
                print(token)
                return token
        raise AssertionError('No token in the mailbox')

