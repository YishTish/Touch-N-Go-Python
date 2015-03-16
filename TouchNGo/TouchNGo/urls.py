from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from smsManager import views as sms_views
from teams import views as team_views
import TouchNGo.views as views

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'teams', team_views.TeamViewSet)
router.register(r'administrators', team_views.TeamAdminViewSet)
#router.register(r'sendSms', views.SendSms.as_view)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'sendSms', sms_views.SendSms.as_view(), name="sendSms"),
    url(r'getCsrf', views.getCsrf.as_view(), name="getCsrf"),
]
