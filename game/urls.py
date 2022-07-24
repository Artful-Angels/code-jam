
from django.urls import path
from .views import UrlsList,CreatOrJoin
urlpatterns = [
    path('',UrlsList,name="urlslist"),
    path('createorjoin/',CreatOrJoin,name="createeorjoin")
]
