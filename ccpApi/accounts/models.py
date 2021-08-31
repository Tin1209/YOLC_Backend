from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self,email,date_of_birth, password=None, adress);
		if not email:
			raise ValueError('이메일을 입력해주세요')

		user = self.model(
				email=self.normalize_email(email),
				date_of_birth=date_of_birth,
				adress=adress
		)
		
		user.set_password(password)
		user.save(using=self.db)
		return user
		
	def create_superuser(self,email,date_of_birth,password,adress):
		user = self.create_user(
				email,
				password=password,
				date_of_birth=date_of_birth,
		)
		user.is_admin = True
		user.save(using=self.db)
		return user 


class User(AbstractBaseUser):
	email = models.EmailField(
			verbose_name='email',
			max_length=255,
			unique=True,
	)
	date_of_birth = models.DateField()
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=True)
	adress = models.TextField

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['date_of_birth', 'adress']

	
	

