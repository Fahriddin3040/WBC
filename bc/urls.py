from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from rest_framework import viewsets
from rest_framework.response import Response

from . import views
from . import models

METHODS_VOC = {
    'get': 'list',    # Список объектов
    'get_detail': 'retrieve',  # Получение деталей объекта
    'put': 'update',  # Обновление объекта
    'delete': 'destroy',  # Удаление объекта
    'post': 'create',  # Создание нового объекта
}



operation = views.OperationModelViewSet()
user = views.UserAPIView

urlpatterns = [
    path('profile/', views.OperationModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('profile/<int:pk>/', views.OperationModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
