#from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import APIView
from smsManager.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from django.http import Http404, JsonResponse


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SendSms(APIView):

    def get(self, request, *args, **kwargs):
        return Response({"key": "get"})

    def post(self, request, *args, **kwargs):
        jsonData = JSONParser().parse(request)
        activityKey = jsonData['key']
        phone = jsonData['phone']
        clientPath = "https://resplendent-fire-842.firebaseapp.com" \
                     "client.html#/?case="+activityKey
        from smsManager.actions import NexmoClient
        responseCode = NexmoClient.send(phone, clientPath)
        return JsonResponse({"code":responseCode})
        #return JsonResponse({'a': self.request.query_params.get('phone', 123),
        #                    'b': request.data,
        #                    'c': jsonData})
