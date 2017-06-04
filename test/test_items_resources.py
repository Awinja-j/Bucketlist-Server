import unittest


class ItemTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_item_creation(self):
        """Test API can create a item (POST request)"""
        self.client.post('/bucketlists/', data={"title": "Bunjee Jumping"})
        self.item = {"title": "Start with the Aberdares"}
        response = self.client.post('/bucketlists/1/', data=self.item)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Start with the Aberdare', str(res.data))

    def test_api_can_get_all_items(self):
        """Test API can get a item (GET request)."""
        bucket = {"title": "Bunjee Jumping"}
        self.client.post('/bucketlists/', data=bucket)
        item = {"title": "Start with the Aberdares"}
        self.client.post('/bucketlists/1/', data=item)
        get_all_response = self.client.get('/bucketlists/1/')
        self.assertEqual(get_all_response.status_code, 302)
        self.assertIn('Start with the Aberdares', str(res.data))

    def test_api_can_get_items_by_id(self):
        """Test API can get a single item by using it's id."""
        bucket = {"title": "Bunjee Jumping"}
        self.client.post('/bucketlists/', data=bucket)
        item = {"title": "Start with the Aberdares"}
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
        self.item = {"title": "Start with the Aberdares"}
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
        self.item = {"title": "Start with the Aberdares"}
        self.client.post('/bucketlists/1/', data=self.item)
        delete_response = self.client.delete('/bucketlists/1/1/')
        self.assertEqual(delete_response.status_code, 204)
        # Test to see if it exists, should return a 404
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