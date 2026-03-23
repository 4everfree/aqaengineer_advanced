
def test_post_v1_account(account_helper, create_user_data):
    login = create_user_data.login
    email = create_user_data.email
    password = create_user_data.password
    account_helper.register_user(login=login, password=password, email=email)
