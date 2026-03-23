def test_put_v1_account_password(account_helper, create_user_data):
    login = create_user_data.login
    old_password = create_user_data.password
    email = create_user_data.email

    account_helper.register_new_user(login=login, password=old_password, email=email)

    account_helper.user_login(login=login, password=old_password)
    token = account_helper.auth_client(login=login, password=old_password)

    account_helper.reset_password(login=login, email=email)

    new_password_mail_token = account_helper.get_password_mail_token(login=login)
    new_password = account_helper.update_account_password(login=login, password=old_password, token=new_password_mail_token, headers=token, )

    account_helper.user_login(login=login, password=old_password, status_code=400)
    account_helper.user_login(login=login, password=new_password)

