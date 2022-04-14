import sys

sys.path.append('../')
from accounts.models.proxy.user_proxy import UserProxy
from chat.models.room_member import RoomMember
from chat.models.proxy.room_proxy import RoomProxy


class RoomMemberProxy(RoomMember):
    class Meta:
        proxy = True

    @classmethod
    def add_room_member(cls, room_id, user_id, bulk_flag=False):
        room_member = cls(
            room_id=room_id,
            user_id=user_id
        )

        if not bulk_flag:
            room_member.save()

        return room_member

    @classmethod
    def bulk_add_room_member(cls, room_id, user_id_list):
        if not RoomProxy.exists_room_by_room_id(room_id=room_id):
            raise Exception('room not found')

        room_member_list = []

        for user_id in user_id_list:
            if not UserProxy.exists_user_by_user_id(user_id=user_id):
                raise Exception('user not found')

            room_member_list.append(
                cls.add_room_member(room_id=room_id, user_id=user_id)
            )

        cls.objects.bulk_create(room_member_list)

        return room_member_list

    @classmethod
    def obtain_user_room(cls, user_id):
        return list(
            cls
                .objects
                .filter(user_id=user_id)
                .values('room__id', 'room__name')
        )
