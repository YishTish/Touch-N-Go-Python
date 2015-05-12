import random
#from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from rest_framework import viewsets, status
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from teams.serializers import UserSerializer
from teams.models import Team
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
    querySet = Team.objects.filter(code=teamCode)
    if(querySet.count() != 1):
        data = {"message": "A team with code \""+teamCode+"\" does not exist"}
        responseStatus = status.HTTP_400_BAD_REQUEST
    else:
        rand = int(random.random()*10000)
        recipient = "972549792080"
        team = querySet[0]
        messageContent = "Verification code for team \"%s\" \
                             (%s) is %s" % (team.name, team.code, rand)
        smsResponse = smsActions.sendMessage(recipient, messageContent)
        if(smsResponse == 200):
            data = "Team member now active"
            responseStatus = status.HTTP_200_OK
        else:
            data = "Failure in sending verification code to %s. code: %s"  \
                   % (recipient, smsResponse)
            responseStatus = status.HTTP_502_BAD_GATEWAY
    return Response(data=data, status=responseStatus)
