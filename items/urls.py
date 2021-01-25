from django.urls import path

from .views import item_detail


urlpatterns = [
    path('<pk>', item_detail)
]
