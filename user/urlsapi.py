from django.urls import path, include
from user.views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('', UserViewSet)


# urlpatterns = [
#     path('user',include(router.urls)),
# ]

app_name = 'user'

urlpatterns = [
    path('me/', ManageUserView.as_view(), name='me'),
    path('create/',CreateUserView.as_view(), name='create'),
    path('token/',CreateTokenView.as_view(), name='token'),
]