from django.db import models

import sys

sys.path.append('../')
from accounts.models import User


class Room(models.Model):
    name = models.CharField(max_length=100)
    member_count = models.IntegerField(default=0)


class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class RoomMessage(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    send_user = models.ForeignKey(User, on_delete=models.CASCADE)
