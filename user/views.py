import re

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from redis import Redis
from index.models import Admin
from utils import send_msg
from utils.random_code import get_random_code

# Create your views here.
from zjf_cmfz import settings


def login(request):
    return render(request, 'user/login.html')


@csrf_exempt
def check_user(request):
    red = Redis(host='127.0.0.1', port=6379)
    mobile = request.POST.get('mobile')

    if re.match(r'^[1][3,4,5,7,8][0-9]{9}$', mobile) and Admin.objects.filter(name=mobile):
        if red.get(mobile + '_2'):
            return JsonResponse({'status': 0})
        else:
            code = get_random_code()  # 生成随机验证码
            code = '123456'
            red.set(mobile + '_1', code, 60)  # 60秒的有效期
            red.set(mobile + '_2', mobile, 60)  # 60秒内只能发送一次
            yunpian = send_msg.YunPian(settings.API_KEY)
            # yunpian.send_msg(mobile, code)
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def login_form(request):
    """
    验证是否登录成功
    :param request:
    :return:
    """
    red = Redis(host='127.0.0.1', port=6379)
    mobile = request.GET.get('mobile')
    code = request.GET.get('code')
    if re.match(r'^[1][3,4,5,7,8][0-9]{9}$', mobile) and Admin.objects.filter(name=mobile):
        redis_code = red.get(mobile + '_1').decode()
        if redis_code == code:
            return JsonResponse({'status': 1})  # 验证码失效
        else:
            return JsonResponse({'status': 0})
    else:
        return JsonResponse({'status': 0})
