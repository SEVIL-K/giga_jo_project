from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from feed.models import Feed

# Create your views here.


def feedlist(request):
    if request.method == "GET":

        # sort를 위한 코드
        sort = request.GET.get('sort', '')
        if sort == 'old':
            feeds = Feed.objects.all().order_by('created_at')
        # 좋아요 수, 댓글 수 정렬기능 아래와 같이 추가 가능
        # elif sort == 'likes':
        #     feeds = Feed.objects.all().order_by('-like_count', '-created_at')
        # elif sort == 'comments':
        #     feeds = Feed.objects.all().order_by('-comment_count', '-created_at')
        else:
            feeds = Feed.objects.all().order_by('-created_at')

        # pagination을 위한 코드
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

        leftIndex = (int(page) - 2)
        rightIndex = (int(page) + 2)

        if leftIndex < 1:
            leftIndex = 1

        if rightIndex > paginator.num_pages:
            rightIndex = paginator.num_pages

        custom_range = range(leftIndex, rightIndex+1)

        context = {
            "feeds": feeds,
            "page_obj": page_obj,
            "paginator": paginator,
            "custom_range": custom_range,
            "sort": sort,
        }
        return render(request, 'feedlist/feedlist.html', context)
    else:
        return HttpResponse("Invalid request method", status=405)
