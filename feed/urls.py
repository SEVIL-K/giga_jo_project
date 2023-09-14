from django.shortcuts import render, redirect, HttpResponse
from django.urls import path

from . import views


urlpatterns = [
    path('index/', views.index, name="index"),  # 테스트용 피드페이지 urls
    path('create/', views.create, name='create'),  # 게시글 작성 urls
    path('read/<int:feed_id>/', views.read),
    path('delete/<int:feed_id>/', views.delete, name='delete'),  # 삭제하기 urls
    path('update/<int:feed_id>/', views.update, name='update'),
    path('read/<int:feed_id>/comment/', views.create_comment, name="create_comment"),
]
