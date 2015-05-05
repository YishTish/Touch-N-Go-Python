from django.conf import settings
from firebase_token_generator import create_token
from firebase import firebase


class FirebaseService:
    def getToken(self, team):
        #auth_payload = {"uid": str(team.code), "auth_data": team.name}
        code = team.code
        auth_payload = {"uid": "python-server", "team_code": code}
        secret = settings.FIREBASE_SECRET
        token = create_token(secret, auth_payload)
        return token

    def setupFirebaseAccount(self):
        fb = firebase.FirebaseApplication(settings.FIREBASE_ROOT, None)
        auth_payload = {"id": "Yishai", "auth_data": "My name"}
        auth = firebase.Authentication(settings.FIREBASE_SECRET,
                                       'backend@touchngo.io',
                                       extra=auth_payload)
        fb.authentication = auth
        result = fb.get("/users", None, {'print': 'pretty'})
        return result

    def getUsers(self, team):
        fb = firebase.FirebaseApplication(settings.FIREBASE_ROOT, None)
        token = self.getToken(team)
        users = fb.get("/users", "", params={'auth': token,
                                             'print': 'pretty'}
                       )
        return users

    def addTeam(self, team):
        fb = firebase.FirebaseApplication(settings.FIREBASE_ROOT, None)
        token = self.getToken(team)
        dataToSave = {
            'name': team.name,
            'code': team.code
        }
        fb.put("/teams", team.code, dataToSave, params={'auth': token})
        return True

    def getTeam(self, team):
        fb = firebase.FirebaseApplication(settings.FIREBASE_ROOT, None)
        token = self.getToken(team)
        team = fb.get("/teams/"+team.code, "", params={'auth': token,
                                                       'print': 'pretty'}
                      )
        return team

    def removeTeam(self, team):
        fb = firebase.FirebaseApplication(settings.FIREBASE_ROOT, None)
        token = self.getToken(team)
        fb.delete("/teams/", name=team.code, params={'auth': token})
        return True
