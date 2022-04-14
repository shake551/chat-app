from chat.models.room import Room


class RoomProxy(Room):
    class Meta:
        proxy = True

    @classmethod
    def exists_room_by_room_id(cls, room_id):
        return cls.objects.filter(pk=room_id).exists()

    @classmethod
    def obtain_room(cls, room_id):
        if cls.objects.filter(pk=room_id).exists():
            room_query = cls.objects.values('id', 'name').get(pk=room_id)
            return room_query
        raise Exception('room not found')

    @classmethod
    def obtain_all_room_list(cls):
        return list(cls.objects.values('id', 'name').all())

    @classmethod
    def create(cls, room_name, member_count):
        room = cls(
            name=room_name,
            member_count=member_count
        )

        room.save()

        return room
