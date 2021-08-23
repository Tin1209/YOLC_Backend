from rest_framework import routers
from main import views
from django.conf.urls import url
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewset)

urlpatterns = [
    path('', include(router.urls)),
]

