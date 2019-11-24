import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

from app import APP
from database.models import setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.casting_assistant='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJVSTNOVUl6UTBVMU4wVTFNVFV3TmtVd1JUaEZNalUwUWtaRk9VRkdOa1JHUVRZM016Y3pSQSJ9.eyJpc3MiOiJodHRwczovL2NvZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkOTBjNGZjNDAxNWYwZWZkOGNiNzBhIiwiYXVkIjoiL2Nhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1NzQ2MjYxMTcsImV4cCI6MTU3NDcxMjUxNywiYXpwIjoidjlsbkxjeHNwNnNRM3NQT1NkcFJxb1d0VThZUUxkbWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.oxycjfSJXrC00jphjnTiJn5P0HMHLoOBP8m_U6zoRkBPPvrfGOmQ8ydXYmPHlfAUwx7hAlq6Hwywg-8bYWflQHsgSePy88Q5WnO7BJjqgZvkRBYRR8me1Bim6HIUqnOA0o05iV1ZcL9_AtXpZ4RA5-W7YBIDIQ-MGg6846cZzXJ99P8_Q-7piVpXs5ebiYlJzxhA1ZW6i8Fv_mRFPyW-rIkZ8McnbxhHvaaFNWliQBcoHT0fb203EqWNimv1Adl1b_Prp4gh_228jyb2fpTA3KhtrtYR7-SpedLVDw6tEQxVg78gMHEHVRPkTXsgCyjtm23rYzP0W75ltl4mEUIGRA'
        self.executive_producer_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJVSTNOVUl6UTBVMU4wVTFNVFV3TmtVd1JUaEZNalUwUWtaRk9VRkdOa1JHUVRZM016Y3pSQSJ9.eyJpc3MiOiJodHRwczovL2NvZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkOTBjNGZjNDAxNWYwZWZkOGNiNzBhIiwiYXVkIjoiL2Nhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1NzQ2MjYyNzUsImV4cCI6MTU3NDcxMjY3NSwiYXpwIjoidjlsbkxjeHNwNnNRM3NQT1NkcFJxb1d0VThZUUxkbWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDptb3ZpZSIsImNyZWF0ZTphY3RvciIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.YZrKxJ68iG0DULA3iAzm8Eg_ztJA1aXLLYw70sUK39UqrnBY4CrXn4UmxswbBU7lD3M7NwCv0210aINUIPby58xMihWAm8jkJh1sY2A3KQ7wyBV0n0xgQMFNX9Tt022zGyNMJMkhnYi8Yym466mZhgx1pGGxBPSnNRoHUzm7ox9k9k2L2m4MVtsQF4xf7BdpYDKbGtZ3TsyzPEEWg2XAfsiI5ARSboBAqum85RnajK-I8VIoKuXABkkrrR2w5l_jA8SgGUyWzRZM_STDPeAKuTYrOTLGjEyPgMDT3jb_CU_QYV_YS3FzK0wR8yIsIQFp7PL2FoYyNQVu_tigucs9Iw'
        self.casting_director='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJVSTNOVUl6UTBVMU4wVTFNVFV3TmtVd1JUaEZNalUwUWtaRk9VRkdOa1JHUVRZM016Y3pSQSJ9.eyJpc3MiOiJodHRwczovL2NvZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkOTBjNGZjNDAxNWYwZWZkOGNiNzBhIiwiYXVkIjoiL2Nhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1NzQ2MjYyMTcsImV4cCI6MTU3NDcxMjYxNywiYXpwIjoidjlsbkxjeHNwNnNRM3NQT1NkcFJxb1d0VThZUUxkbWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvciIsImRlbGV0ZTphY3RvciIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.jGkJbi6X1AeNT1mp1diweuuk5TmhloFtfe_53I2QOJnRiBKrNLNHz9mgCNgbtoULqwajaAGCYo-APE8aOOszVL1ZX50DX1sEEv9_G2WIUZt0NgOAx7mLnmfEThr7ui0CB4zwLoYfTCH5vbwMqBMH9JNBkZfU1DJKhRtnEpMzRA4gOPHqXQRGgzz6-4ZpXpRE_uPdGcbO_vcYeh69N7Qf6rilZHfX8CV0Y2O2j1265mQTjI95QTVVoPAtII09l2U94aKCY0jMoZgVRazWx8QsAES6vSTTB6cg55S6ZZUOe42mXNB-fNyqT9BedYoD0rFZ58QYAneQb_tV6yUYhTasjA'

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