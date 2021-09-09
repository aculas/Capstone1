
from unittest import TestCase
from app import app

##############################################################################


class TestCase(TestCase):
    def test_base_route(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('user', html)

    def test_about_route(self):
        with app.test_client() as client:
            resp = client.get('/about', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('software engineer', html)

    def test_artists_route(self):
        with app.test_client() as client:
            resp = client.get('/artists', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('username', html)
