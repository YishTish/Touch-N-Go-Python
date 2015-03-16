from django.contrib.auth.models import User
from rest_framework import serializers
import teams.models as teams


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.StringRelatedField(many=True)
    administrators = serializers.StringRelatedField(many=True)

    class Meta:
        model = teams.team
        fields = ('name', 'team_code', 'members', 'administrators')


class TeamMemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = teams.member
        fields = ('team_code', 'name', 'phone_number')
