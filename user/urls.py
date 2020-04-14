from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('get_list/', views.get_list, name='get_list'),
    path('edit/', views.edit, name='edit'),
    path('add/', views.add, name='add'),
    path('check_username/', views.check_username, name='check_username'),
    path('get_weeks_data/', views.get_weeks_data, name='get_weeks_data'),
    path('get_distribute/', views.get_distribute, name='get_distribute'),
    path('celledit/', views.celledit, name='celledit'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_distributed/', views.user_distributed, name='user_distributed'),
]
