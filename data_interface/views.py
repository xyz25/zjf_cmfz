import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from album.models import Album, Chapter
from article.models import Article, Pic
from carousel.models import Carousel
from data_interface.defaults import album_default, article_default, carousel_default, album_chapter_default, all_default
from index.models import Admin
from user.models import User
from utils.md5_password import get_md5_password
from utils.random_code import get_random_code


def first_page(request):
    """一级页面接口"""
    user_id = request.GET.get('uid')
    data = {}
    if not user_id:
        data = {
            'status': 401,
            'msg': '用户未登录！！！！'
        }
        return JsonResponse(data)
    if not Admin.objects.filter(id=user_id):
        data = {
            'status': 401,
            'msg': '用户不存在！！！！'
        }
        return JsonResponse(data)
    type = request.GET.get('type')

    if type == 'album':
        """请求数据类型为专辑"""
        data = json.dumps(list(Album.objects.all()), default=album_default)
        return HttpResponse(data)

    if type == 'article':
        """请求数据类型为文章"""
        if not request.GET.get('sub_type'):
            return JsonResponse({
                'status': 401,
                'msg': '未指定文章类型！！！！'
            })
        else:
            if request.GET.get('sub_type') == 'ssyj':
                """请求数据类型为上师言教"""
                data = json.dumps(list(Article.objects.filter(cate=True)), default=article_default)
                return HttpResponse(data)
            elif request.GET.get('sub_type') == 'xmfy':
                """请求数据类型为显密法要"""
                data = json.dumps(list(Article.objects.filter(cate=False)), default=article_default)
                return HttpResponse(data)

    if type == 'all':
        """请求数据类型为专辑，轮播图，文章"""
        data['header'] = list(Carousel.objects.all())
        data['album'] = list(Album.objects.all())
        data['article_ssyj'] = list(Article.objects.filter(cate=True))
        data['article_xmfy'] = list(Article.objects.filter(cate=False))
        return HttpResponse(json.dumps(data, default=all_default))


def album_detail(request):
    user_id = request.GET.get('uid')
    data = {}
    if not user_id:
        data = {
            'status': 401,
            'msg': '用户未登录！！！！'
        }
        return JsonResponse(data)

    album_id = request.GET.get('id')
    if not album_id:
        data = {
            'status': 401,
            'msg': '未提供专辑标识！！！！'
        }
        return JsonResponse(data)

    def album_intro_default(u):
        if isinstance(u, Album):
            return {
                'thumbnail': str(u.img_src),
                'title': u.title,
                'score': u.score,
                'author': u.author,
                'broadcast': u.broadcast,
                'set_count': Chapter.objects.filter(album_id=u.id).count(),
                'brief': u.content
            }

    try:
        album = Album.objects.get(id=album_id)
    except:
        data = {
            'status': 401,
            'msg': '没有此专辑！！！'
        }
        return JsonResponse(data)
    data['introduction'] = json.dumps(album, default=album_intro_default)
    data['list'] = json.dumps(list(Chapter.objects.filter(album_id=album_id)), default=album_chapter_default)

    return JsonResponse(data)


@csrf_exempt
def register(request):
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    if not phone or not password:
        return JsonResponse({
            'status': 401,
            'msg': '密码或用户名有误！！！！'
        })
    if User.objects.filter(name=phone):
        return JsonResponse({
            "error": "-200",
            "error_msg": "该手机号已经存在!!!"
        })
    try:
        with transaction.atomic():
            salt = get_random_code()
            password = get_md5_password(salt, password)
            user = User.objects.create(name=phone, password=password, salt=salt)
            return JsonResponse({
                'password': password,
                'uid': user.id,
                'phone': phone
            })
    except Exception as tips:
        print(tips)
        return JsonResponse({
            "error": "-200",
            "error_msg": "注册失败！！！"
        })


@csrf_exempt
def user_modify(request):
    uid = request.POST.get('uid')
    if not User.objects.filter(id=uid):
        data = {
            'status': 401,
            'msg': '用户不存在！！！！'
        }
        return JsonResponse(data)

    photo = request.FILES.get('photo')
    decscription = request.POST.get('decscription')
    religions_name = request.POST.get('religions_name')
    address = request.POST.get('address')
    password = request.POST.get('password')

    try:
        with transaction.atomic():
            user = User.objects.get(id=uid)
            user.details = decscription if decscription else user.details
            user.religions_name = religions_name if religions_name else user.religions_name
            user.address = address if address else user.address
            user.img_src = photo
            if password:
                salt = get_random_code()
                password = get_md5_password(salt, password)
                user.password = password
                user.salt = salt
            user.save()
            data = {
                'password': user.password,
                'farmington': user.religions_name,
                'uid': user.id,
                'photo': '/static/' + str(user.img_src),
                'address': user.address,
                'description': user.details,
                'phone': user.name
            }
            return JsonResponse(data)
    except:
        data = {
            'status': 401,
            'msg': '操作有误！！！'
        }
        return JsonResponse(data)
