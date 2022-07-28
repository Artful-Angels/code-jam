from channels.layers import get_channel_layer
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework.response import Response

from .game_handlers.game_logic import (
    NicknameTaken, add_member_to_game, create_game
)

channel_layer = get_channel_layer()


# Create your views here.
@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def urls_list(request):
    routes = [
        "GET   game/                  ENDPOINTS",
        "POST  createorjoin/          CREATE OR JOIN TO GAME",
    ]
    return Response(routes)


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def create_or_join(request):
    data = {}
    if request.method == "POST":
        game_code = request.data.get("game_code")
        nickname = request.data.get("nickname")
        game_state = cache.get(f"game:{game_code}")
        if game_state:
            try:
                add_member_to_game(game_state, nickname)
            except NicknameTaken:
                data["response"] = "name_error"
                data["message"] = "Name For This Game has Taken, Choice Another One!"
                return Response(data, status=status.HTTP_409_CONFLICT)

            cache.set(f"game:{game_code}", game_state)
            data["response"] = "success_add"
            data["message"] = "New Member Added To the Game Members!!"
            data["game_state"] = game_state
            return Response(data, status=status.HTTP_200_OK)

        game_state = create_game(int(game_code))
        add_member_to_game(game_state, nickname)
        # game_logic = {
        #     "1": {
        #         "is_opend": False,
        #         "is_mine": False,
        #         "is_flaged": False,
        #         "name_num": 2,
        #     },
        # }

        # game_members = {
        #     nickname: {"name": nickname, "is_alive": True},
        # }
        cache.set(f"game:{game_code}", game_state)
        # cache.set(f"game:members:{game_code}", game_members)

        data["response"] = "success_creat"
        data["message"] = "New Game Created!!"
        return Response(data, status=status.HTTP_200_OK)

    data["response"] = "error"
    data["message"] = "Bad request error with the request"
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
