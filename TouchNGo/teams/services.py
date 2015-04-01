from django.conf import settings
from .models import Team
from firebase_token_generator import create_token
from firebase import firebase


class FirebaseService:
    def createAccount(team):
        #auth_payload = {"uid": str(team.code), "auth_data": team.name}
        auth_payload = {"uid": "Yishai", "auth_data": team.name}
        secret = settings.FIREBASE_SECRET
        token = create_token(secret, auth_payload)
        return token

    def setupFirebaseAccount(self, token):
        fb = firebase.FirebaseApplication(settings.FIREBASE_ROOT, None)
        auth_payload = {"id": "Yishai", "auth_data": "My name"}
        auth = firebase.FirebaseAuthentication(settings.FIREBASE_SECRET,
                                               'random@email.com',
                                               extra=auth_payload)
        fb.authentication = auth
        result = fb.get("/users", None)
        return result
