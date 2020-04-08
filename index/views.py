from django.shortcuts import render


# Create your views here.
from carousel.models import Carousel


def index(request):
    carousels = list(Carousel.objects.all())[:3]
    return render(request, 'index/index.html',{'adminname':request.session.get('adminname'),'carousels':carousels})
