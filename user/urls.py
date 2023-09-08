from django.urls import path, include
from . import views

urlpatterns = [
    path('mypage/<int:id>', views.MyPage, name='myPage'),
    path('mypage/update/<int:id>', views.update_profile, name='update-profile')
]