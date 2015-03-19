#from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.context_processors import csrf
from rest_framework import viewsets
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
from smsManager.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class getCsrf(APIView):
    def get(self, request, *args, **kwargs):
        c = {}
        c.update(csrf(request))
        return Response(csrf(request))
    #return JsonResponse({"csrf": csrf(request)})
