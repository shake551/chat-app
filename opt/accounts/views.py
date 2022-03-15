from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

import uuid
import os
import base64
import re
import datetime as dt

from .models import User
from .serializer import UserSerializer
from .utils.auth import NormalAuthentication
from .utils.auth import JWTAuthentication
from .utils.auth import hash_password


# 引数がuuid形式であればTrue, それ以外はFalseを返す
def check_uuid_format(confirmed_text):
    match_text = re.search(
        r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
        confirmed_text
    )
    print(match_text)
    if not match_text:
        print('not match')
        return False
    if match_text.group(0) == confirmed_text:
        return True
    print('not exist')
    return False


@api_view(['POST'])
@csrf_exempt
def pre_signup(request):
    salt = base64.b64encode(os.urandom(32))
    
    insert_data = {
        'name': request.data['name'], 
        'email': request.data['email'],
        # salt と password を結合してハッシュ化
        'password': hash_password(request.data['password'], salt),
        'urltoken': uuid.uuid4(),
        'salt': salt.decode('utf-8'),
    }
    
    serializer = UserSerializer(data=insert_data)

    if serializer.is_valid():
        new_data = serializer.save()
        verify_url = 'http://localhost:3000/verify/' + str(new_data.urltoken)
        send_mail(
            '本登録のお願い',
            '以下のリンクにアクセスして本登録を完了してください\n' + verify_url,
            'admin@example.com',
            [new_data.email],
            fail_silently=False,
        )
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


# 本登録URLにアクセスがあったときに本登録を完了する
@api_view(['GET'])
def verify_user(request):
    if not 'token' in request.GET:
        return JsonResponse({"message":"cannot receive token"}, status=400)
    
    got_token = request.GET.get('token')
    
    # uuidのformatが不正であればエラーを返す
    if not check_uuid_format(got_token):
        return JsonResponse({"message":"token is not valid"}, status=400)
    
    if User.objects.filter(urltoken=got_token).exists():
        user_query = User.objects.get(urltoken=got_token)

        # (現在時間) > (タイムスタンプ + 1日)ならばtokenは無効
        effective_date = user_query.created_at + dt.timedelta(days=1)
        if dt.datetime.now() > effective_date:
            return JsonResponse({"message":"token is not valid"}, status=200)
        
        # ユーザー本登録の完了
        user_query.status = 1
        user_query.save()
        return JsonResponse({"message":"ok"}, status=201)
    return JsonResponse({"message":"token is not valid"}, status=400)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([NormalAuthentication])
def loginApi(request):
    return JsonResponse({"token":request.user}, status=201)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def token(request):
    response = {
        "user": {
            "id": request.user.id,
            "name": request.user.name,
        },
        'token': request.auth
    }
    return JsonResponse(response, status=200)
