from django.urls import path
from carousel import views
app_name = 'carousel'

urlpatterns = [
    path('get_list/',views.get_list,name='get_list'),

]
