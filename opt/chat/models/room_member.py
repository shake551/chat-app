from django.db import models

import sys

sys.path.append('../')
from accounts.models.user import User
from chat.models.room import Room


class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
