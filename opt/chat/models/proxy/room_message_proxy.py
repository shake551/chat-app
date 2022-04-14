from chat.models.room_message import RoomMessage
from django.db.models import F


class RoomMessageProxy(RoomMessage):
    class Meta:
        proxy = True

    @classmethod
    def post_message(cls, user_id, room_id, message):
        new_message = cls(
            message=message,
            room=room_id,
            send_user=user_id
        )

        new_message.save()

        return new_message

    @classmethod
    def obtain_room_message_list(cls, room_id):
        return list(
            cls
                .objects
                .filter(room_id=room_id)
                .values('message', time=F('created_at'), user=F('send_user__name'))
        )
