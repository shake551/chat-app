from django.db import models

import sys

sys.path.append('../')
from accounts.models.user import User
from chat.models.room import Room


class RoomMessage(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    send_user = models.ForeignKey(User, on_delete=models.CASCADE)
