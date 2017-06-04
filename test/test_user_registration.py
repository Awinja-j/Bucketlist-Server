import unittest
from app import db
from app.models import User
from test import BaseTestCase




class TestUserModel(unittest.TestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)


class RegistrationTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_succesful_user_registration(self):
        """this contains all the user functionality"""
        # Test API can create new user(POST request)all credentials
        self.user = {"first_name": "Joan", "last_name": "Awinja", "email": "joan.awinja@andela.com",
                     "password": "Awinja@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code, 201)

    def test_registration_with_missing_firstname(self):
        # add user with missing first name
        self.user = {"last_name": "mwaniki", "email": "josh.mwaniki@andela.com", "password": "josh@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code, 201)

    def test_registration_with_missing_lastname(self):
        # add user with missing last name
        self.user = {"first_name": "Jones", "email": "jones.ingari@andela.com", "password": "jones@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code, 201)

    def test_registration_with_empty_password_field(self):
        # add user with missing password
        self.user = {"first_name": "Judy", "last_name": "Khasoa", "email": "judy.khasoa@andela.com"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code, 400)

    def test_register_with_empty_email_field(self):
        # add user with missing email
        # The client SHOULD NOT repeat the request without modifications.
        self.user = {"first_name": "Tom", "last_name": "Nganyi", "password": "Nganyi@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code, 400)

    def test_registration_with_invalid_email_format(self):
        # add user with invalid email format
        # The client SHOULD NOT repeat the request without modifications.
        self.user = {"first_name": "James", "last_name": "Ochweri", "email": "james.ochweri.com",
                     "password": "Ochweri@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code, 400)

    def test_registration_with_used_email_address(self):
        # add duplicate user email
        # The client SHOULD NOT repeat the request without modifications.
        self.user = {"first_name": "John", "last_name": "Kamau", "email": "joan.awinja@andela.com",
                     "password": "Awinja@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
            """teardown all initialized variables."""
            with self.app.app_context():
                # drop all tables
                db.session.remove()
                db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()