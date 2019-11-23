import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

from app import APP
from .database.models import setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.casting_assistant='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJVSTNOVUl6UTBVMU4wVTFNVFV3TmtVd1JUaEZNalUwUWtaRk9VRkdOa1JHUVRZM016Y3pSQSJ9.eyJpc3MiOiJodHRwczovL2NvZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkOTBjNGZjNDAxNWYwZWZkOGNiNzBhIiwiYXVkIjoiL2Nhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1NzQ1MTQ1NTUsImV4cCI6MTU3NDYwMDk1NSwiYXpwIjoidjlsbkxjeHNwNnNRM3NQT1NkcFJxb1d0VThZUUxkbWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.O7yQq4IgV1H1Mb4zNow01aJ_PCiiXh1q_BLwFX1FDHb3AlMxqf4Q_4CResDP4Y42QWbS0MHvw3M470o53-EjyZiTYS7IPPem-HkI7fFGyrQ2PuZqdXGYQp3SkLMBqY3V58Qr1v0psqw51ZUnVL3AhrctFmhUsFZAEVlU7nOnVd1FufIWcScGPZhPfERAWqQyq18qjbiC6iRFEeGrDuNyUyKwKu_c57StAZa3eSilZ8jmFmMqN6fR0hOL3c5jNEbrQrcEatv47UwLCKAgCn01G_D7xMGbZxtHaDsd1KtPEpKI-i7rypeGLU2TG47Ut6dXBst10DkpGK4NzYCkPtS3vw'
        self.executive_producer_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJVSTNOVUl6UTBVMU4wVTFNVFV3TmtVd1JUaEZNalUwUWtaRk9VRkdOa1JHUVRZM016Y3pSQSJ9.eyJpc3MiOiJodHRwczovL2NvZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkOTBjNGZjNDAxNWYwZWZkOGNiNzBhIiwiYXVkIjoiL2Nhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1NzQ1MTQ0MzcsImV4cCI6MTU3NDYwMDgzNywiYXpwIjoidjlsbkxjeHNwNnNRM3NQT1NkcFJxb1d0VThZUUxkbWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDptb3ZpZSIsImNyZWF0ZTphY3RvciIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.fdVr2PG7IYYVPIJMypWkJ_-Xa4e-ixvG20_hTXVgo1iXByYDMS_QhEwmSJpHjf58IvhoyghdqoSBQQktvgRc2VwN43mENlz2KlarC-L82auEntvPMCXAqUVygkROg1WZ1n-KOSw4z-Nyfs125ujLY3t_0NZpRMJhu-HarujfcdxpQkHxJKOcIMxVuhmgo7Qk5jTZ9MfdL5mqbSk_PAFOaOJUvT_aPBLvjlAPkRT8rfYc-VW9rXRFHbkxlprxHaz__HbCo1O8mQKX-2jjJ3FCFV31d2EyMDlHjsSfvZER4rfYICzdKmJ8DTFMSnXrgmFQidzdr3U46FNMQ9ODkYKEKA'
        self.casting_director='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJVSTNOVUl6UTBVMU4wVTFNVFV3TmtVd1JUaEZNalUwUWtaRk9VRkdOa1JHUVRZM016Y3pSQSJ9.eyJpc3MiOiJodHRwczovL2NvZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkOTBjNGZjNDAxNWYwZWZkOGNiNzBhIiwiYXVkIjoiL2Nhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1NzQ1MTQ1MDEsImV4cCI6MTU3NDYwMDkwMSwiYXpwIjoidjlsbkxjeHNwNnNRM3NQT1NkcFJxb1d0VThZUUxkbWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvciIsImRlbGV0ZTphY3RvciIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.SXg98xtbTxSIm35BjqfyUvgf0NPncIEtSddM1kzYqVkEU53zRlcAmFPOPFal4odzi_Hdl9Lr2pMw6tWGbQp-iaAIcRx9bK2Mb_153meFI84a0eAbQ44RfGYuhPTqoLaE64V7FV-0NxwddAdQagX5ehwH-TRye8u9SVTXHtcHWdAHb5FRiExdzZ-lVy20dvZVN-FXfhzVFpq4yu1ilLt3Us_lwZaGb72CEIkX8aDgyFTD7a13v-pINmSu1U1taJPw0FRO3eamwdTfpzy2K7E3CZIyd5A23dpdTLAUd8TkKgFUn6z67JLRHDLVSWh20QmlnE4tOW8fQaOK6T8FvLqf4Q'

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_actors(self):
        response = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        response = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_create_actors_with_casting_assistant_token(self):
        payload = {
            'name': 'Abioye',
            'gender': 'non-binary',
            'age': 25
        }
        response = self.client().post('/actors', json=payload, headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        self.assertEqual(response.status_code, 401)
  
    def test_create_movies_with_casting_assistant_token(self):
        payload = {
            'title': 'His Dark Material',
            'release_date': '20th November 2019'
        }
        response = self.client().post('/movies', json=payload, headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        self.assertEqual(response.status_code, 401)

    def test_create_movies_with_casting_director_token(self):
        payload = {
            'title': 'His Dark Material',
            'release_date': '20th November 2019'
        }
        response = self.client().post('/movies', json=payload, headers={"Authorization": "Bearer {}".format(self.casting_director)})
        self.assertEqual(response.status_code, 401)

    def test_create_actors(self):
        payload = {
            'name': 'Abioye',
            'gender': 'non-binary',
            'age': 25
        }
        response = self.client().post('/actors', json=payload, headers={"Authorization": "Bearer {}".format(self.casting_director)})
        self.assertEqual(response.status_code, 200)

    def test_create_movies(self):
        payload = {
            'title': 'His Dark Material',
            'release_date': '20th November 2019'
        }
        response = self.client().post('/movies', json=payload, headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        self.assertEqual(response.status_code, 200)

    def test_update_actors_with_casting_assistant_token(self):
        payload = {
            'name': 'Abioye T',
            'gender': 'male',
            'age': 23
        }
        response = self.client().patch('/actors/1', json=payload, headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        self.assertEqual(response.status_code, 401)

    def test_update_movies_with_casting_assistant_token(self):
        payload = {
            'release_date': '14th November 2019'
        }
        response = self.client().patch('/movies/1', json=payload, headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        self.assertEqual(response.status_code, 401)

    def test_update_actors(self):
        payload = {
            'name': 'Abioye T',
            'gender': 'male',
            'age': 23
        }
        response = self.client().patch('/actors/1', json=payload, headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        self.assertEqual(response.status_code, 200)

    def test_update_movies(self):
        payload = {
            'release_date': '14th November 2019'
        }
        response = self.client().patch('/movies/1', json=payload, headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        self.assertEqual(response.status_code, 200)

    def test_delete_actor_with_casting_assistant_token(self):
        res = self.client().delete('/actors/1', headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        self.assertEqual(res.status_code, 401)

    def test_delete_movies_with_casting_assistant_token(self):
        res = self.client().delete('/movies/1', headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        self.assertEqual(res.status_code, 401)

    def test_delete_movies_with_casting_director_token(self):
        res = self.client().delete('/movies/1', headers={"Authorization": "Bearer {}".format(self.casting_director)})
        self.assertEqual(res.status_code, 401)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_delete_movies(self):
        res = self.client().delete('/movies/1', headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()