from django.urls import path

from index import views

app_name = 'cmfz'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('check_user/', views.check_user, name='check_user'),
    path('login_form/', views.login_form, name='login_form'),
    path('logout/', views.logout, name='logout'),
]
