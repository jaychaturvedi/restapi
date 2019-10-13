from django.urls import path, include
from user.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', UserViewSet)


urlpatterns = [
    path('user',include(router.urls)),
]