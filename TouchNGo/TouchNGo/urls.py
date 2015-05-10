from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework_nested import routers

from smsManager import views as sms_views
from teams import views as team_views
import TouchNGo.views as tng_views

#admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'users', tng_views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'teams', team_views.TeamViewSet)
#router.register(r'teams/:id/members/:memberId', team_views.TeamMemberViewSet)
router.register(r'members', team_views.TeamMemberViewSet)
router.register(r'administrators', team_views.TeamAdminViewSet)
#router.register(r'sendSms', views.SendSms.as_view)

# membersRouter = routers.NestedSimpleRouter(router, r'teams', lookup='teams')
# membersRouter.register(r'members', team_views.TeamMemberViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
   # url(r'^', include(membersRouter.urls)),
    url(r'api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'login/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'sendSms', sms_views.SendSms.as_view(), name="sendSms"),
#    url(r'getCsrf', views.getCsrf.as_view(), name="getCsrf"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'register/', tng_views.create_auth, name="register"),
]
