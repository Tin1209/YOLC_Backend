from django.contrib.auth.models import User
from rest_framework import serializers

class AppAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
