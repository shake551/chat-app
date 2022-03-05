from rest_framework import serializers

from .models import Room, RoomMember, RoomMessage


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'member_count']


class RoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMember
        fields = ['room', 'user']


class RoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessage
        fields = ['id', 'message', 'room', 'send_user']
