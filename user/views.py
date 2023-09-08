from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserModel

# Create your views here.
def test(request):
    return render(request, template_name='base.html')

def MyPage(request, id):
    me = UserModel.objects.get(id=id)
    return render(request, template_name='user/myPage.html', context={'profile': me})

def update_profile(request, id):
    me = UserModel.objects.get(id=id)
    
    