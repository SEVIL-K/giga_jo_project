from django.shortcuts import render, redirect, HttpResponse
from django.urls import path

from . import views


urlpatterns = [
    # path('index/', views.index, name="index"), # 예시
    path('create/', views.create, name='create'),  # 게시글 작성 urls
]
