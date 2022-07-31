from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework.response import Response

from .game_handlers.game_logic import (
    GameStarted, NicknameTaken, add_member_to_game, create_game
)


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def create_or_join(request):
    # Check the request method
    if request.method == "POST":
        game_code = request.data.get("game_code")
        nick_name = request.data.get("nickname")
        game_state = cache.get(f"game:{game_code}")
        # Check if the game already in the cache
        if game_state:
            try:
                add_member_to_game(game_state, nick_name)
            except NicknameTaken:
                return Response(status=status.HTTP_409_CONFLICT)
            except GameStarted:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            cache.set(f"game:{game_code}", game_state)
            return Response(status=status.HTTP_200_OK)

        # Create new game
        game_state = create_game(int(game_code))
        add_member_to_game(game_state, nick_name)
        cache.set(f"game:{game_code}", game_state)

        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
