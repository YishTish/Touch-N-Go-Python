import sys

from django.conf import settings
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

import TouchNGo

for path in sys.path:
    print(path)


class functionalTests(TestCase):

    def setUp(self):
        settings.configure(TouchNGo, DEBUG=True)
        self.client = APIClient()
        self.url = "http://localhost:8000"

    def tearDown(self):
        pass

#User signs up, becomes admin
    def testRegistration(self):
        data = {'username': 'YishTish',
                'email': 'yishail@gmail.com',
                'password': '123456'}
        response = self.client.post(
            self.client + '/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    def testLogin(self):
        pass

#admin creates team

#Team is registered in Firebase, and a secret is \
#    assigned to communicate between server and Firebase

#admin assigns members to the team

#Admin sends sms to team members to download app and sign up

#team member downloads app and inserts team code to authenticate

#Server registers team member

#Server fetches Firebase token for team members

#Admin adds more admin users

#Admin disables team members

#Disabled team member tries to use app

#Admin creates a second team

#Admin disables a team
