from hamcrest import assert_that, has_property, starts_with, all_of, has_properties, equal_to


def test_post_v1_account(account_helper, create_user_data):
    login = create_user_data.login
    email = create_user_data.email
    password = create_user_data.password
    account_helper.register_user(login=login, password=password, email=email)
    response = account_helper.register_user(login=login, password=password, email=email)
    assert_that(response,
                all_of(
                    has_property("status_code"),
                    has_property("resource"),
                    has_property('login')
                )
                )
    assert_that(response,
                has_property('resource',
                             has_property('rating',
                                          has_properties(
                                              {
                                                  'enabled': equal_to(True),
                                                  'quality': equal_to(0),
                                                  'quantity': equal_to(0),
                                              }
                                          )
                                          )
                             )
                )
