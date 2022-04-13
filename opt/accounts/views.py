from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

import sys

sys.path.append('../')
from accounts.models.user import User
from .serializer import UserSerializer
from .utils.auth import NormalAuthentication, obtain_id_from_jwt, check_uuid_format
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
def obtain_all_users(request):
    my_user_id = obtain_id_from_jwt(request)
    users = list(User.objects.values('id', 'name').exclude(id=my_user_id))

    response = {
        "users": users,
        'token': request.auth
    }

    return JsonResponse(response, status=200)
