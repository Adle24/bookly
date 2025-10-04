auth_prefix = "/api/v1/auth"


def test_user_creation(fake_session, fake_user_service, test_client):
    signup_data = {
        "username": "jod35",
        "email": "jodstrevin@gmail.com",
        "firstname": "jod35",
        "lastname": "ssali",
        "password": "test1234",
    }

    response = test_client.post(url=f"{auth_prefix}/signup", json=signup_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.create_user_called_once_with(signup_data["email"], fake_session)