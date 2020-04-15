import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from album.models import Album, Chapter
from article.models import Article
from carousel.models import Carousel


def first_page(request):
    """一级页面接口"""
    user_id = request.GET.get('uid')
    data = {}
    # body = []  # 返回json数据的body参数
    if not user_id:
        data = {
            'status': 401,
            'msg': '用户未登录！！！！'
        }
        return JsonResponse(data)

    type = request.GET.get('type')

    def album_default(u):
        if isinstance(u, Album):
            return {
                'thumbnail': str(u.img_src),
                'title': u.title,
                'author': u.author,
                'type': '0',
                'set_count': Chapter.objects.filter(album_id=u.id).count(),
                'create_data': u.publish_time.strftime("%Y-%m-%d %H:%M:%S")
            }

    def article_default(u):
        if isinstance(u, Article):
            return {
                'thumbnail': '',
                'title': u.title,
                'author': u.author,
                'type': '1',
                'set_count': '',
                'create_data': u.publish_time.strftime("%Y-%m-%d %H:%M:%S")
            }

    def carousel_default(u):
        if isinstance(u, Carousel):
            return {
                'thumbnail': str(u.img_url),
                'desc': u.title,
                'id': u.id
            }

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
        data['header'] = json.dumps(list(Carousel.objects.all()), default=carousel_default)
        data['album'] = json.dumps(list(Album.objects.all()), default=album_default)
        data['article_ssyj'] = json.dumps(list(Article.objects.filter(cate=True)), default=article_default)
        data['article_xmfy'] = json.dumps(list(Article.objects.filter(cate=False)), default=article_default)
        return JsonResponse(data)



