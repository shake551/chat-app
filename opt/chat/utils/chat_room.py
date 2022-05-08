from chat.serializer import ChatSerializer


def change_room_name_to_user_name(rooms, user_id):
    if type(rooms) is dict:
        print(rooms)
        if not rooms['member_count'] == 2:
            return

        room_member = ChatSerializer.RoomMemberSerializer.obtain_room_member(room_id=rooms['id'])

        if room_member[0]['user__id'] == user_id:
            rooms['name'] = room_member[1]['user__name']
        else:
            rooms['name'] = room_member[0]['user__name']

        return

    for room in rooms:
        print(room)
        if not room['member_count'] == 2:
            continue

        room_member = ChatSerializer.RoomMemberSerializer.obtain_room_member(room_id=room['room_id'])

        if room_member[0]['user__id'] == user_id:
            room['room_name'] = room_member[1]['user__name']
        else:
            room['room_name'] = room_member[0]['user__name']
