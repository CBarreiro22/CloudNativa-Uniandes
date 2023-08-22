import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

from src.main import app
from src.models.model import db_session
from src.models.post import Post


class TestOperations(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        db_session.remove()

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_create_post(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        response = self.tester.post("/posts", json={
            'routeId': 'fnajkdkjawDKJWAndlkaw',
            'expireAt': (datetime.now() + timedelta(days=1)).isoformat()
        }, headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})

        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertIn('id', data)
        self.assertIn('userId', data)
        self.assertIn('createdAt', data)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_create_post_invalid_expire_at(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        response = self.tester.post("/posts", json={
            'routeId': 'fnajkdkjawDKJWAndlkaw',
            'expireAt': 'invalid_datetime_format'
        }, headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})

        self.assertEqual(response.status_code, 412)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_delete_post(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        # Create a test post
        test_post = Post('test_route', 'test_user_id', datetime.now())
        db_session.add(test_post)
        db_session.commit()

        response = self.tester.delete(f"/posts/{test_post.id}",
                                      headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"msg": "La publicación fue eliminada"})

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_get_post(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        # Create a test post
        test_post = Post('test_route', 'test_user_id', datetime.now())
        db_session.add(test_post)
        db_session.commit()

        response = self.tester.get(f"/posts/{test_post.id}",
                                   headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)
        self.assertIn('userId', response.json)
        self.assertIn('createdAt', response.json)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_get_posts(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        response = self.tester.get("/posts", headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_reset_database(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        response = self.tester.post("/posts/reset")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"msg": "Todos los datos fueron eliminados"})

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_get_posts_with_filters(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        # Create test posts with different properties
        test_post1 = Post('route_1', 'test_user_id', datetime.now())
        test_post2 = Post('route_2', 'test_user_id', datetime.now() + timedelta(days=2))
        test_post3 = Post('route_3', 'other_user_id', datetime.now() + timedelta(days=5))
        db_session.add_all([test_post1, test_post2, test_post3])
        db_session.commit()

        response = self.tester.get("/posts?expire=true&route=route_1&owner=me",
                                   headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['routeId'], 'route_1')

    def test_check_health(self):
        response = self.tester.get("/posts/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'pong')

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_delete_post_invalid_uuid(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        invalid_uuid = "invalid_uuid_format"

        response = self.tester.delete(f"/posts/{invalid_uuid}",
                                      headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
        self.assertEqual(response.status_code, 400)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_invalid_uuid_parameter_missing_id(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        response = self.tester.get("/posts/some_route",
                                   headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
        self.assertEqual(response.status_code, 400)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_invalid_uuid_parameter_invalid_id(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        invalid_id = "invalid_id_format"

        response = self.tester.get(f"/posts/{invalid_id}",
                                   headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
        self.assertEqual(response.status_code, 400)

    @patch('src.commands.user_service.UserService.get_user_information')
    def test_get_posts_invalid_expire(self, mock_get_user_info):
        mock_get_user_info.return_value = 'test_user_id'

        mock_response = Mock()
        mock_response.status_code = 200

        with patch('src.commands.user_service.requests.get', return_value=mock_response):
            response = self.tester.get("/posts?expire=invalid_value",
                                       headers={'Authorization': 'Bearer 2fcbb20f-39f8-4691-98b9-9983a1be1256'})
            self.assertEqual(response.status_code, 400)

    if __name__ == '__main__':
        unittest.main()
