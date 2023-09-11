from django.shortcuts import render, redirect, HttpResponse
from django.urls import path

from . import views


urlpatterns = [
    path('index/', views.index, name="index"),  # 게시글 보여주는 url
    path('create/', views.create, name='create'),  # 게시글 작성 urls
    # path('update/', views.update, name='update'),
]
