import json

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from carousel.models import Carousel
from user.models import User


def get_list(request):
    """获取单页的用户信息"""
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(User.objects.all().order_by('id'))
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
        if isinstance(u, User):
            return {
                'id': u.id,
                'name': u.name,
                'religions_name': u.religions_name,
                'password': u.password,
                'salt': u.salt,
                'email': u.email,
                'status': u.status,
                'last_login_time': u.last_login_time.strftime("%Y-%m-%d %H:%M:%S"),
                'address': u.address,
            }

    data = json.dumps(page_data, default=mydefault)
    print(data)
    return HttpResponse(data)


@csrf_exempt
def edit(request):
    """
    修改、删除 轮播图信息
    :param request:
    :return:
    """
    oper = request.POST.get('oper')
    desc = request.POST.get('desc')
    id = request.POST.get('id')
    status = request.POST.get('status')
    print(status)
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
    """
    添加轮播图信息
    :param request:
    :return:
    """
    title = request.POST.get('title')
    print(request.POST.get('status'))
    status = True if request.POST.get('status') == '1' else False
    print(status)
    pic = request.FILES.get('pic')
    Carousel.objects.create(title=title, status=status, img_url=pic)
    return HttpResponse()


def get_status(request):
    return HttpResponse("<select><option value='1'>显示</option>" + "<option value='0'>不显示</option></select>")
