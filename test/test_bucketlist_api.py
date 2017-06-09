import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
import json
from manage import db, app
from config import TestingConfig

class BucketlistTestCase(unittest.TestCase):
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

    def login_user(self, email="joan.awinja@andela.com", password="Awinja@1"):
        user = {
            "email": email,
            "password": password
        }
        return self.client.post('/auth/login', data=json.dumps(user), content_type='application/json')

    def test_post_bucketlist(self):
        """Test API can create a bucketlist (POST request)"""
        self.register_user()
        result = self.login_user()
        token = json.loads(result.get_data(as_text=True))['Authorization']

        bucket = {"title": "Bunjee Jumping"}
        response = self.client.post('/bucketlists/', data=json.dumps(bucket), headers={'Content-Type': 'application/json','Authorization': token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Bunjee', str(response.data))

    def test_api_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        self.register_user()
        result = self.login_user()
        token = json.loads(result.get_data(as_text=True))['Authorization']

        bucket = {"title": "Go to Maaasai mara"}
        response = self.client.post('/bucketlists/', data=json.dumps(bucket), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response.status_code, 201)

        get_all_response = self.client.get('/bucketlists/', headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(get_all_response.status_code, 200)
        self.assertIn('Go to Maaasai mara', str(get_all_response.data))

    # def test_get_bucketlist_by_id(self):
    #     """Test API can get a single bucketlist by using it's id."""
    #     self.register_user()
    #     result = self.login_user()
    #     token = json.loads(result.get_data(as_text=True))['Authorization']
    #
    #     bucketlist = {"title": "Go to Dubai"}
    #     response1 = self.client.post('/bucketlists/', data=json.dumps(bucketlist), headers={'Content-Type': 'application/json', 'Authorization': token})
    #     self.assertEqual(response1.status_code, 201)
    #
    #     id = json.loads(response1.get_data(as_text=True))['id']
    #     response2 = self.client.get('/bucketlists/' + str(id), headers={'Content-Type': 'application/json','Authorization':token})
    #     self.assertEqual(response2.status_code, 200)
    #     self.assertIn('Go to Dubai', str(result.data))
    #


    def test_put_bucketlist(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        token = json.loads(result.get_data(as_text=True))['Authorization']

        bucketlist= {'title': 'Go to Kerita Forest'}
        response=self.client.post('/bucketlists/', data=json.dumps(bucketlist), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response.status_code, 201)

        id = json.loads(response.get_data(as_text=True))['id']
        bucketlist2 = {"title": "Go to Kerita forest and zip line!"}
        response2 = self.client.put('/bucketlists/' + str(id), data=json.dumps(bucketlist2), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response2.status_code, 201)
        self.assertIn('and zip line!', str(response2.data))

    def test_delete_bucketlist(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        token = json.loads(result.get_data(as_text=True))['Authorization']

        bucketlist= {'title': 'Finding Emo'}
        response = self.client.post('/bucketlists/', data=json.dumps(bucketlist), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response.status_code, 201)

        id = json.loads(response.get_data(as_text=True))['id']
        response2 = self.client.delete('/bucketlists/' + str(id), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response2.status_code, 200)

        # # Test to see if it exists, should return a 404
        # result = self.client.get('/bucketlists/1', headers={'Content-Type': 'application/json','Authorization':token})
        # self.assertEqual(result.status_code, 404)

#sadpath
     def test
         pass

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()