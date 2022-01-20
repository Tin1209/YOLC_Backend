from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import User 
from django.contrib.auth import authenticate
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

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
			print("로그인 성공!")
			return JsonResponse({'code': '0000', 'msg': '로그인 성공'}, status=200)
		else:
			print("로그인 실패")
			return JsonResponse({'code': '1001', 'msg': '로그인 실패'}, status=200)

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
    elif image_id == 2:
        user.img2 = img
    elif image_id == 3:
        user.img3 = img
    elif image_id == 4:
        user.img4 = img
    elif image_id == 5:
        user.img5 = img
    elif image_id == 6:
        user.img6 = img
    user.save()
    return JsonResponse({'code': '200', 'msg': '업로드 성공 '}, status=200)

@api_view(["GET"])
@csrf_exempt
def show_image(request, user, image_id):

    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        return JsonResponse({'code': '401', 'msg': '존재하지 않는 유저입니다.', 'image': ''}, status=401)

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

    file_path = img.path
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path,'rb'),content_type='image/jpeg')
    
    return response

