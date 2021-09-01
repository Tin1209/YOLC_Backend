from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import AppAddressesSerializer
from django.contrib.auth import authenticate

# Create your views here.


@api_view(["POST", "GET"])
@csrf_exempt
def login(request):
    if request.method == 'POST':
        id = request.data.get('username', '')
        pw = request.data.get('password', '')
        login_result = authenticate(username=id, password=pw)

        if login_result:
            print("로그인 성공!")
            return JsonResponse({'code': '0000', 'msg': '로그인 성공'}, status=200)
        else:
            print("로그인 실패")
            return JsonResponse({'code': '1001', 'msg': '로그인 실패'}, status=200)

    elif request.method == 'GET':
        query_set = User.objects.all()
        serializer = AppAddressesSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
@csrf_exempt
def signup(request):
    id = request.data.get('username', '')
    pw = request.data.get('password', '')

    is_exist = User.objects.filter(username=id).exists()
    if is_exist:
        print("회원가입 실패: 중복된 ID")
        return JsonResponse({'code': '1002', 'msg': '중복된 ID 입니다'}, status=200)
    else:
        print('회원가입 성공')
        User.objects.create_user(username=id, password=pw)
        return JsonResponse({'code': '0001', 'msg': '회원가입 성공입니다'}, status=201)
