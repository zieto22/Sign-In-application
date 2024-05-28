import unittest
from app import app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        # Tear down any test-specific setup
        pass

    def test_index_page(self):
        # Test if the index page loads correctly
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
