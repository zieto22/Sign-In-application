import unittest
from app import app

class BasicTestCase(unittest.TestCase):
    """
    A basic test case for the Todo-list application.
    """

    def setUp(self):
        """
        Set up the test case by configuring the app for testing and creating a test client.
        """
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        """
        Clean up after the test case.
        """
        pass

    def test_index_page(self):
        """
        Test the index page of the application.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
