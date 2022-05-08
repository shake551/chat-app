from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializer import ChatSerializer

import sys

from .utils.chat_room import change_room_name_to_user_name

sys.path.append('../')
from accounts.utils.auth import JWTAuthentication
from accounts.utils.auth import obtain_id_from_jwt


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_room(request):
    room_name = request.data['room_name']
    room_members = request.data['room_members']

    room = ChatSerializer.create_room(room_name=room_name, user_id_list=room_members)

    res = {
        'room': room,
        "token": request.auth
    }

    return JsonResponse(res, status=201)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def post_msg(request):
    ChatSerializer.RoomMessageSerializer.post_message(
        message=request.data['message'],
        room_id=request.data['room_id'],
        user_id=request.data['user_id']
    )

    return JsonResponse({}, status=201)


# 全roomの取得
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtain_all_rooms(request):
    rooms = ChatSerializer.RoomSerializer.obtain_all_room_list()

    res = {
        "rooms": rooms,
        "token": request.auth
    }

    return JsonResponse(res, status=201)


# ログインユーザーの全room取得
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtain_user_rooms(request):
    jwt_token = get_authorization_header(request).split()[1]
    user_id = obtain_id_from_jwt(jwt_token=jwt_token)

    rooms = ChatSerializer.RoomMemberSerializer.obtain_user_room(user_id=user_id)

    change_room_name_to_user_name(rooms=rooms, user_id=user_id)

    res = {
        "rooms": rooms,
        "token": request.auth
    }
    return JsonResponse(res, status=201)


# ルームのメッセージ取得
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtain_room_msg(request, room_id):
    messages = ChatSerializer.RoomMessageSerializer.obtain_room_message(room_id=room_id)

    room = ChatSerializer.RoomSerializer.obtain_room(room_id=room_id)

    jwt_token = get_authorization_header(request).split()[1]
    user_id = obtain_id_from_jwt(jwt_token=jwt_token)

    change_room_name_to_user_name(rooms=room, user_id=user_id)

    res = {
        "room": room,
        "messages": messages,
        "token": request.auth
    }

    return JsonResponse(res, status=200)
