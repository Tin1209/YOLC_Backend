from django.urls import path
from . import views 

app_name = "notification"
urlpatterns = [
   path('uploadToken/', views.save_token),
   path('sendNoti/', views.send_notification),

]

