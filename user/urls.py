from django.urls import path
from user.views import *

urlpatterns = [
    path('', user_list, name='user_list'),
    path('<int:id>/details/', user_details, name="user_details"),
    path('<int:id>/edit/', user_edit, name="user_edit"),
    path('add/', user_add, name="user_add"),
    path('<int:id>/delete/', user_delete, name="user_delete"),
]