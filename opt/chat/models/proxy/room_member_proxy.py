import sys

from django.db.models import F

sys.path.append('../')
from chat.models.room_member import RoomMember


class RoomMemberProxy(RoomMember):
    class Meta:
        proxy = True

    @classmethod
    def add_room_member(cls, room_id, user_id):
        room_member = cls(
            room_id=room_id,
            user_id=user_id
        )

        room_member.save()

        return room_member

    @classmethod
    def obtain_user_room(cls, user_id):
        return list(
            cls
                .objects
                .filter(user_id=user_id)
                .values('room_id', member_count=F('room__member_count'), room_name=F('room__name'))
        )

    @classmethod
    def obtain_room_member(cls, room_id):
        return cls\
            .objects\
            .filter(room_id=room_id)\
            .values('user__name', 'user__id')
