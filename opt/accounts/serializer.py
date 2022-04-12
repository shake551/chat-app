from rest_framework import serializers

from opt.accounts.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'salt', 'urltoken', 'status']
