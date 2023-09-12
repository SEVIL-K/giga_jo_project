from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('mypage/<int:id>', views.MyPage, name='myPage'),
    path('mypage/update/<int:id>', views.update_profile, name='update-profile'),
    path('myfeed/<int:id>', views.Myfeed, name='my-feed'),
]
