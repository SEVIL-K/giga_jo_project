from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Feed


# Create your views here.
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        # user = request.user
        Feed.objects.create(title=title, content=content)
        # Feed.objects.create(title=title,content=content,user=user) # 아직 user기능 열지 않음
        return HttpResponse("작성완료!")
    elif request.method == "GET":
        return render(request, "feed/create.html")
    else:
        return HttpResponse("잘못적음!")
