from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class functionalTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "http://localhost:8000"
        self.username = 'YishTish'
        self.password = '123456'
        self.email = 'yishail@gmail.com'

    def tearDown(self):
        pass

    def _createUser(self):
        data = {'username': self.username,
                'groups': [],
                'email': self.email,
                'password': self.password}
        response = self.client.post(
            self.url+'/users/', data, format='json')
        print("creating user. response code: ", response.status_code)
        return response

#User signs up, becomes admin
    def testRegistration(self):
        response = self._createUser()
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.email, response.data['email'])

#Login with above credentials
    def testLogin(self):
        #Once user has been created, login
        self._createUser()
        self.client.logout()
        user = self.client.login(
            username=self.username,
            password=self.password)
#self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        newResponse = self.client.get('/users/')
        newResponse.render()
        print(newResponse.data)
