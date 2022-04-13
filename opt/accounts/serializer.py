from django.core.mail import send_mail
from rest_framework import serializers
import sys

sys.path.append('../')
from accounts.models.user import User
from accounts.models.proxy.user_proxy import UserProxy
from accounts.utils.auth import check_uuid_format, obtain_id_from_jwt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'salt', 'urltoken', 'status']

    def pre_signup(self, name, email, password):
        user = UserProxy.pre_signup(name=name, email=email, password=password)

        verify_url = 'http://localhost:3000/verify/' + str(user.urltoken)
        send_mail(
            '本登録のお願い',
            '以下のリンクにアクセスして本登録を完了してください\n' + verify_url,
            'admin@example.com',
            [user.email],
            fail_silently=False,
        )

        return user

    def verify(self, token):
        if not check_uuid_format(token):
            raise serializers.ValidationError('token is not valid')

        if not UserProxy.exists_user_by_token(token=token):
            raise serializers.ValidationError('user not found')

        return UserProxy.verify(token=token)

    def obtain_user_list_exclude_login_user(self, jwt_token):
        login_user_id = obtain_id_from_jwt(jwt_token=jwt_token)

        return UserProxy.obtain_user_list_exclude_login_user(login_user_id=login_user_id)
