from rest_framework import serializers
import sys

sys.path.append('../')
from accounts.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'salt', 'urltoken', 'status']
