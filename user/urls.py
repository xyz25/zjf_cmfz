from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('check_user/', views.check_user, name='check_user'),
    path('login_form/', views.login_form, name='login_form'),
    path('logout/', views.logout, name='logout'),
]
