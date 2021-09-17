from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class SmsAuth(APIView):
	def post(self,request):
		try:
			print("loading")
			print(request)
			p_num = request.data.get('phone_number', '')
			print(p_num)
		except KeyError:
			return Response({'message': 'Bad Request'},
					status=status.HTTP_400_BAD_REQUEST)
		else:
			models.Auth.objects.update_or_create(phone_number=p_num)
			return Response({'message': 'OK'})

	def get(self, request):
		try:
			p_num = request.data.get('phone_number', '')
			a_num = request.data.get('auth_number', '')
		except KeyError:
			return Response({'message': 'Bad request'},
					status=status.HTTP_400_BAD_REQUEST)
		else:
			result = models.Auth.check_auth_number(p_num, a_num)
			return Response({'message': 'OK', 'result': result})
