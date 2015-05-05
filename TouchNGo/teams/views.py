#from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from teams.models import Team, Member, Administrator
from teams.serializers import UserSerializer, \
    TeamSerializer, TeamMemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @detail_route(methods=['post'])
    def disableUser(self, request, pk=None):
        response = self.response()
        team = self.get_object()
        uid = request.DATA['phone_number']

        admin = request.user
        adminInTeam = Administrator.objects.filter(teams=team, user=admin)


        if(adminInTeam.count() == 0):
            response.status_code=status.HTTP_401_UNAUTHORIZED
            response.data = {'message' :'User is not allowed to manipulate a foreign team'}

            return response

        relevantMembers = Member.objects.filter(team=team, phone_number=uid)
        if(relevantMembers.count() != 1):
            response.status_code = status.HTTP_400_BAD_REQUEST
            response.data = {'message': 'Team member not found'}
        else:
            member = relevantMembers[0]
            member.active = False
            member.save()
            response.status_code = status.HTTP_200_OK
            data = {'message': 'Team member has been disabled'}

        return response


class TeamAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = TeamMemberSerializer
