from django.urls import path
from carousel import views

app_name = 'carousel'

urlpatterns = [
    path('get_list/', views.get_list, name='get_list'),
    path('edit/', views.edit, name='edit'),
    path('add/', views.add, name='add'),
    path('get_status/', views.get_status, name='get_status'),
    path('carousel_list/', views.carousel_list, name='carousel_list'),

]
