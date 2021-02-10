from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from users.views import CreateUserView, CurrentUserView

auth_urls = [
    path('login', obtain_auth_token),
    path('register', CreateUserView.as_view()),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('current', CurrentUserView.as_view()),
]
