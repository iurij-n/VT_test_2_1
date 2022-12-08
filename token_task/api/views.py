import re

import requests
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
URL = 'https://www.google.com/'


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_id_type(id):
    is_email = re.search(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',
        id)
    if is_email:
        return is_email.group(0), 'email'
    is_phone = re.match(
        r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}',
        id)
    if is_phone:
        return is_phone.group(0), 'phone'
    return None


@api_view(['POST'])
def signin_view(request):
    try:
        user = get_object_or_404(User,
                                 username=request.data.get('id'),
                                 password=request.data.get('password'))

        token = get_tokens_for_user(user)

        return JsonResponse(token)
    except Exception:
        return JsonResponse(
            {'error': 'Пользователь с такими данными не найден.'})


@api_view(['POST'])
def signup_view(request):

    users = User.objects.all()

    for user in users:
        if request.data.get('id') == user.username:
            return JsonResponse(
                {'error':
                    'Пользователь с таким email или '
                    'номером телефона уже зарегистрирован.'})

    if get_id_type(request.data.get('id')):
        username, id_type = get_id_type(request.data.get('id'))
        request.data['username'] = username
        request.data.pop('id')
        if id_type == 'phone':
            request.data['phone_number'] = username
        elif id_type == 'email':
            request.data['email'] = username
        else:
            raise ValueError

        request.data['id_type'] = id_type

        user = User.objects.create(**request.data)

        token = get_tokens_for_user(user)

        return JsonResponse(token)

    return JsonResponse({'error': 'Неверное имя пользователя.'})


@api_view(['GET'])
def info_view(request):
    RefreshToken.for_user(request.user)
    return JsonResponse(
        {'id': request.user.username, 'id_type': request.user.id_type})


@api_view(['GET'])
def latency_view(request):
    if request.user.is_authenticated:
        response = requests.get(URL)
        RefreshToken.for_user(request.user)
        return JsonResponse({'latency': response.elapsed.total_seconds()})
    return JsonResponse({'error': 'Пользователь на авторизован.'})


@api_view(['GET'])
def logout_view(request):
    if request.user.is_authenticated:
        token = RefreshToken.for_user(request.user)
        token.blacklist()
        return Response(
            {'message': 'Токен обновления добавлен в черный список.'})
    return JsonResponse({'error': 'Пользователь на авторизован.'})
