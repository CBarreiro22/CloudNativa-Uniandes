from src.main import app


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

    def test_update_user(self):
        with app.test_client() as test_client:
            # Create a test user first
            data = {
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com"
            }
            test_client.post('/users', json=data)

            update_data = {
                "status": "NEW_STATUS",
                "dni": "87654321",
                "fullName": "Updated User",  # Changed from "fullname" to "fullName"
                "phoneNumber": "987654321"
            }
            response = test_client.patch('/users/1', json=update_data)
            assert response.status_code == 200
            response_data = response.json
            assert "msg" in response_data

    # ... (Other test methods)

    def test_get_user_info(self):
        with app.test_client() as test_client:
            # Create a test user first
            data = {
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com"
            }
            test_client.post('/users', json=data)

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
