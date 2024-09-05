from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'articles'


router = routers.DefaultRouter()

router.register(r'articles', views.ArticleViewSet, basename='article')


urlpatterns = [
    path('', include(router.urls))
]