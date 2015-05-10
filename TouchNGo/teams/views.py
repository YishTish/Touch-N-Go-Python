#from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from teams.models import Team, Member, Administrator
from teams.serializers import UserSerializer, \
    TeamSerializer, TeamMemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def _changeUserStatus(self, team, request, newStatus):
        admin = request.user
        uid = request.DATA['phone_number']
        adminInTeam = Administrator.objects.filter(teams=team, user=admin)

        if(adminInTeam.count() == 0):
            status_code = status.HTTP_401_UNAUTHORIZED
            data = {
                'message': 'User is not allowed to \
                manipulate a foreign team'
            }

        else:
            relevantMembers = Member.objects.filter(team=team,
                                                    phone_number=uid)
            if(relevantMembers.count() != 1):
                status_code = status.HTTP_400_BAD_REQUEST
                data = {'message': 'Team member not found'}
            else:
                member = relevantMembers[0]
                member.active = newStatus
                member.save()
                status_code = status.HTTP_200_OK
                data = {'message': 'Team member has been disabled'}

        return Response(data=data, status=status_code)

    @detail_route(methods=['post'])
    def disableUser(self, request, pk=None):
        team = self.get_object()
        return self._changeUserStatus(team, request, False)

    @detail_route(methods=['post'])
    def enableUser(self, request, pk=None):
        team = self.get_object()
        return self._changeUserStatus(team, request, True)



class TeamAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = TeamMemberSerializer

    # def list(self, request, team_pk=None):
    #     response = self.response()
    #     members = self.queryset.filter(team=team_pk)
    #     response.status_code = status.HTTP_200_OK
    #     response.data = {"response": "Ok", "members_count": members.count()}
    #     return response

    # def create(self, request, team_pk=None):

    #     pass

    # def retrieve(self, request, pk=None, team_pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
