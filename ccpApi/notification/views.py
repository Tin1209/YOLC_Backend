from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import noti_token
import os

from firebase_admin import messaging

# Create your views here.

@api_view(["POST"])
@csrf_exempt
def save_token(request):
    user = request.data.get('user','')
    token = request.data.get('token','')
    address = request.data.get('address','')

    is_exist = noti_token.objects.filter(name=user).exists()

    if is_exist:
        target = noti_token.objects.get(name=user)
        target.token = token
        target.save()
        return JsonResponse({'code': '201', 'msg': 'token update'}, status=200)
    else:
        target = noti_token(name=user,token=token,address=address)
        target.save()
        return JsonResponse({'code': '200', 'msg': 'create token'}, status=200)


@api_view(["POST"])
@csrf_exempt
def send_notification(request):
   

    address = request.data.get('useraddress','')
    isExternal = request.data.get('stranger','')
    target = noti_token.objects.get(address=address)
    target_token = target.token

    if isExternal=='1':
        message = messaging.Message(
            data={
                'title': '출입 허가 요청',
                'body': '누군가가 침입했습니다!',
                'isExternal': isExternal,
            },
            token=target_token,
        )
    else:
        message = messaging.Message(
            data={
                'title': 'Door',
                'body': '문이 열렸습니다.',
                'isExternal': isExternal,
            },
            token=target_token,
        )

    response = messaging.send(message)

    return response
