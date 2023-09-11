from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Feed


def index(request):
    if request.method == "GET":
        feeds = Feed.objects.all()  # read

        context = {
            "feeds": feeds
        }
        return render(request, "feed/index.html", context)
    else:
        return HttpResponse("타당하지않은 값입니다.", status=405)


# Create your views here.
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.user
        # Feed.objects.create(title=title, content=content)
        Feed.objects.create(title=title, content=content,
                            author=author)  # 아직 user기능 열지 않음
        return redirect("/feed/index")
    elif request.method == "GET":
        return render(request, "feed/create.html")
    else:
        return HttpResponse("잘못적음!")


def read(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
    context = {
        "feed": feed
    }
    return render(request, "feed/detail.html", context, )


def delete(request, feed_id):
    if request.method == "POST":
        feed = Feed.objects.get(id=feed_id)
        # if request.user == feed.user:
        feed.delete()
        return redirect("/feed/index/")
        # else:
        #     return HttpResponse("권한없음!")
    else:
        return HttpResponse("잘못적음!")


def update(request, feed_id):
    if request.method == "POST":
        feed = Feed.objects.get(id=feed_id)
        # 사용자 인증 확인 부분 주석 처리
        # if request.user == feed.author:
        feed.title = request.POST.get("title")
        feed.content = request.POST.get("content")
        feed.save()
        return redirect("/feed/read/{}/".format(feed_id))
    elif request.method == "GET":
        feed = Feed.objects.get(id=feed_id)
        context = {
            "feed": feed
        }
        return render(request, "feed/update.html", context)
    else:
        return HttpResponse("잘못적음!")
