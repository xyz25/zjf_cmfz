from django.urls import path

from data_interface import views

app_name = 'api'

urlpatterns = [
    path('first_page/', views.first_page, name='first_page'),
]
