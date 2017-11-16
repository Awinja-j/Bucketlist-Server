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



class ItemTestCase(unittest.TestCase):
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

    def test_item_creation(self):
        """Test API can create a item (POST request)"""
        self.register_user()
        result = self.login_user()
        token = json.loads(result.get_data(as_text=True))['Authorization']

        bucket = {"title": "Bunjee Jumping"}
        one = self.client.post('/bucketlists/', data=json.dumps(bucket), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(one.status_code, 201)

        id = json.loads(one.get_data(as_text=True))['id']
        item = {"title": "Start with the Aberdares"}
        response = self.client.post('/bucketlists/' + str(id) + '/items', data=json.dumps(item), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Start with the Aberdares', str(response.data))

    def test_item_can_be_edited(self):
        """Test API can edit an existing item. (PUT request)"""
        self.register_user()
        result = self.login_user()
        token = json.loads(result.get_data(as_text=True))['Authorization']

        bucket = {"title": "Go to Kerita Forest"}
        response = self.client.post('/bucketlists/', data=json.dumps(bucket), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response.status_code, 201)

        id = json.loads(response.get_data(as_text=True))['id']
        item = {"title": "Start with the Aberdares"}
        response1 = self.client.post('/bucketlists/' + str(id) + '/items', data=json.dumps(item), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response1.status_code, 201)

        item_id = json.loads(response1.get_data(as_text=True))['id']
        bucketlist_id = json.loads(response1.get_data(as_text=True))['bucketlist_id']
        update = {"title": "Start with the Aberdares and hike 20km!"}
        response2 = self.client.put('/bucketlists/' + str(bucketlist_id) + '/items/' + str(item_id), data=json.dumps(update), headers={'Content-Type': 'application/json','Authorization':token})
        self.assertEqual(response2.status_code, 200)
        self.assertIn('updated succesfully!', str(response2.data))

    # def test_item_deletion(self):
    #     """Test API can delete an existing item. (DELETE request)."""
    #     self.register_user()
    #     result = self.login_user()
    #     token = json.loads(result.get_data(as_text=True))['Authorization']
    #
    #     bucketlist = {"title": "Bunjee Jumping"}
    #     response = self.client.post('/bucketlists/', data=json.dumps(bucketlist), headers={'Content-Type': 'application/json','Authorization':token})
    #     self.assertEqual(response.status_code, 201)
    #
    #     id = json.loads(response.get_data(as_text=True))['id']
    #     item = {"title": "Start with the Aberdares"}
    #     response1 = self.client.post('/bucketlists/' + str(id) + '/items', data=json.dumps(item), headers={'Content-Type': 'application/json','Authorization':token})
    #     self.assertEqual(response1.status_code, 201)
    #
    #     item_id = json.loads(response1.get_data(as_text=True))['id']
    #     bucketlist_id = json.loads(response1.get_data(as_text=True))['bucketlist_id']
    #     delete_response = self.client.delete('/bucketlists/' + str(bucketlist_id) + '/items/' + str(item_id), headers={'Content-Type': 'application/json','Authorization': token})
    #     self.assertEqual(delete_response.status_code, 204)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()