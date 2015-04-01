#from django.shortcuts import render
from django.contrib.auth.models import User
from teams.models import Team, Member
from rest_framework import viewsets
from teams.serializers import UserSerializer, \
    TeamSerializer, TeamMemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = TeamMemberSerializer
