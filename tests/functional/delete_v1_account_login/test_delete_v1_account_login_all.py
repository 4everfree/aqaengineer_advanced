def test_delete_v1_account_login_all(account_helper, create_user_data):
    login = create_user_data.login
    old_password = create_user_data.password
    email = create_user_data.email

    account_helper.register_new_user(login=login, password=old_password, email=email)
    account_helper.user_login(login=login, password=old_password)
    headers = account_helper.auth_client(login=login, password=old_password)

    response = account_helper.logout_all_devices(headers=headers)

    response = account_helper.get_user_info()
    assert response.status_code == 401, "Неправильный статус код при logout"
    assert response.json()['title'] == 'User must be authenticated', "Неправильный дескрипшен logout"