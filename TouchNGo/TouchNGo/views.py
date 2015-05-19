import random
#from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from rest_framework import viewsets, status
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from teams.serializers import UserSerializer
from teams.models import Team, Member
from smsManager.actions import NexmoClient as smsActions


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

#class GroupViewSet(viewsets.ModelViewSet):
 #   queryset = Group.objects.all()
  #  serializer_class = GroupSerializer


class getCsrf(APIView):
    def get(self, request, *args, **kwargs):
        c = {}
        c.update(csrf(request))
        return Response(csrf(request))
    #return JsonResponse({"csrf": csrf(request)})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def create_auth(request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        User.objects.create_user(
            email=serialized.initial_data['email'],
            username=serialized.initial_data['username'],
            password=serialized.initial_data['password'],
            first_name=serialized.initial_data['first_name'],
            last_name=serialized.initial_data['last_name']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
@permission_classes((AllowAny, ))
def initializeDevice(request):
    teamCode = request.DATA['team']
    number = request.DATA['phone_number']
    memberQS = Member.objects.filter(team__code=teamCode, phone_number=number)
    #querySet = Team.objects.filter(code=teamCode, members__phone_number=number)
    if(memberQS.count() != 1):
        data = {"message": "A team with code \""+teamCode+"\" does not  have "
                           "member with the phone number "+number}
        responseStatus = status.HTTP_400_BAD_REQUEST
    else:
        member = memberQS[0]
        code = member.assignVerCode()
        recipient = member.phone_number

        teamQS = Team.objects.filter(code=teamCode)
        team = teamQS[0]
        messageContent = "Verification code for team \"%s\" \
                             (%s) is %s" % (team.name, team.code, code)
        #smsResponse = smsActions.sendMessage(recipient, messageContent)
        smsResponse = 200
        if(smsResponse == 200):
            data = "Team member now active"
            responseStatus = status.HTTP_200_OK
        else:
            data = "Failure in sending verification code to %s. code: %s"  \
                   % (recipient, smsResponse)
            responseStatus = status.HTTP_502_BAD_GATEWAY
    return Response(data=data, status=responseStatus)


@api_view(['post'])
@permission_classes((AllowAny, ))
def activateDevice(request):
    teamCode = request.DATA['team']
    phoneNumber = request.DATA['phone_number']
    verCode = request.DATA['ver_code']
    udid = request.DATA['udid']
    memberQS = Member.objects.filter(team__code=teamCode,
                                     phone_number=phoneNumber,
                                     ver_code=verCode)
    if(memberQS.count() != 1):
        data = "Unautorized: Code %s for phone number %s in " \
               "team %s is invalid" % \
               (verCode, phoneNumber, teamCode)
        responseStatus = status.HTTP_400_BAD_REQUEST
    else:
        member = memberQS[0]
        member.active = True
        member.udid = udid
        member.save()
        data = "Device has been activated"
        responseStatus = status.HTTP_200_OK

    return Response(data=data, status=responseStatus)
