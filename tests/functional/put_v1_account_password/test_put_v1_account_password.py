def test_put_v1_account_password(account_helper, create_user_data):
    login = create_user_data.login
    old_password = create_user_data.password
    email = create_user_data.email

    account_helper.register_new_user(login=login, password=old_password, email=email)
    account_helper.user_login(login=login, password=old_password)
    headers = account_helper.auth_client(login=login, password=old_password)

    new_password = old_password + '1'
    account_helper.change_password(login=login, password=old_password, new_password=new_password, email=email, headers=headers)

    account_helper.user_login(login=login, password=old_password, status_code=400)
    account_helper.user_login(login=login, password=new_password)

