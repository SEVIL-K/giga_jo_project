from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedlist),
    path('feedlist/', views.feedlist, name='feedlist'),
]
