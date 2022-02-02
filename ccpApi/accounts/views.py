from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import User 
from django.contrib.auth import authenticate
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from firebase_admin import messaging
from PIL import Image
import os
from .check_face import Want_enter
from .face_registration import face_register
from .client import open_door
import requests
import time

# Create your views here.

@api_view(["POST"])
@csrf_exempt
def login(request):
	if request.method == 'POST':
		id = request.data.get('username', '')
		pw = request.data.get('password', '')
		print("id: " + id + "pw: " + pw)
		login_result = authenticate(username=id, password=pw)

		if login_result:

                        user = User.objects.get(username=id)
                        address = user.address
                        return JsonResponse({'code': '0000', 'msg': 'success login', 'address': address}, status=200)
		else:
			print("로그인 실패")
			return JsonResponse({'code': '1001', 'msg': '로그인 실패', 'address': ''}, status=200)

@api_view(["POST"])
@csrf_exempt
def signup(request):
    id = request.data.get('username', '')
    pw = request.data.get('password', '')
    address = request.data.get('address', '')
    name = request.data.get('name', '')
    phone_num = request.data.get('phone_number', '')

    is_exist = User.objects.filter(username=id).exists()
    if is_exist:
        return JsonResponse({'code': '1002', 'msg': '중복된 ID 입니다'}, status=200)
    else:
        User.objects.create_user(username=id, password=pw, name=name, address=address, phone_number=phone_num)
        return JsonResponse({'code': '0001', 'msg': '회원가입 성공입니다'}, status=201)

@api_view(["PUT"])
@csrf_exempt
def update_profile_image(request, user, image_id, format_=None):
    
    img = request.FILES.get('img')
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        return JsonResponse({'code': '401', 'msg': '존재하지 않는 유저입니다.'}, status=401)
    
    if image_id == 1:
        user.img1 = img
        path = user.img1.path
    elif image_id == 2:
        user.img2 = img
        path = user.img2.path
    elif image_id == 3:
        user.img3 = img
        path = user.img3.path
    elif image_id == 4:
        user.img4 = img
        path = user.img4.path
    elif image_id == 5:
        user.img5 = img
        path = user.img5.path
    elif image_id == 6:
        user.img6 = img
        path = user.img6.path
    if os.path.isfile(path):
        os.remove(path)
    user.save()
    return JsonResponse({'code': '200', 'msg': '업로드 성공 '}, status=200)

def show_image(request, user, image_id):
    user = User.objects.get(username=user)
    if image_id == 1:
        img = user.img1
    elif image_id == 2:
        img = user.img2
    elif image_id == 3:
        img = user.img3
    elif image_id == 4:
        img = user.img4
    elif image_id == 5:
        img = user.img5
    elif image_id == 6:
        img = user.img6

    #tmp = Image.open(img.path)
    #return JsonResponse({'type': img.path}, status=200)
    

    return render(request, 'accounts/profile_image.html',{'img':img})

def show_page(request,user):
    user = User.objects.get(username=user)
    return render(request, 'accounts/profile.html',{'user':user})


@api_view(["POST"])
@csrf_exempt
def save_token(request):
    user = request.data.get('user','')
    token = request.data.get('token','')
    address = request.data.get('address','')

    is_exist = User.objects.filter(username=user).exists()
    target = User.objects.get(username=user)
    target.token = token
    target.save()
    
    return JsonResponse({'code': '201', 'msg': 'token update'}, status=200)


@api_view(["POST"])
@csrf_exempt
def send_notification(request):


    address = request.data.get('useraddress','')
    isExternal = request.data.get('stranger','')
    target = User.objects.get(address=address)
    target_token = target.token

    if isExternal=='1':
        message = messaging.Message(
            data={
                'title': '출입 허가 요청',
                'body': '출입 허가 요청이 도착했습니다!',
                'isExternal': isExternal,
            },
            token=target_token,
        )
    else:
        img_list = []
        count = 0

        while count < 3:
            img = requests.get("http://heean6620.iptime.org:11111/get", timeout=20)
            img_list.append(img.text)
            count += 1
            time.sleep(0.05)

        register = face_register()
        register.save_faces(target.username)
        enter = Want_enter()
        result = enter.check_face(img_list)
        if result:
            open_door(result)
            message = messaging.Message(
                data={
                    'title': 'Door',
                    'body': '문이 열렸습니다.',
                    'isExternal': isExternal,
                },
                token=target_token,
            )
        else:
            message = messaging.Message(
                data={
                    'title': 'Door',
                    'body': '누군가가 침입하려고 합니다!',
                    'isExternal': isExternal,
                },
                token=target_token,
            )

    response = messaging.send(message)

    return response

@api_view(["POST"])
@csrf_exempt
def stranger_open(request):
    isOpen = request.data.get('isOpen','')
    if isOpen:
        open_door(1)
    return JsonResponse({'code': '200', 'msg': '통신 성공!'}, status=200)
