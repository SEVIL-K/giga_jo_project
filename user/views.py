from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserModel
from feed.models import Feed
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from PIL import Image

# Create your views here.



def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/feedlist/')
    else:
        return redirect('/login')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        nickname = request.POST['nickname']
        email = request.POST['email']
        password = request.POST['password']
        image = request.FILES.get('image')
        if not image:
            image = 'default.png'
        UserModel.objects.create_user(
            username=username, nickname=nickname, email=email, password=password, image=image)
        return redirect('/login/')
    elif request.method == 'GET':
        return render(request, 'user/signup.html')
    else:
        return HttpResponse('Invalid request method', status=405)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/feedlist/')
        else:
            return redirect('/login/')
    elif request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        return redirect('/login/')

@login_required(login_url='/login/')
def logout(request):
    user = request.user
    if user.is_authenticated:
        auth_logout(request)
        return redirect('/login/')
    else:
        return HttpResponse('Invalid request method', status=405)


def test(request):  # 테스트용 메소드
    return render(request, template_name='user/myFeed.html')


def MyPage(request, id):
    me = UserModel.objects.get(id=id)

    return render(request, template_name='user/myPage.html', context={'profile': me})


def Myfeed(request, id):
    my_feeds = Feed.objects.filter(author_id=id)  # 불러올 나의 피드
    page = request.GET.get('page')

    paginator = Paginator(my_feeds, 6)

    try:
        page_obj = paginator.page(page)  # 현재 페이지
    except PageNotAnInteger:  # 페이지가 1개인 경우
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # 페이지 범위를 초과하는 url을 입력했을 경우
        page_obj = paginator.page(page)

    return render(request, template_name='user/myFeed.html', context={'my_feeds': my_feeds, 'page_obj': page_obj, 'paginator': paginator})

# @login_required


def update_profile(request, id):
    me = UserModel.objects.get(id=id)
    if request.method == 'GET':
        return render(request, template_name='user/myPage.html', context={'profile': me})
    elif request.method == 'POST':
        re_add = reverse(viewname='update-profile', args=(id,))

        username = request.POST.get('username')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        image = request.FILES.get('image')
        if not image:
            image = 'default.png'
        if password1 != password2:
            return render(request, template_name='user/myPage.html', context={'error': '비밀번호가 다릅니다!'})
        else:
            # print(f"{username}, {nickname}, {email}, {password1}")
            me.username = username
            me.nickname = nickname
            me.email = email
            me.set_password(password1)
            me.image = image
            me.save()
            auth_login(request, me)
            return redirect(re_add)


@login_required(login_url='/login/')
def user_view(request):
    user_list = UserModel.objects.all().exclude(username=request.user.username)
    return render(request, 'user/follow.html', {'user_list': user_list})


@login_required(login_url='/login/')
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(me)
    else:
        click_user.followee.add(me)
    return redirect('/user')