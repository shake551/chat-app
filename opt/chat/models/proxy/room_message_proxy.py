from chat.models.room_message import RoomMessage


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
                .values('message', 'created_at', 'send_user__name')
        )
