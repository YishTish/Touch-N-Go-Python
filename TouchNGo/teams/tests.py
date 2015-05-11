from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Team, Administrator, Member
from .services import FirebaseService


class functionalTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "http://localhost:8000"
        self.first_name = 'Yishai'
        self.last_name = 'Landau'
        self.username = 'YishTish'
        self.password = '123456'
        self.email = 'yishail@gmail.com'
        self.teamCode = ""

    def tearDown(self):
        if(self.teamCode != ""):
            team = Team.objects.filter(code=self.teamCode)
            if(team.count() > 0):
                fbService = FirebaseService()
                fbService.removeTeam(team[0])

    def _createUser(self):
        data = {'username': self.username,
                'groups': [],
                'email': self.email,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name,
                }
        response = self.client.post(
            self.url+'/register/', data, format='json')
        return response

    def _createTeam(self, teamName='test team1'):
        self._createUser()
        self._login()
        data = {'name': teamName,
                'members': [],
                'administrators': []}
        response = self.client.post(self.url+'/teams/', data, format='json')
        response.render()
        self.teamCode = response.data['code']
        return response

    def _login(self):
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.url+'/login/', data,
                                    format='json')
        response.render()
        self.client.credentials(
            HTTP_AUTHORIZATION=' JWT '+response.data['token']
        )
        return response.data['token']

    def _createAndGetTeam(self, teamName):
        self._createTeam(teamName)
        team = Team.objects.filter(name=teamName)
        self.assertEqual(team.count(), 1)
        return team[0]

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
        response = self.client.post(self.url+'/login/', data,
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
        teamName = 'test team1'
        team = self._createAndGetTeam(teamName)
        self.assertIsNotNone(team)

    def testTeamHasAdministrator(self):
        teamName = 'test team1'
        team = self._createAndGetTeam(teamName)
        admin = Administrator.objects.filter(teams=team)
        self.assertIsNotNone(admin)
        self.assertGreater(admin.count(), 0)

    def testTeamHasUniqueHexaCode(self):
        teamName = 'test team1'
        team = self._createAndGetTeam(teamName)
        self.assertIsNotNone(team.code)
        self.assertGreater(len(team.code), 0)
        self.assertLess(len(team.code), 7, team.code)

    def testTeamFirebaseToken(self):
        teamName = 'test team1'
        team = self._createAndGetTeam(teamName)
        fbService = FirebaseService()
        token = fbService.getToken(team)
        self.assertIsNotNone(token)

    def testGetUsers(self):
        teamName = 'test team1'
        team = self._createAndGetTeam(teamName)
        fbService = FirebaseService()
        users = fbService.getUsers(team)
        self.assertIsNotNone(users)

    def testCreateTeamOnFirebase(self):
        teamName = 'test team1'
        team = self._createAndGetTeam(teamName)
        fbService = FirebaseService()
        firebaseTeam = fbService.getTeam(team)
        self.assertTrue(firebaseTeam)
        self.assertEqual(firebaseTeam['name'], team.name)

    def testAddUserToFirebase(self):
        self._createUser()
        token = self._login()
        data = {'name': 'my first team',
                'members': [],
                'administrators': []}
        self.client.credentials(
            HTTP_AUTHORIZATION=' JWT '+token
        )
        response = self.client.post(self.url+'/teams/', data, format='json')
        self.assertIsNotNone(response.data['code'])
        self.assertEqual(len(response.data['code']), 6)

    def testAddTeamMember(self):
        self._createUser()
        team = self._createAndGetTeam("My testing team")
        name = 'Member #1'
        phone_number = '1234567890'

        member = Member(team=team, name=name, phone_number=phone_number)
        self.assertIsNotNone(member)

    def testAddTeamMemberViaUrl(self):
        self._createUser()
        token = self._login()
        team = self._createAndGetTeam("My testing team")
        member = {"name": "mike", "phone_number": "1234567890"}
        member2 = {"name": "aike", "phone_number": "1234467890"}

        data = {
            "members": [member, member2],
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=' JWT '+token
        )

        targetUrl = self.url+'/teams/'+str(team.id)+'/'
        response = self.client.patch(targetUrl, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # targetUrl = self.url+'/teams/'+str(team.id)+'/members/'
        # response = self.client.post(targetUrl, data, format='json')
        # print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testRemoveTeamMember(self):
        self._createUser()
        token = self._login()
        team = self._createAndGetTeam("Freeze member")
        member = {"name": "Bob", "phone_number": "123456789"}
        member2 = {"name": "Robert", "phone_number": "987654321"}

        data = {"members": [member, member2]}
        self.client.credentials(HTTP_AUTHORIZATION=' JWT '+token)

        putUrl = self.url+'/teams/'+str(team.id)+'/'
        self.client.patch(putUrl, data, format='json')

        disableUrl = self.url+'/teams/'+str(team.id)+'/removeMember/'
        response = self.client.post(disableUrl,
                                    {"phone_number": "123456789"},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        memberList = Member.objects.filter(phone_number="123456789")
        self.assertEqual(memberList.count(), 0)

    def testEnableTeamMember(self):
        self._createUser()
        token = self._login()
        team = self._createAndGetTeam("Enable member")
        member = {"name": "Bob", "phone_number": "123456789"}

        data = {"members": [member]}
        self.client.credentials(HTTP_AUTHORIZATION=' JWT '+token)
        putUrl = self.url+'/teams/'+str(team.id)+'/'
        self.client.patch(putUrl, data, format='json')

        enableUrl = self.url+'/teams/'+str(team.id)+'/enableUser/'
        response = self.client.post(enableUrl,
                                    {"phone_number": "123456789"},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        memberList = Member.objects.filter(phone_number="123456789")
        member = memberList[0]
        self.assertTrue(member.active)

    def testInitializeMemberDevice(self):
        self._createUser()
        token = self._login()
        team = self._createAndGetTeam("Initialize member device")
        member = {"name": "Bob", "phone_number": "123456789"}
        data = {"members": [member]}
        self.client.credentials(HTTP_AUTHORIZATION=' JWT '+token)
        putUrl = self.url+'/teams/'+str(team.id)+'/'
        self.client.patch(putUrl, data, format='json')
        self.client.logout()

        querySet = Member.objects.filter(team=team, phone_number="123456789")
        inactiveMember = querySet[0]
        self.assertFalse(inactiveMember.active)

        deviceData = {"team": team.code, "phone_number": "123456789"}
        response = self.client.post(
            self.url+"/initializeDevice/",
            deviceData, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        self.assertEqual(response.data, "Code sent by sms")





    def testRegisterMemberDevice(self):
        pass

    def testTeamMemberGetFirebaseToken(self):
        pass

    #def testGetTeamMemebers(self):

    #def testAddTeamAdministrator(self):

    #def testRemoveTeamAdministrator(self):

     # def testGetTeamUsersByTeam(self):
    #     self.assertTrue(None)

    # def testGetTeamUserByOtherTeam(self):
    #     self.assertTrue(None)

    # def testDeleteTeam(self):
    #     self.assertTrue(False)

    # def testTeamHasFirebaseAccount(self):
    #     self._createTeam()
    #     team = Team.objects.filter(name='test team1')
    #     oneTeam = team[0]
    #     token = oneTeam.firebase_token
    #     fbService = FirebaseService()
    #     users = fbService.setupFirebaseAccount()
    #     self.assertTrue(False)
