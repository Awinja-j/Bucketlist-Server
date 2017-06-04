import unittest


class LoggingTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
    def test_succesful_user_login(self):
        user ={"first_name": "Joan", "last_name" : "Awinja", "email": "joan.awinja@andela.com", "password": "Awinja@1"}
        create_response = self.client.post('/auth/register/', data=user)
        self.assertEqual(create_response.status_code,201)
        login_user = {"email" : "joan.awinja@andela.com", "password" : "Awinja@1"}
        login_response = self.client.post('/auth/login/', data=login_user)
        self.assertEqual(login_response.status_code, 302)

    def test_login_user_with_invalid_email(self):
        create_user = {"first_name": "Joan", "last_name" : "Awinja", "email": "joan.awinja@andela.com", "password": "Awinja@1"}
        create_response = self.client.post('/auth/register/', data=create_user)
        self.assertEqual(create_response.status_code,201)
        login_user = {"email" : "james.a@andela.com", "password" : "James@1"}
        response = self.client.post('/auth/login/', data=login_user)
        self.assertEqual(response.status_code, 400)

    def test_login_user_with_wrong_password(self):
        create_user = {"first_name": "James", "last_name" : "Ochweri", "email": "james.o@andela.com", "password": "ochweri@1"}
        create_response = self.client.post('/auth/register/', data=create_user)
        self.assertEqual(create_response.status_code,201)
        login_user = {"email" : "joan.awinja@andela.com", "password" : "awinja@1"}
        response = self.client().post('/auth/login/', data=login_user)
        self.assertEqual(response.status_code, 401)

    def test_login_user_with_wrong_credentials(self):
        create_user = {"first_name": "James", "last_name" : "Ochweri", "email": "james.o@andela.com", "password": "ochweri@1"}
        create_response = self.client.post('/auth/register/', data=create_user)
        self.assertEqual(create_response.status_code,201)
        login_user = {"email" : "joan.awinja@andela.com", "password" : "awinja@1"}
        response = self.client().post('/auth/login/', data=login_user)
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