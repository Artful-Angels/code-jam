from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def UrlsList(request):
    routes = [
        'GET   /game/                  ENDPOINTS',
    ]
    return Response(routes)