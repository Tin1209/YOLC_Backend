from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
import sys
import os
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,username, name, address, phone_number, password=None):
        if not username:
            raise ValueError('must have user name')

        user = self.model(
            username=username,
            name=name,
            address=address,
            phone_number=phone_number
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, name, address, phone_number, password):
        user = self.create_user(
            username=username,
            name=name,
            address=address,
            phone_number=phone_number,
            password=password
            )
        user.is_admin = True
        user.save(using=self._db)
        return user 

class User(AbstractBaseUser):
    username = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200,unique=True)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    token = models.CharField(max_length=200,blank=True)

    def upload_dir1(instance, filename):
        prefix = instance.username
        return "face/" + prefix + "/image1.jpg"
    def upload_dir2(instance, filename):
        prefix = instance.username
        return "face/" + prefix + "/image2.jpg"
    def upload_dir3(instance, filename):
        prefix = instance.username
        return "face/" + prefix + "/image3.jpg"
    def upload_dir4(instance, filename):
        prefix = instance.username
        return "face/" + prefix + "/image4.jpg"
    def upload_dir5(instance, filename):
        prefix = instance.username
        return "face/" + prefix + "/image5.jpg"
    def upload_dir6(instance, filename):
        prefix = instance.username
        return "face/" + prefix + "/image6.jpg"


    
    img1 = models.FileField(upload_to=upload_dir1,blank=True,null=True)
    img2 = models.FileField(upload_to=upload_dir2,blank=True,null=True)
    img3 = models.FileField(upload_to=upload_dir3,blank=True,null=True)
    img4 = models.FileField(upload_to=upload_dir4,blank=True,null=True)
    img5 = models.FileField(upload_to=upload_dir5,blank=True,null=True)
    img6 = models.FileField(upload_to=upload_dir6,blank=True,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['name', 'address', 'phone_number']


def has_perm(self, perm, obj=None):
    return True

def has_module_perms(self, app_label):
    return True

@property 
def is_staff(self):
    return self.is_admin
