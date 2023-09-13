from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from user.models import UserModel
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
        try:
            image = request.FILES['image']
        except:
            image = None
        
        Feed.objects.create(title=title, content=content,
                            author=author, image=image)
        return redirect("/feedlist/")
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


@csrf_exempt
def delete(request, feed_id):

    if request.method == "POST":
        feed = Feed.objects.get(id=feed_id)
        if request.user == feed.author:
            feed.delete()
            return redirect("/feedlist/")
        else:
            return HttpResponse("권한없음!")
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


def create_comment(request, feed_id):
    if request.method == "POST":
        feed_commnet = Feed.objects.get(id=feed_id)
        # ?.content = request.POST.get('content')
        # ?.save()
        return redirect("/feed/read/{}/", feed_id=feed_id)
    else:
        return HttpResponse("잘못된 요청")


def authorsfeed(request, author_id):
    if request.method == "GET":
        author = UserModel.objects.get(id=author_id)
        feeds = Feed.objects.filter(author_id=author_id)
        # feeds = author.feed_set.all()

        page = request.GET.get('page')
        paginator = Paginator(feeds, 6)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_obj = paginator.page(page)

        context = {
            'author':author, 'feeds':feeds, 'page_obj':page_obj, 'paginator':paginator
        }
        return render(request, "feed/authorsfeed.html", context)
    else:
        return HttpResponse("Invalid request method", status=405)