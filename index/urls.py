from django.urls import path

from index import views

app_name = 'cmfz'

urlpatterns = [
    path('index/', views.index, name='index'),
]
