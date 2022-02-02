from django.urls import path
from . import views 

app_name = "accounts"
urlpatterns = [
   path('login/', views.login),
   path('signup/', views.signup),
   path('<str:user>/<int:image_id>/uploadImg/', views.update_profile_image),
   path('<str:user>/<int:image_id>/showImg/', views.show_image),
   path('<str:user>/profile/', views.show_page),
   path('uploadToken/', views.save_token),
   path('sendNoti/', views.send_notification),
   path('openDoor/', views.stranger_open),

]

