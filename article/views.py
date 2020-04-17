import json, time
import os

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

from article.models import Pic, Article


def get_list(request):
    """获取单页的文章信息信息"""

    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(Article.objects.all().order_by('id'))
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
        if isinstance(u, Article):
            return {
                'id': u.id,
                'title': u.title,
                'publish_time': u.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                'author': u.author,
                'cate': u.cate,
                'content': u.content
            }

    data = json.dumps(page_data, default=mydefault)
    print(data)
    return HttpResponse(data)


@csrf_exempt
def add(request):
    """
    接受前端模态框提交的添加文章信息
    """

    cate = True if request.POST.get('cate') == 'true' else False
    title = request.POST.get('title')
    content = request.POST.get('content')
    author = request.POST.get('author')
    print(cate, author, title, content)
    try:
        with transaction.atomic():
            Article.objects.create(title=title, cate=cate, author=author, content=content)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})


@csrf_exempt
def edit(request):
    """
    修改文章信息
    :param request:
    :return:
    """
    id = request.POST.get('id')
    cate = True if request.POST.get('cate') == '显密法要' else False
    title = request.POST.get('title')
    content = request.POST.get('content')
    author = request.POST.get('author')
    print(cate, author, title, content)
    try:
        with transaction.atomic():
            art = Article.objects.get(id=id)
            art.content = content
            art.author = author
            art.title = title
            art.cate = cate
            art.save()
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})


@csrf_exempt
def article_del(request):
    """删除文章"""
    oper = request.POST.get('oper')
    id = request.POST.get('id')
    if oper == 'del':
        with transaction.atomic():
            Article.objects.get(id=id).delete()
    return HttpResponse()


@csrf_exempt
def celledit(request):
    try:
        if request.POST.get('oper') == 'edit':
            with transaction.atomic():
                id = request.POST.get('id')
                art = Article.objects.get(id=id)
                if request.POST.get('cate'):
                    print(request.POST.get('cate') == 'true')
                    cate = True if request.POST.get('cate') == 'true' else False
                    art.cate = cate
                elif request.POST.get('title'):
                    art.title = request.POST.get('title')
                elif request.POST.get('author'):
                    art.author = request.POST.get('author')
                art.save()
    except Exception as tips:
        print(tips)

    return HttpResponse()


@xframe_options_sameorigin  # 允许页面嵌套时发起访问
@csrf_exempt
def pic_upload(request):
    """
    前端上传图片所使用的试图函数
    :param request: 文件
    :return:{"error":0,"url":"图片全路径"}
    图片所在的服务器路径
    """

    file = request.FILES.get("imgFile")

    if file:
        # 获取图片所在的服务的全路径
        img_url = request.scheme + "://" + request.get_host() + "/static/img/" + str(file)
        result = {"error": 0, "url": img_url}
        Pic.objects.create(img=file)
    else:
        result = {"error": 1, "url": "上传失败"}
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_all_pic(request):
    """
    前端图片空间获取所有图片的试图函数
    :param request:
    :return:
    """
    # 找到图片所在的目录  方便进行回显
    pic_dir = request.scheme + "://" + request.get_host() + '/static/'
    pic_list = Pic.objects.all()
    rows = []
    for i in list(pic_list):
        # 获取图片的后缀
        path, pic_suffix = os.path.splitext(i.img.url)
        rows.append({
            "is_dir": False,
            "has_file": False,
            "filesize": i.img.size,
            "dir_path": "",
            "is_photo": True,
            "filetype": pic_suffix,
            "filename": i.img.name,
            "datetime": "2018-06-06 00:36:39"
        })

    data = {
        "moveup_dir_path": "",
        "current_dir_path": "",
        "current_url": pic_dir,
        "total_count": len(pic_list),
        "file_list": rows

    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def article_list(request):
    return render(request, 'article/article_list.html')
