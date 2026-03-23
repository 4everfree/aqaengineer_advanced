def test_put_v1_account_email(account_helper, create_user_data):
    login = create_user_data.login
    password = create_user_data.password
    email = create_user_data.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

    email = email.split('@')[0] + '1@' + email.split('@')[1]
    account_helper.update_account_email(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password, status_code=403)
    account_helper.activate_user(login)
    account_helper.user_login(login=login, password=password)

