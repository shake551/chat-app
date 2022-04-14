from django.forms import model_to_dict
from rest_framework import serializers
from django.db import transaction

from accounts.models.proxy.user_proxy import UserProxy
from chat.models.proxy.room_member_proxy import RoomMemberProxy
from chat.models.proxy.room_message_proxy import RoomMessageProxy
from chat.models.proxy.room_proxy import RoomProxy
from chat.models.room import Room
from chat.models.room_member import RoomMember
from chat.models.room_message import RoomMessage


class ChatSerializer(serializers.ModelSerializer):
    class RoomSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = ['id', 'name', 'member_count']

        @classmethod
        def obtain_room(cls, room_id):
            if not RoomProxy.exists_room_by_room_id(room_id=room_id):
                raise serializers.ValidationError('room is not found')

            return model_to_dict(RoomProxy.obtain_room(room_id=room_id))

        @classmethod
        def obtain_all_room_list(cls):
            return RoomProxy.obtain_all_room_list()

    class RoomMemberSerializer(serializers.ModelSerializer):
        class Meta:
            model = RoomMember
            fields = ['room', 'user']

        @classmethod
        def obtain_user_room(cls, user_id):
            if not UserProxy.exists_user_by_user_id(user_id=user_id):
                raise serializers.ValidationError('user is not found')

            return RoomMemberProxy.obtain_user_room(user_id=user_id)

    class RoomMessageSerializer(serializers.ModelSerializer):
        class Meta:
            model = RoomMessage
            fields = ['id', 'message', 'room', 'send_user']

        @classmethod
        def post_message(cls, message, room_id, user_id):
            if not (RoomProxy.exists_room_by_room_id(room_id=room_id)
                    and UserProxy.exists_user_by_user_id(user_id)):
                raise serializers.ValidationError('invalid parameter')

            return RoomMessageProxy.post_message(user_id=user_id, room_id=room_id, message=message)

        @classmethod
        def obtain_room_message(cls, room_id):
            if not RoomProxy.exists_room_by_room_id(room_id=room_id):
                raise serializers.ValidationError('room is not found')

            return RoomMessageProxy.obtain_room_message_list(room_id=room_id)

    @classmethod
    @transaction.atomic
    def create_room(cls, room_name, user_id_list):
        new_room = RoomProxy.create(room_name=room_name, member_count=len(user_id_list))

        for user_id in user_id_list:
            if not UserProxy.exists_user_by_user_id(user_id=user_id):
                raise serializers.ValidationError('user not found')

            RoomMemberProxy.add_room_member(room_id=new_room.id, user_id=user_id)

        return model_to_dict(new_room)
