import unittest

from app import app
from config import *


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def requestHeadersAssistant(self):
        AUTH_TOKEN = 'Bearer ' + CASTING_ASSISTANT
        REQUEST_HEADER = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': AUTH_TOKEN}
        return REQUEST_HEADER
    
    def requestHeadersDirector(self):
        AUTH_TOKEN = 'Bearer ' + CASTING_DIRECTOR
        REQUEST_HEADER = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': AUTH_TOKEN}
        return REQUEST_HEADER
    
    def requestHeadersProducer(self):
        AUTH_TOKEN = 'Bearer ' + EXECUTIVE_PRODUCER
        REQUEST_HEADER = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': AUTH_TOKEN}
        return REQUEST_HEADER

    def setUp(self):
        self.database_path = SQLALCHEMY_DATABASE_URI
        self.app = app
        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_page_not_found(self):
            res = self.client().get('/test_endpoint')
            self.assertEqual(res.status_code, 404)

    def test_create_actor(self):
        info = {"name": "New Actor", "age": 45, "gender": "MALE"}
        res = self.client().post('/actors/create', data=info, headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 200)

    def test_create_actor_error(self):
        info = {"name": "New Actor"}
        res = self.client().post('/actors/create', data=info, headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 500)

    def test_create_actor_error_RBAC(self):
        info = {"name": "New Actor", "age": 45, "gender": "MALE"}
        res = self.client().post('/actors/create', data=info, headers=self.requestHeadersAssistant())
        self.assertEqual(res.status_code, 403)

    def test_create_movie(self):
        info = {"name": "New Movie", "release_date": "2024-03-24 21:37:56"}
        res = self.client().post('/movies/create', data=info, headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 200)

    def test_create_movie_error(self):
        info = {"release_date": "2024-03-24 21:37:56"}
        res = self.client().post('/movies/create', data=info,  headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 500)

    def test_create_movie_error_RBAC(self):
        info = {"release_date": "2024-03-24 21:37:56"}
        res = self.client().post('/movies/create', data=info, headers=self.requestHeadersDirector())
        self.assertEqual(res.status_code, 403)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.requestHeadersAssistant())
        self.assertEqual(res.status_code, 200)

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.requestHeadersAssistant())
        self.assertEqual(res.status_code, 200)

    def test_search_movies(self):
        info = {"search_term": "test"}
        res = self.client().post('/movies/search', data=info, headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 200)

    def test_search_actors(self):
        info = {"search_term": "test"}
        res = self.client().post('/actors/search', data=info, headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 200)

    def test_edit_movies(self):
        info = {"name": "New Movie", "release_date": "2024-03-24 21:37:56"}
        info_updated = {"name": "New Movie modified", "release_date": "2024-04-30 21:37:56"}
        res = self.client().post('/movies/create', data=info, headers=self.requestHeadersProducer())
        id = res.get_json().get('created')
        res = self.client().patch('/movies/{}/edit'.format(id), data=info_updated, headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 200)

    def test_edit_movies_error(self):
        info = {"name": "New Movie", "release_date": "2024-03-24 21:37:56"}
        info_updated = {"name": "New Movie modified", "release_date": "2024-04-30 21:37:56"}
        res = self.client().post('/movies/create', data=info, headers=self.requestHeadersProducer())
        id = res.get_json().get('created')
        res = self.client().patch('/movies/{}/edit'.format(id), data=info_updated, headers=self.requestHeadersAssistant())
        self.assertEqual(res.status_code, 403)

    def test_edit_actors(self):
        info = {"name": "New Actor", "age": 45, "gender": "MALE"}
        info_updated = {"name": "New Actor modified", "age": 34, "gender": "FEMALE"}
        res = self.client().post('/actors/create', data=info, headers=self.requestHeadersDirector())
        id = res.get_json().get('created')
        res = self.client().patch('/actors/{}/edit'.format(id), data=info_updated, headers=self.requestHeadersDirector())
        self.assertEqual(res.status_code, 200)

    def test_edit_actors_error(self):
        info = {"name": "New Actor", "age": 45, "gender": "MALE"}
        info_updated = {"name": "New Actor modified", "age": 34, "gender": "FEMALE"}
        res = self.client().post('/actors/create', data=info, headers=self.requestHeadersDirector())
        id = res.get_json().get('created')
        res = self.client().patch('/actors/{}/edit'.format(id), data=info_updated, headers=self.requestHeadersAssistant())
        self.assertEqual(res.status_code, 403)

    def test_delete_movies(self):
        info = {"name": "New Movie", "release_date": "2024-03-24 21:37:56"}
        res = self.client().post('/movies/create', data=info, headers=self.requestHeadersProducer())
        id = res.get_json().get('created')
        res = self.client().delete('/movies/{}'.format(id), headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 200)

    def test_delete_actors(self):
        info = {"name": "New Actor", "age": 45, "gender": "MALE"}
        res = self.client().post('/actors/create', data=info, headers=self.requestHeadersDirector())
        id = res.get_json().get('created')
        res = self.client().delete('/actors/{}'.format(id), headers=self.requestHeadersDirector())
        self.assertEqual(res.status_code, 200)

    def test_delete_movies_error(self):
        id = -22
        res = self.client().delete('/movies/{}'.format(id), headers=self.requestHeadersProducer())
        self.assertEqual(res.status_code, 404)

    def test_delete_actors_error(self):
        id = -34
        res = self.client().delete('/actors/{}'.format(id), headers=self.requestHeadersDirector())
        self.assertEqual(res.status_code, 404)

    def test_delete_movies_error_RBAC(self):
        info = {"name": "New Movie", "release_date": "2024-03-24 21:37:56"}
        res = self.client().post('/movies/create', data=info, headers=self.requestHeadersProducer())
        id = res.get_json().get('created')
        res = self.client().delete('/movies/{}'.format(id), headers=self.requestHeadersAssistant())
        self.assertEqual(res.status_code, 403)

    def test_delete_actors_error_RBAC(self):
        info = {"name": "New Actor", "age": 45, "gender": "MALE"}
        res = self.client().post('/actors/create', data=info, headers=self.requestHeadersDirector())
        id = res.get_json().get('created')
        res = self.client().delete('/actors/{}'.format(id), headers=self.requestHeadersAssistant())
        self.assertEqual(res.status_code, 403)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()