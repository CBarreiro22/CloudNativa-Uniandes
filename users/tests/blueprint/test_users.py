from users.src.main import app


class TestUserOperations:

    def test_create_user(self):
        with app.test_client() as test_client:
            data = {
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com",
                "dni": "12345678",
                "fullName": "Test User",  # Changed from "fullname" to "fullName"
                "phoneNumber": "123456789"
            }
            response = test_client.post('/users', json=data)
            assert response.status_code == 200
            response_data = response.json
            assert "id" in response_data
            assert "createdAt" in response_data

    def test_create_user_exist(self):

        with app.test_client() as test1_client:

            data = {
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com",
                "dni": "12345678",
                "fullName": "Test User",  # Changed from "fullname" to "fullName"
                "phoneNumber": "123456789"
            }
            response = test1_client.post('/users', json=data)
            assert response.status_code == 412
            response_data = response.json
            error_message = response_data['error']
            assert "El usuario ya existe" in error_message

    def test_update_user(self):
        with app.test_client() as test_client:
            # Create a test user first
            create_data = {
                "username": "testuser2",
                "password": "testpassword2",
                "email": "test2@example.com",
                "dni": "12345678",
                "fullName": "Test User",
                "phoneNumber": "123456789"
            }
            response = test_client.post('/users', json=create_data)
            user_id = response.json["id"]


            # Fetch the user to ensure the updates were applied
            login_data = {
                "username": "testuser2",
                "password": "testpassword2"
            }
            token_response = test_client.post('/users/auth', json=login_data)
            token = token_response.json["token"]

            headers = {
                "Authorization": f"Bearer {token}"
            }
            update_data = {
                "status": "NO_VERIFICADO",
                "dni": "87654321",
                "fullName": "Updated User",
                "phoneNumber": "987654321"
            }
            update_url = f'/users/{user_id}'
            response = test_client.patch(update_url, json=update_data)

            assert response.status_code == 200
            response_data = response.json
            assert "msg" in response_data
            response = test_client.get('/users/me', headers=headers)
            assert response.status_code == 200
            user_data = response.json
            assert user_data["status"] == update_data["status"]
            assert user_data["dni"] == update_data["dni"]
            assert user_data["fullName"] == update_data["fullName"]
            assert user_data["phoneNumber"] == update_data["phoneNumber"]
    # ... (Other test methods)

    def test_get_user_info(self):
        with app.test_client() as test_client:
            # Create a test user first
            data = {
                "username": "testuser2",
                "password": "test2password",
                "email": "test2@example.com"
            }
            test_client.post('/users', json=data)

            login_data = {
                "username": "testuser2",
                "password": "testpassword2"
            }
            token_response = test_client.post('/users/auth', json=login_data)
            token = token_response.json["token"]

            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = test_client.get('/users/me', headers=headers)
            assert response.status_code == 200
            response_data = response.json
            assert "id" in response_data
            assert "username" in response_data
            assert "email" in response_data
            assert "fullName" in response_data
            assert "dni" in response_data
            assert "phoneNumber" in response_data
            assert "status" in response_data

    def test_generate_token(self):
        with app.test_client() as test_client:
            create_data = {
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com",
                "dni": "12345678",
                "fullName": "Test User",
                "phoneNumber": "123456789"
            }
            test_client.post('/users', json=create_data)

            login_data = {
                "username": "testuser",
                "password": "testpassword"
            }
            response = test_client.post('/users/auth', json=login_data)
            assert response.status_code == 200
            response_data = response.json
            assert "id" in response_data
            assert "token" in response_data
            assert "expireAt" in response_data

    def test_get_user_info_authenticated(self):
        with app.test_client() as test_client:
            create_data = {
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com",
                "dni": "12345678",
                "fullName": "Test User",
                "phoneNumber": "123456789"
            }
            test_client.post('/users', json=create_data)

            login_data = {
                "username": "testuser",
                "password": "testpassword"
            }
            token_response = test_client.post('/users/auth', json=login_data)
            token = token_response.json["token"]

            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = test_client.get('/users/me', headers=headers)

            assert response.status_code == 200
            response_data = response.json
            assert "id" in response_data
            assert "username" in response_data
            assert "email" in response_data
            assert "fullName" in response_data
            assert "dni" in response_data
            assert "phoneNumber" in response_data
            assert "status" in response_data