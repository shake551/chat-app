from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

import sys

sys.path.append('../')
from .serializer import UserSerializer
from .utils.auth import NormalAuthentication
from .utils.auth import JWTAuthentication


@api_view(['POST'])
@csrf_exempt
def pre_signup(request):
    user_serializer = UserSerializer()
    user = user_serializer.pre_signup(
        name=request.data['name'],
        email=request.data['email'],
        password=request.data['password']
    )

    return JsonResponse({'user': model_to_dict(user)}, status=201)


# 本登録URLにアクセスがあったときに本登録を完了する
@api_view(['GET'])
def verify_user(request):
    if 'token' not in request.GET:
        return JsonResponse({"message": "cannot receive token"}, status=400)

    got_token = request.GET.get('token')

    user_serializer = UserSerializer()
    user_serializer.verify(got_token)

    return JsonResponse({"message": "ok"}, status=201)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([NormalAuthentication])
def loginApi(request):
    return JsonResponse({"token": request.user}, status=201)


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


# 自分以外のユーザーのid,nameを取得する
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtain_user_list_exclude_login_user(request):
    jwt_token = get_authorization_header(request).split()[1]
    user_serializer = UserSerializer()

    response = {
        "users": user_serializer.obtain_user_list_exclude_login_user(jwt_token=jwt_token),
        'token': request.auth
    }

    return JsonResponse(response, status=200)
