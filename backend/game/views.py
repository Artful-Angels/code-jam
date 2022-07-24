from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()
# Create your views here.
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def UrlsList(request):
    routes = [
        'GET   game/                  ENDPOINTS',
        'POST  createorjoin/           CREAT OR JOIN TO GAME'
    ]
    return Response(routes)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def CreatOrJoin(request):
    data = {}
    if request.method == "POST":
        game_code = request.data.get("game_code")
        nickname = request.data.get("nickname")
        GameMembers = cache.get(f'game:members:{game_code}')
        if GameMembers:
            if nickname in GameMembers:
                data["response"] = "name_error"
                data["message"] = "Name For This Game has Taken, Choice Another One!"
                return Response(data,status=status.HTTP_409_CONFLICT)

            GameMembers[nickname] = {
                "name":str(nickname),
                "is_alive":True
            }
            cache.set(f'game:members:{game_code}',GameMembers)

            

            data["response"] = "success_add"
            data["message"] = "New Member Added To the Game Members!!"
            data["game_member"] = cache.get(f'game:members:{game_code}')
            data["game_logic"] = cache.get(f'game:logic:{game_code}')
            return Response(data,status=status.HTTP_200_OK)

            
        else:
            GameLogic = {
                "1": {
                    "is_opend":False,
                    "is_mine":False,
                    "is_flaged":False,
                    "name_num":2
                },
            }

            GameMembers = {
                nickname:{
                        "name":nickname,
                        "is_alive":True
                    },
            }
            cache.set(f'game:logic:{game_code}', GameLogic)
            cache.set(f'game:members:{game_code}', GameMembers)

            data["response"] = "success_creat"
            data["message"] = "New Game Created!!"
            return Response(data,status=status.HTTP_200_OK)
    data["message"] = "Error"
    return Response(data)