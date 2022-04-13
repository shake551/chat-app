import os
import uuid
import base64
import datetime as dt

from rest_framework.exceptions import ValidationError

from .user import User
from ..utils.auth import hash_password


class UserProxy(User):
    class Meta:
        proxy = True

    @classmethod
    def exists_user_by_token(cls, token):
        return cls.objects.filter(urltoken=token).exists()

    @classmethod
    def obtain_user_by_token(cls, token):
        return cls.objects.get(urltoken=token)

    @classmethod
    def pre_signup(cls, name, email, password):
        salt = base64.b64encode(os.urandom(32))

        pre_signup_user = cls(
            name=name,
            email=email,
            password=hash_password(password, salt),
            urltoken=uuid.uuid4(),
            salt=salt.decode('utf-8')
        )

        pre_signup_user.save()

        return pre_signup_user

    @classmethod
    def verify(cls, token):
        user = cls.objects.get(urltoken=token)

        effective_date = user.created_at + dt.timedelta(days=1)

        if dt.datetime.now() > effective_date:
            raise ValidationError('token is not valid')

        user.status = 1
        user.save()

        return user

    @classmethod
    def obtain_user_list_exclude_login_user(cls, login_user_id):
        return list(cls.objects.values('id', 'name').exclude(id=login_user_id))
