from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.request import Request
from teams.models import Team, Administrator, Member
from rest_framework.authtoken.models import Token
from teams.services import FirebaseService


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.StringRelatedField(many=True)
    administrators = serializers.StringRelatedField(many=True)

    class Meta:
        model = Team
        fields = ('name', 'code', 'firebase_path',
                  'firebase_token', 'members', 'administrators')

    def create(self, validated_data):
        req = self.context['request']
        data = {'name': validated_data['name'],
                'administrator': req.user}
        team = Team.objects.create_team(data)
        firebaseToken = FirebaseService.createAccount(team)
        team.firebase_token = firebaseToken
        team.save()
        return team


class TeamMemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Member
        fields = ('team_code', 'name', 'phone_number')
