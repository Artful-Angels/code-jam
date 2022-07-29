from django.urls import path

from .views import create_or_join

urlpatterns = [
    path("createorjoin/", create_or_join, name="createeorjoin"),
]
