def test_get_v1_account(auth_account_helper):
    auth_account_helper.dm_account_api.account_api.post_v1_account(
        json_data=auth_account_helper.dm_account_json_data
    )
    auth_account_helper.dm_account_api.account_api.get_v1_account()