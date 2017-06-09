import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
from manage import db, app
from config import TestingConfig
import json

class LoggingTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, email="joan.awinja@andela.com", password="Awinja@1"):
        user = {
            "email": email,
            "password": password
        }
        return self.client.post('/auth/register', data=json.dumps(user), content_type='application/json')

    def test_successful_user_login(self):
        login_user = {"email": "joan.awinja@andela.com", "password": "Awinja@1"}
        login_response = self.client.post('/auth/login', data=json.dumps(login_user))
        self.assertEqual(login_response.status_code, 200)

    def test_login_user_with_invalid_email(self):
        login_user = {"email": "james.a@andela.com", "password": "Awinja@1"}
        response = self.client.post('/auth/login', data=json.dumps(login_user))
        self.assertEqual(response.status_code, 400)

    def test_login_user_with_wrong_password(self):
        login_user = {"email": "joan.awinja@andela.com", "password": "awinja@1"}
        response = self.client.post('/auth/login/', data=json.dumps(login_user))
        self.assertEqual(response.status_code, 401)

    def test_login_user_with_wrong_credentials(self):
        login_user = {"email": "james.o@andela.com", "password": "ochweri@1"}
        response = self.client.post('/auth/login/', data=json.dumps(login_user))
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()