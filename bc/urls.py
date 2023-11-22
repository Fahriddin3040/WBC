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
    path('note/', views.OperationModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('note/<int:pk>/', views.OperationModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('user/', views.UserAPIView.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:pk>/', views.UserAPIView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('category/', views.CategoryApiView.as_view({'get': 'get', 'post': 'post'})),
    path('category/<int:pk>', views.CategoryApiView.as_view({'get': 'get_detail', 'put': 'update', 'delete': 'delete'})),

]
