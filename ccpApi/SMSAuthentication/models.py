from django.db import models
import requests
from random import randint
from django.db import models
from django.utils import timezone
import datetime
import time
from . import ApiKeys
import json 

# Create your models here.

class Auth(models.Model):
	phone_number = models.CharField(
			verbose_name="휴대폰 번호",
			primary_key=True,
			max_length=11)
	auth_number = models.IntegerField(verbose_name="인증 번호")	

	class Meta:
		db_table = "smsauth"

	def save(self, *args, **kwargs):
		print("save")
		self.auth_number = randint(1000,10000)
		super().save(*args, **kwargs)
		print("success save")
		self.send_sms()

	def send_sms(self):
		print("send sms")
		url = ApiKeys.api_url
		data = {
			"type": "SMS",
			"from": "01039326620",
			"content": "인증번호는 [{}] 입니다.".format(self.auth_number),
			"messages": [
			{
				"to": self.phone_number,
			}
			],
		}
		timestamp = round(time.time() * 1000)
		timestamp = str(timestamp)
		
		headers = {
			"Content-Type": "application/json; charset=utf-8",
			"x-ncp-apigw-timestamp": timestamp,
			"x-ncp-iam-access-key": ApiKeys.access_key_id,
			"x-ncp-apigw-signature-v2": ApiKeys.make_signature("POST", timestamp),
		}
		print(self.phone_number)
		data = json.dumps(data)

		res = requests.post(url, data=data, headers=headers)
		print(res.headers)
		print(res.json)
		print(res.text)		

	@classmethod
	def check_auth_number(cls, p_num, c_num):
		time_limit = timezone.now() - datetime.timedelta(minutes=3)
		result = cls.objects.filter(
				phone_number=p_num,
				auth_number=c_num,
				modified__gte=time_limit.strftime('%Y-%m-%d')
		)
		if result:
			return True
		return False
	
	

