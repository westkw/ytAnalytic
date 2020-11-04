from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ytAnalytic-home'),
    path('about/', views.about, name='ytAnalytic-about'),
    path('searched/', views.searched, name='ytAnalytic-searched'),
    path('video/', views.video, name='ytAnalytic-video'),
    path('channel/', views.channel, name='ytAnalytic-channel')
]