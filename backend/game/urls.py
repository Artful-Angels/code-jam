from django.urls import path

from .views import create_or_join, urls_list

urlpatterns = [
    path('', urls_list, name="urlslist"),
    path('createorjoin/', create_or_join, name="createeorjoin")
]
