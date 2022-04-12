from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

from .models import Room, RoomMessage, RoomMember
from .serializer import RoomSerializer, RoomMemberSerializer, RoomMessageSerializer

import sys

sys.path.append('../')
from accounts.models import User
from accounts.utils.auth import JWTAuthentication
from accounts.utils.auth import obtain_id_from_jwt


def obtain_user(user_id):
    if User.objects.filter(pk=user_id).exists():
        user_query = User.objects.get(pk=user_id)
        return user_query
    return Exception('user not found')


def obtain_room(room_id):
    if Room.objects.filter(pk=room_id).exists():
        room_query = Room.objects.get(pk=room_id)
        return room_query
    raise Exception('room not found')


def add_user(room_id, user_id):
    user_query = obtain_user(user_id)
    room_query = obtain_room(room_id)
    serializer = RoomMemberSerializer(data={
        'room': room_query.id,
        'user': user_query.id
    })
    if serializer.is_valid():
        room_member = serializer.save()
        res = {
            "room_id": room_member.room.id,
            "user_id": room_member.user.id
        }
        return res
    raise Exception("cannot add user")


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_room(request):
    room_name = request.data['room_name']
    room_members = request.data['room_members']

    res = {}
    try:
        with transaction.atomic():
            serializer = RoomSerializer(data={
                'name': room_name,
                'member_count': len(room_members)
            })
            if serializer.is_valid():
                room = serializer.save()
                res['room'] = {
                    "id": room.id,
                    "name": room.name,
                    "member_count": room.member_count,
                }

            users = []
            for user_id in room_members:
                room_member = add_user(res['room']['id'], user_id)
                users.append(room_member)
            res['users'] = users
            res['token'] = request.auth
            return JsonResponse(res, status=201)
    except Exception as e:
        return JsonResponse(e, status=400)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def post_msg(request):
    user_query = obtain_user(request.data['user_id'])
    room_query = obtain_room(request.data['room_id'])

    serializer = RoomMessageSerializer(data={
        'message': request.data['msg'],
        'room': room_query.id,
        'send_user': user_query.id
    })
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


# 全roomの取得
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtain_all_rooms(request):
    if not Room.objects.all().exists():
        return JsonResponse({"message": 'no room'}, status=400)

    rooms = []
    all_rooms = Room.objects.all()
    for room in all_rooms:
        tmp_room = {
            "room_id": room.id,
            "room_name": room.name
        }
        rooms.append(tmp_room)
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
    # jwtからユーザーIDを取得
    user_id = obtain_id_from_jwt(request)

    # 所属しているroomがなければ空を返す
    if not RoomMember.objects.filter(user_id=user_id):
        return JsonResponse({"rooms": []}, status=201)

    user_rooms = RoomMember.objects.filter(user_id=user_id)

    rooms = []
    for user_room in user_rooms:
        tmp_room = {
            "room_id": user_room.room.id,
            "room_name": user_room.room.name
        }
        rooms.append(tmp_room)
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
    if not Room.objects.filter(pk=room_id):
        return JsonResponse({"message": 'no room'}, status=400)

    all_message_query = RoomMessage.objects.filter(room_id=room_id)
    messages = []
    for message in all_message_query:
        tmp_message = {
            "message": message.message,
            "time": message.created_at,
            "send_user": message.send_user.name
        }
        messages.append(tmp_message)
    res = {
        "room": {
            "room_id": room_id,
            "name": all_message_query[0].room.name,
        },
        "messages": messages,
        "token": request.auth
    }
    return JsonResponse(res, status=200)
