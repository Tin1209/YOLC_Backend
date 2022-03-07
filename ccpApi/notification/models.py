from django.db import models

# Create your models here.

class noti_token(models.Model):
    name = models.CharField(max_length=100,unique=True)
    token = models.CharField(max_length=200)
    address = models.CharField(max_length=100,unique=True,blank=True)

    class Meta:
        db_table = "notificationtoken"
