#from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.decorators import APIView

from rest_framework.response import Response
from django.http import Http404, JsonResponse

from smsManager.actions import NexmoClient

class SendSms(APIView):

    def get(self, request, *args, **kwargs):
        return Response({"key": "get"})

    def post(self, request, *args, **kwargs):
        jsonData = JSONParser().parse(request)
        activityKey = jsonData['key']
        phone = jsonData['phone']
        clientPath = "https://touchngo.io/" \
                     "client.html#/?case="+activityKey

        responseCode = NexmoClient.send(phone, clientPath)
        return JsonResponse({"code": responseCode})
        #return JsonResponse({'a': self.request.query_params.get('phone', 123),
        #                    'b': request.data,
        #                    'c': jsonData})
