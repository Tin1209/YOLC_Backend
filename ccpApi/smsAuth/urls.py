from django.urls import path
from . import views
from .views import SmsAuth

app_name = "SMSAuthentication"
urlpatterns = [
	path('auth/', SmsAuth.as_view()),
]
