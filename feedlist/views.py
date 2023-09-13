from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from feed.models import Feed

# Create your views here.


def feedlist(request):
    if request.method == "GET":
        feeds = Feed.objects.all().order_by('-created_at')
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
            "custom_range": custom_range
        }
        return render(request, 'feedlist/feedlist.html', context)
    else:
        return HttpResponse("Invalid request method", status=405)
