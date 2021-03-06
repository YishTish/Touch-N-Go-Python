import binascii, os, random
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# User logs in and creates an account - logging in is done with
#		 	an email address and a password.
# Once logged in, User has an option to create a team. This user
#		     is set as the administrator of the team
# Administrators have a name, email address, password, boolean active flag.
# Administrator model is taken from Django.contrib.User model, providing all
#			the user management out of the box
# An administrator can create and manage more than one team
# A team has a name, a 6 hexa-digit code, and Firebase details -
#			path and secret. The 6 hexa-digit code is the name
#			of the Firebase root which will be used for the team
# Once a team is created, the team administrator adds members to the team.
# The back-end application (this, the Django-based app) has two types of
#			users - administrators and team-members.
# Team members consist of name, phone number, device UDID, phone type,
#			and a boolean flag representing activity
# Team members and administrators are not deleted, but their 'active'
#			attribute is set to false.
# An admin can be also a team member - duplicate recods in the table, and
#			 handled seperatley.
# A team can have more than one administrator.
# Administrator adds and disables members and changes team name.
# Each team has a unique Firebase secret that allows access to read and write
#			 from their team's instant
# When a member logs in from their app, their phone UDID is sent to the back-end
# server, to receive a token.
# Tokens are generated by Firebase on a periodical basis - when they expire,
#			the back-end refreshes a new token.
# Once the token is sent to device, all mobile interaction is against Firebase.
# Access to the web dashboard is allowed to administrators, using the same
#			credentials as the back-end application


class common_data(models.Model):
    created = models.DateField(default=datetime.now())
    active = models.BooleanField(default='true')

    class Meta:
        abstract = True


class TeamManager(models.Manager):
    def create_team(self, teamData):
        code = str(binascii.hexlify(os.urandom(3)))
        #The following is a ugly hack to remove the
        #decorators from the returned string.
        #TODO: Find a prettier way
        code = code[2:8]
        firebaseUser = str(code)+'@touchngo.io'
        firebasPassword = str(binascii.hexlify(os.urandom(6)))
        team = self.create(name=teamData['name'],
                           code=code,
                           firebase_user=firebaseUser,
                           firebase_password=firebasPassword)
        teamAdmin = Administrator(user=teamData['administrator'])
        teamAdmin.save()
        #team.administrators.create(user=teamData['administrator'])
        team.save()
        teamAdmin.teams.add(team)
        return team


class Team(common_data):
    code = models.CharField(max_length=10, unique=True, null=True)
    name = models.CharField(max_length=100)
    firebase_path = models.CharField(max_length=64, unique=True, null=True)
    firebase_user = models.CharField(max_length=50, null=True)
    firebase_password = models.CharField(max_length=20, null=True)
    firebase_token = models.CharField(max_length=64, null=True)

    objects = TeamManager()


class Administrator(models.Model):
    teams = models.ManyToManyField(Team)
    #team = models.ForeignKey(Team, related_name='administrators')
    user = models.ForeignKey(User)


class MemberManager(models.Manager):

    def create_member(self, team, name, phone_number,
                      udid=None, active=False, ver_code=None):
        if(ver_code is None):
            ver_code = int((random.random()*10000))
        if(udid is None):
            udid = ""
        member = Member(team=team, name=name, phone_number=phone_number, udid=udid, active=active)
        member.save()
        return member

    # def create(self, memberData):
    #     print("create")

class Member(common_data):
    team = models.ForeignKey(Team, related_name='members')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    udid = models.CharField(max_length=40)
    ver_code = models.IntegerField(default=int(random.random()*10000))

    class Meta:
        unique_together = ("team", "phone_number")

    def assignVerCode(self):
        code = int((random.random()*10000))
        self.ver_code = code
        self.save()
        return code

    objects = MemberManager()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
