#from django.shortcuts import render
from django.contrib.auth.models import User
from teams.models import team, member
from rest_framework import viewsets
from teams.serializers import UserSerializer, \
    TeamSerializer, TeamMemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = team.objects.all()
    serializer_class = TeamSerializer


class TeamAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = member.objects.all()
    serializer_class = TeamMemberSerializer
