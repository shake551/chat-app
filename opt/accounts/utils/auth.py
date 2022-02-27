from config.settings import SECRET_KEY
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.http import JsonResponse

import time
import jwt
import hashlib
import json

from ..models import User


# 生のパスワードとsaltでハッシュ化する
def hash_password(my_password, salt):
    password = bytes(my_password, 'utf-8')
    if type(salt) != bytes:
        salt = salt.encode('utf-8')
    safe_pass = hashlib.sha256(salt + password).hexdigest()
    return safe_pass

# ユーザーのクエリを入力しtokenを返す
def generate_token(user_query, setting_time):
    time_limit = int(time.time()) + setting_time
    return jwt.encode(
        {"userid": user_query.pk, "name":user_query.name, "exp":time_limit},
        SECRET_KEY
    ).decode('utf-8')


# ログイン認証クラス
"""ログインできた場合 access token を返す"""
class NormalAuthentication(BaseAuthentication):
    def authenticate(self, request):
        res = json.loads(request.body.decode('utf-8'))
        name = res['name']
        password = res['password']
        user_query = User.objects.get(name=name)
        
        if not user_query:
            raise exceptions.AuthenticationFailed('認証失敗')
        
        confirmed_password = hash_password(password, user_query.salt)

        if confirmed_password != user_query.password:
            raise exceptions.AuthenticationFailed('パスワードあってません')
        access_token = generate_token(user_query, 60*60)
        refresh_token = generate_token(user_query, 60*60*24)
        
        token_set = {
            'refresh_token': refresh_token,
            'access_token': access_token,
        }
        return (token_set, None)


# token認証クラス
class JWTAuthentication(BaseAuthentication):
    keyword = 'JWT'
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        
        if len(auth) == 1:
            msg = "Authorization 無効"
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Authorization 無効 スペースなし"
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, SECRET_KEY)
            userid = jwt_info.get('userid')
            try:
                user_query = User.objects.get(pk=userid)
                user_query.is_authenticated = True
                print(user_query)
                access_token = generate_token(user_query, 60 * 60)
                refresh_token = generate_token(user_query, 60 * 60 * 24)

                token_set = {
                    'refresh_token': refresh_token,
                    'access_token': access_token,
                }
                return (user_query, token_set)
            except:
                msg = "no user"
                raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError:
            msg = "token timeout"
            raise exceptions.AuthenticationFailed(msg)
        except:
            msg = "failed"
            raise exceptions.AuthenticationFailed(msg)


# jwtからユーザーIDを取得する
def obtain_id_from_jwt(request):
    auth = get_authorization_header(request).split()
    jwt_token = auth[1]
    jwt_info = jwt.decode(jwt_token, SECRET_KEY)
    user_id = jwt_info.get('userid')
    
    return user_id