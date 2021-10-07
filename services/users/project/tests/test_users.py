import json
import unittest
from project.tests.base import BaseTestCase
from project import db
from project.api.models import User

def add_user(username: str, email: str):
    """Helper method to add user to the db

    Args:
        username (str): [username]
        email (str): [email]
    """
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

def users_count():
    """Count Users Currently in the Database
    """
    users = User.query.all()
    return len(users)


class TestUserService(BaseTestCase):
    """
        Users Service Test
    """
    def test_users(self):
        """
            Ensure the /hello route behaves as expected
        """
        response = self.client.get('/users/hello')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('hi you!', data['message'])
        self.assertIn('success', data['status'])

   

    def test_add_user(self):
        """
        Tests to Make Sure a New User Can be added Successfully
        """
        with self.client:
            response = self.client.post('/users', data=json.dumps({
                'username':'arthur',
                'email':'arthur@gmail.com'
            }), content_type='application/json')

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('user arthur@gmail.com was added with success', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_payload(self):
        """Throw Error if an empty payload is sent
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid request payload', data['message'])
            self.assertIn('failed', data['status'])

    def test_add_user_invalid_payload_keys(self):
        """Throw an error if email key is missing from request payload
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'username':'arthur1'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid request payload', data['message'])
            self.assertIn('failed', data['status'])

    def test_add_user_duplicate_email(self):
        """Throw an error if the email already exists."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'david',
                    'email': 'david@gmail.com'
                }),
                content_type='application/json',
            ) 
            response =  self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'david',
                    'email': 'david@gmail.com'
                }),
                content_type='application/json',
            ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('failed', data['status'])

    def test_get_single_user(self):
        """Ensure getting a single user works as expected
        """
        user = add_user('arthur1','arthur1@gmail.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('arthur1', data['data']['username'])
            self.assertIn('arthur1@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])
    
    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('failed', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/9435')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('failed', data['status'])

    # def test_all_users(self):
    #     """Ensure get all users route works as expected
    #     """
    #     add_user('mercy', 'mercy@gmail.com')
    #     add_user('bolum', 'bolum@gmail.com')
    #     user_count = users_count() + 2
    #     with self.client:
    #         response = self.client.get('/users')
    #         data = json.loads(response.data.decode())
    #         users_count = users_count()
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(len(data['data']['users']), user_count)
    #         self.assertIn('mercy', data['data']['users'][0]['username'])
    #         self.assertIn('mercy@gmail.com', data['data']['users'][0]['email'])
    #         self.assertIn('bolum', data['data']['users'][1]['username'])
    #         self.assertIn('bolum@gmail.com', data['data']['users'][1]['email'])
    #         self.assertIn('success', data['status'])



if __name__ == '__main__':
    unittest.main() 