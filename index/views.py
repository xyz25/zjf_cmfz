import re
from django.shortcuts import render, redirect
from carousel.models import Carousel
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from redis import Redis
from index.models import Admin
from utils import send_msg
from utils.init_permission import init_permission
from utils.random_code import get_random_code

from zjf_cmfz import settings


def index(request):
    """
    获取session中的adminname,获取轮播图，渲染首页
    :param request:
    :return:
    """
    if request.session.get('adminname'):
        carousels = list(Carousel.objects.all())[:3]
        menu_list = request.session.get('menu_list')
        print(menu_list)
        return render(request, 'index/index.html',
                      {'adminname': request.session.get('adminname'), 'carousels': carousels,'menus':menu_list})
    else:
        return redirect('cmfz:login')


def login(request):
    """
    渲染登录界面
    """
    return render(request, 'index/login.html')


@csrf_exempt
def check_user(request):
    """
    检测用户名是否合法且存在，存在则发送手机验证码
    """
    red = Redis(host='127.0.0.1', port=6379)
    mobile = request.POST.get('mobile')

    if re.match(r'^[1][3,4,5,7,8][0-9]{9}$', mobile) and Admin.objects.filter(name=mobile):
        if red.get(mobile + '_2'):
            return JsonResponse({'status': 0})
        else:
            code = get_random_code()  # 生成随机验证码
            code = '123456'  # 方便测试，真实功能已实现
            red.set(mobile + '_1', code, 60)  # 60秒的有效期
            red.set(mobile + '_2', mobile, 60)  # 60秒内只能发送一次
            yunpian = send_msg.YunPian(settings.API_KEY)

            # yunpian.send_msg(mobile, code)    # 方便测试使用
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def login_form(request):
    """
    验证验证码是否正确，进行登录
    :param request:
    :return:
    """
    red = Redis(host='127.0.0.1', port=6379)
    mobile = request.GET.get('mobile')
    code = request.GET.get('code')
    if re.match(r'^[1][3,4,5,7,8][0-9]{9}$', mobile) and Admin.objects.filter(name=mobile):
        redis_code = red.get(mobile + '_1').decode()
        if redis_code == code:
            request.session['adminname'] = mobile
            init_permission(Admin.objects.get(name=mobile), request)
            return JsonResponse({'status': 1})  # 验证码验证成功
        else:
            return JsonResponse({'status': 0})  # 验证码验证失败
    else:
        return JsonResponse({'status': 0})


def logout(request):
    """管理员退出登录"""
    request.session.flush()
    return redirect('cmfz:login')
