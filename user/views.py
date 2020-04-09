import json, time

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
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
    status = True if request.POST.get('status') == 'True' else False
    email = request.POST.get('email')

    if oper == 'edit':
        with transaction.atomic():
            user = User.objects.get(id=id)
            user.status = status
            user.name = name
            user.religions_name = religions_name
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
    """检查用户名是否重复"""
    user_name = request.GET.get('user_name')
    return JsonResponse({'status': 0}) if user_name in [i[0] for i in list(User.objects.values_list('name'))] \
        else JsonResponse({'status': 1})


# @cache_page(timeout=24 * 60 * 60, key_prefix='get_weeks_data')
def get_weeks_data(request):
    """获取最近一周的注册人数"""
    if cache.has_key('get_weeks_data'):
        data = cache.get('get_weeks_data')
    else:
        print('get_weeks_data')
        t = time.time()
        t1 = t - 24 * 60 * 60 * 1
        day1 = time.strftime('%Y-%m-%d', time.gmtime(t1))
        t2 = t - 24 * 60 * 60 * 2
        day2 = time.strftime('%Y-%m-%d', time.gmtime(t2))
        t3 = t - 24 * 60 * 60 * 3
        day3 = time.strftime('%Y-%m-%d', time.gmtime(t3))
        t4 = t - 24 * 60 * 60 * 4
        day4 = time.strftime('%Y-%m-%d', time.gmtime(t4))
        t5 = t - 24 * 60 * 60 * 5
        day5 = time.strftime('%Y-%m-%d', time.gmtime(t5))
        t6 = t - 24 * 60 * 60 * 6
        day6 = time.strftime('%Y-%m-%d', time.gmtime(t6))
        t7 = t - 24 * 60 * 60 * 7
        day7 = time.strftime('%Y-%m-%d', time.gmtime(t7))
        print(day1, day2, day3, day4, day5, day6, day7)
        u7 = len(User.objects.filter(register_time=day1))
        u6 = len(User.objects.filter(register_time=day2))
        u5 = len(User.objects.filter(register_time=day3))
        u4 = len(User.objects.filter(register_time=day4))
        u3 = len(User.objects.filter(register_time=day5))
        u2 = len(User.objects.filter(register_time=day6))
        u1 = len(User.objects.filter(register_time=day7))
        data = {
            'x': [day7, day6, day5, day4, day3, day2, day1],
            'y': [u1, u2, u3, u4, u5, u6, u7]
        }
        cache.set('get_weeks_data', data, 24 * 60 * 60)
    return JsonResponse({'data': data}, safe=False)


# @cache_page(timeout=12 * 60 * 60, key_prefix='get_distribute')
def get_distribute(request):
    """获取全国用户分布数据"""
    if cache.has_key('get_distribute'):
        data = cache.get('get_distribute')
    else:
        print('get_distribute')
        provinces = ["北京", "天津", "河北", "山西", "内蒙古", "吉林", "黑龙江", "辽宁", "上海", "江苏", "浙江", "安徽",
                     "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏",
                     "陕西", "甘肃", "青海", "宁夏", "新疆", "香港", "澳门", "台湾"
                     ]
        data = []
        for i in provinces:
            data.append({'name': i, 'value': len(User.objects.filter(address=i))})
            cache.set('get_distribute', data, 60 * 60)
    return JsonResponse({'data': data})
