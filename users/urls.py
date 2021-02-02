from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users.views import CreateUserView, CurrentUserView

urlpatterns = [
    path('auth/login', obtain_auth_token),
    path('auth/register', CreateUserView.as_view()),
    path('current', CurrentUserView.as_view()),
]
