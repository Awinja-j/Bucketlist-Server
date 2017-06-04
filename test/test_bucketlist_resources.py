import unittest

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

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    # Make the tests conveniently executable
    if __name__ == "__main__":
        unittest.main()