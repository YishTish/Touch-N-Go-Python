from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Team, Administrator
from .services import FirebaseService


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
        return response

    def _createTeam(self):
        self._createUser()
        self._login()
        data = {'name': 'test team1',
                'members': [],
                'administrators': []}
        response = self.client.post(self.url+'/teams/', data, format='json')
        response.render()
        return response

    def _login(self):
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.url+'/api-token-auth/', data,
                                    format='json')
        response.render()
        self.client.credentials(
            HTTP_AUTHORIZATION=' JWT '+response.data['token']
        )
        return response.data['token']

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
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.url+'/api-token-auth/', data,
                                    format='json')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#Creatr new team without authorization
    def testCreateTeamWithoutToken(self):
        self._createUser()
        data = {'name': 'test team',
                'team_code': '12345',
                'members': [],
                'administrators': []}
        response = self.client.post(self.url+'/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testTeamCreation(self):
        response = self._createTeam()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testCreatedTeamExists(self):
        self._createTeam()
        team = Team.objects.filter(name='test team1')
        self.assertIsNotNone(team)

    def testTeamHasAdministrator(self):
        self._createTeam()
        team = Team.objects.filter(name='test team1')
        admin = Administrator.objects.filter(team=team)
        self.assertIsNotNone(admin)
        self.assertGreater(admin.count(), 0)

    def testTeamHasUniqueHexaCode(self):
        self._createTeam()
        team = Team.objects.filter(name='test team1')
        self.assertEqual(team.count(), 1)
        oneTeam = team[0]
        self.assertIsNotNone(oneTeam.code)
        self.assertGreater(len(oneTeam.code), 0)
        self.assertLess(len(oneTeam.code), 7)

    def testTeamHasFirebaseAccount(self):
        self._createTeam()
        team = Team.objects.filter(name='test team1')
        oneTeam = team[0]
        token = oneTeam.firebase_token
        fbService = FirebaseService()
        users = fbService.setupFirebaseAccount(token)
        print(users)
        self.assertTrue(False)


    def testTeamHasFirebaseToken(self):
        self._createTeam()
        team = Team.objects.filter(name='test team1')
        oneTeam = team[0]
        self.assertIsNotNone(oneTeam.firebase_token)
