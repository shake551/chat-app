from accounts.models.proxy.user_proxy import UserProxy
from chat.models.proxy.room_proxy import RoomProxy
from chat.models.room_message import RoomMessage
from django.db.models import F


class RoomMessageProxy(RoomMessage):
    class Meta:
        proxy = True

    @classmethod
    def post_message(cls, user_id, room_id, message):
        room = RoomProxy.obtain_room(room_id=room_id)
        user = UserProxy.obtain_user(user_id=user_id)

        new_message = cls(
            message=message,
            room=room,
            send_user=user
        )

        new_message.save()

        return new_message

    @classmethod
    def obtain_room_message_list(cls, room_id, start, size):
        return list(
            cls
                .objects
                .filter(room_id=room_id)
                .values('message', time=F('created_at'), user=F('send_user__name'))
                .order_by('time')
                .reverse()
                [start:start+size]
        )
