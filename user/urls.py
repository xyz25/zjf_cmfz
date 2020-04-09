from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('get_list/', views.get_list, name='get_list'),
    path('edit/', views.edit, name='edit'),
    path('add/', views.add, name='add'),
    path('check_username/', views.check_username, name='check_username'),

]
