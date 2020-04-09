import json

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from carousel.models import Carousel
from user.models import User
from utils import random_code


def get_list(request):
    """获取单页的用户信息"""
    print('dads')
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
    print('sssss')
    print(data)
    return HttpResponse(data)


@csrf_exempt
def edit(request):
    """
    修改、删除 用户信息
    :param request:
    :return:
    """
    oper = request.POST.get('oper')
    name = request.POST.get('name')
    id = request.POST.get('id')
    religions_name = request.POST.get('religions_name')
    password = request.POST.get('password')
    address = request.POST.get('address')
    status = True if request.POST.get('status')=='True' else False
    email = request.POST.get('email')

    if oper == 'edit':
        with transaction.atomic():
            user= User.objects.get(id=id)
            user.status = status
            user.name=name
            user.religions_name= religions_name
            user.password = password
            user.address = address
            user.email = email
            user.save()
    elif oper == 'del':
        with transaction.atomic():
            User.objects.get(id=id).delete()
    return HttpResponse()


@csrf_exempt
def add(request):
    """
    添加用户信息
    :param request:
    :return:
    """

    user_name = request.POST.get('user_name')
    if user_name in [i[0] for i in list(User.objects.values_list('name'))]:
        return JsonResponse({'status': 0})
    religions_name = request.POST.get('religions_name')
    password = request.POST.get('password')
    email = request.POST.get('email')
    address = request.POST.get('address')
    status = True
    with transaction.atomic():
        User.objects.create(name=user_name, religions_name=religions_name, password=password,
                            salt=random_code.get_random_code(), status=status, address=address, email=email)

    return JsonResponse({'status': 1})


def check_username(request):
    user_name = request.GET.get('user_name')
    return JsonResponse({'status': 0}) if user_name in [i[0] for i in list(User.objects.values_list('name'))] else JsonResponse({'status': 1})
