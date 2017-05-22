# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
    def test_user(self):
        """this contains all the user functionality"""
        #Test API can create new user(POST request)all credentials
        self.user = {"first_name": "Joan", "last_name" : "Awinja", "email": "joan.awinja@andela.com", "password": "Awinja@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code,201)

        # add user with missing first name
        self.user = {"last_name" : "mwaniki", "email": "josh.mwaniki@andela.com", "password": "josh@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code,201)

        # add user with missing last name
        self.user = {"first_name": "Jones", "email": "jones.ingari@andela.com", "password": "jones@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code,201)

        # add user with missing password
        self.user = {"first_name": "Judy", "last_name" : "Khasoa", "email": "judy.khasoa@andela.com"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code,400)
        
        # add user with missing email
        # The client SHOULD NOT repeat the request without modifications.
        self.user = {"first_name": "Tom", "last_name" : "Nganyi", "password": "Nganyi@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code,400)

        # add user with invalid email format
        # The client SHOULD NOT repeat the request without modifications.
        self.user = {"first_name": "James", "last_name" : "Ochweri", "email": "james.ochweri.com", "password": "Ochweri@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code,400)

        # add duplicate user email
        # The client SHOULD NOT repeat the request without modifications.
        self.user = {"first_name": "John", "last_name" : "Kamau", "email": "joan.awinja@andela.com", "password": "Awinja@1"}
        response = self.client.post('/auth/register/', data=self.user)
        self.assertEqual(response.status_code,400)

    def test_login_user(self):
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
        self.assertEqual(response, status_code, 400)

    def test_login_user_with_wrong_password(self):
        create_user = {"first_name": "James", "last_name" : "Ochweri", "email": "james.o@andela.com", "password": "ochweri@1"}
        create_response = self.client.post('/auth/register/', data=create_user)
        self.assertEqual(create_response.status_code,201)        
        login_user = {"email" : "joan.awinja@andela.com", "password" : "awinja@1"}
        response = self.client().post('/auth/login/', data=login_user)
        self.assertEqual(response, status_code, 401)

    def test_login_user_with_wrong_credentials(self):
        create_user = {"first_name": "James", "last_name" : "Ochweri", "email": "james.o@andela.com", "password": "ochweri@1"}
        create_response = self.client.post('/auth/register/', data=create_user)
        self.assertEqual(create_response.status_code,201)        
        login_user = {"email" : "joan.awinja@andela.com", "password" : "awinja@1"}
        response = self.client().post('/auth/login/', data=login_user)
        self.assertEqual(response, status_code, 401)

    def test_create_bucketlist(self):
        """Test API can create a bucketlist (POST request)"""
        # test add bucketlist
        bucket = {"title": "Bunjee Jumping"}
        response = self.client.post('/bucketlists/', data=bucket)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        bucket = {"title": "Go to Maaasai mara"}
        response = self.client.post('/bucketlists/', data=bucket)
        self.assertEqual(response.status_code, 201)
        get_all_response = self.client().get('/bucketlists/')
        self.assertEqual(get_all_respons.status_code, 302)
        self.assertIn('Go to Maaasai mara', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        bucketlist = {"title": "Go to Dubai"}
        response = self.client.post('/bucketlists/', data=bucketlist)
        self.assertEqual(response.status_code, 201)
        # result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # result = self.client().get(
        #     '/bucketlists/{}'.format(result_in_json['id']))
        result = self.client.get('/bucketlists/1/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Dubai', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        response = self.client.post(
            '/bucketlists/',
            data={'title': 'Go to Kerita Forest'})
        self.assertEqual(response.status_code, 201)
        response2 = self.client().put(
            '/bucketlists/1',
            data={
                "title": "Go to Kerita forest and zip line!"
            })
        self.assertEqual(response2.status_code, 200)
        results = self.client.get('/bucketlists/1')
        self.assertIn('and zip line!', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        response = self.client.post(
            '/bucketlists/',
            data={'title': 'Finding Emo'})
        self.assertEqual(response.status_code, 201)
        response2 = self.client.delete('/bucketlists/1')
        self.assertEqual(response2.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client.get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)
    def test_item_creation(self):
        """Test API can create a item (POST request)"""
        self.client.post('/bucketlists/', data = {"title": "Bunjee Jumping"})
        self.item = {"title" : "Start with the Aberdares"}
        response = self.client.post('/bucketlists/1/', data=self.item)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Start with the Aberdare', str(res.data))
        
    def test_api_can_get_all_items(self):
        """Test API can get a item (GET request)."""
        bucket = {"title": "Bunjee Jumping"}
        self.client.post('/bucketlists/', data=bucket)
        item = {"title" : "Start with the Aberdares"}
        self.client.post('/bucketlists/1/', data=item)
        get_all_response = self.client.get('/bucketlists/1/')
        self.assertEqual(get_all_response.status_code, 302)
        self.assertIn('Start with the Aberdares', str(res.data))

    def test_api_can_get_items_by_id(self):
        """Test API can get a single item by using it's id."""
        bucket = {"title": "Bunjee Jumping"}
        self.client.post('/bucketlists/', data = bucket)
        item = {"title" : "Start with the Aberdares"}
        self.client.post('/bucketlists/1/', data=item)
        get_item_response = self.client.get('/bucketlists/1/1/')
        self.assertEqual(get_item_response.status_code, 200)
        self.assertIn('Start with the Aberdares', str(res.data))

    def test_item_can_be_edited(self):
        """Test API can edit an existing item. (PUT request)"""
        response = self.client.post(
            '/bucketlists/',
            data={"title": "Go to Kerita Forest"})
        self.assertEqual(response.status_code, 201)
        self.item = {"title" : "Start with the Aberdares"}
        self.client.post('/bucketlists/1/', data=self.item)
        response2 = self.client.put(
            '/bucketlists/1/1/',
            data={
                "title": "Start with the Aberdares and hike 20km!"
            })
        self.assertEqual(response2.status_code, 200)
        results = self.client.get('/bucketlists/1')
        self.assertIn('and hike 20km!!', str(results.data))

    def test_item_deletion(self):
        """Test API can delete an existing item. (DELETE request)."""
        bucketlist = {"title": "Bunjee Jumping"}
        response = self.client.post('/bucketlists/', data=bucketlist)
        self.assertEqual(response.status_code, 201)
        self.item = {"title" : "Start with the Aberdares"}
        self.client.post('/bucketlists/1/', data=self.item)
        delete_response = self.client.delete('/bucketlists/1/1/')
        self.assertEqual(delete_response.status_code, 204)
        #Test to see if it exists, should return a 404
        result = self.client.get('/bucketlists/1/1/')
        self.assertEqual(result.status_code, 404)
    

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()