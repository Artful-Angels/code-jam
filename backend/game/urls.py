
from django.urls import path
from .views import UrlsList
urlpatterns = [
    path('',UrlsList,name="urlslist")
]
