from django.shortcuts import render, redirect

# Create your views here.
from carousel.models import Carousel


def index(request):
    """
    获取session中的adminname,获取轮播图，渲染首页
    :param request:
    :return:
    """
    if request.session.get('adminname'):
        carousels = list(Carousel.objects.all())[:3]
        return render(request, 'index/index.html',{'adminname':request.session.get('adminname'),'carousels':carousels})
    else:
        return redirect('user:login')
