import json

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from carousel.models import Carousel


def get_list(request):
    """获取全部的轮播图信息"""
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(Carousel.objects.all().order_by('id'))
    paginator = Paginator(st_list, int(rows))
    try:
        rows = list(paginator.page(page).object_list)
    except Exception as tips:
        print(tips)
        rows = list(paginator.page(int(page) - 1).object_list)
        page = int(page) - 1

    page_data = {
        'page': page,
        'total': paginator.num_pages,
        'records': paginator.count,
        'rows': rows
    }

    def mydefault(u):
        if isinstance(u, Carousel):
            print(u.status, u.img_url)
            return {
                'id': u.id,
                'desc': u.title,
                'date': u.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                'status': u.status,
                'img_url': u.img_url,
            }

    data = json.dumps(page_data, default=mydefault)
    print(data)
    return HttpResponse(data)


@csrf_exempt
def edit(request):
    oper = request.POST.get('oper')
    desc = request.POST.get('desc')
    id = request.POST.get('id')
    status = request.POST.get('status')
    if oper == 'edit':
        with transaction.atomic():
            car = Carousel.objects.get(id=id)
            car.status = True if status == '1' else False
            car.title = desc
            car.save()
    elif oper == 'del':
        with transaction.atomic():
            Carousel.objects.get(id=id).delete()
    return HttpResponse()


@csrf_exempt
def add(request):
    title = request.POST.get('title')
    status = True if request.POST.get('status') else False
    pic = request.FILES.get('pic')
    Carousel.objects.create(title=title, status=status, img_url=pic)
    return HttpResponse()


def get_status(request):
    return HttpResponse("<select><option value='1'>显示</option>" + "<option value='0'>不显示</option></select>")
