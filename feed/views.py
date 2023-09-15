from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Feed, FeedComment
from user.models import UserModel



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
    comments = FeedComment.objects.filter(feed=feed)
    context = {
        "feed": feed,
        "comments": comments
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
        if request.user == feed.author:
            feed.title = request.POST.get("title")
            feed.content = request.POST.get("content")
            if request.FILES.get("image"):
                    new_image = request.FILES["image"]
                    feed.image = new_image  # 이미지 필드를 업데이트
            feed.save()  # 새 이미지를 저장
            return redirect("/feed/read/{}/".format(feed_id))
    elif request.method == "GET":
        feed = Feed.objects.get(id=feed_id)
        context = {
            "feed": feed
        }
        return render(request, "feed/update.html", context)
    else:
        return HttpResponse("잘못적음!")


# 댓글기능 구현중
@login_required
def create_comment(request, feed_id):
    if request.method == "POST":
        content = request.POST.get("content")
        author = request.user
        feed = Feed.objects.get(id=feed_id)
        comment = FeedComment.objects.create(content=content, author=author, feed=feed)
        # comment = FeedComment(content=content, author=author)
        # comment.save()
        # 댓글 생성 후 리디렉션 또는 다른 작업 수행
        return redirect("/feed/read/{feed_id}/".format(feed_id=feed_id))  # 피드 상세 페이지로 리디렉션
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


# 댓글 수정 기능

def update_comment(request, comment_id):
    if request.method == "POST":
        comment = FeedComment.objects.get(pk=comment_id)
        # 사용자 인증 확인 부분 주석 처리
        if request.user == comment.author:
            comment.content = request.POST.get("content")
            comment.save()
            return redirect("/feed/read/{}/".format(comment.feed.id))
    elif request.method == "GET":
        comment = FeedComment.objects.get(pk=comment_id)
        context = {
            "comment": comment
        }
        return render(request, "feed/update_comment.html", context)
    else:
        return HttpResponse("잘못적음!")
# 댓글 삭제 기능
@csrf_exempt
def delete_comment(request, comment_id):

    # if request.method == "POST":
        comment = FeedComment.objects.get(pk=comment_id)
        if request.user == comment.author:
            comment.delete()
            return redirect("/feed/read/{}/".format(comment.feed.id))
        else:
            return HttpResponse("권한없음!")
    # else:
    #     return HttpResponse("잘못적음!")

def feed_like(request, id):
    re_address = reverse('read', args=(id,))
    current_feed = Feed.objects.get(id=id)
    user = request.user
    if current_feed.like < 0:
        current_feed.like = 0
        current_feed.save()

    if current_feed not in user.liked_feed.all():
        user.liked_feed.add(current_feed)
        current_feed.like += 1
        current_feed.save()
    else:
        user.liked_feed.remove(current_feed)
        current_feed.like -= 1
        current_feed.save()
    print(current_feed.like)

    return redirect(re_address)
