from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

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
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['name', 'address', 'phone_number']

    def __str__(self):
        return self.username

def has_perm(self, perm, obj=None):
    return True

def has_module_perms(self, app_label):
    return True

@property 
def is_staff(self):
    return self.is_admin


