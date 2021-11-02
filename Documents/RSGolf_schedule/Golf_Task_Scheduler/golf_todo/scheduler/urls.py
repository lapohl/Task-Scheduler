from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from . import views
from django.conf.urls import url



urlpatterns = [
  path('', views.home, name='home'),
  path('index.html', views.home, name='home'),
  path('log.html', views.log, name='log'),
  path('task.html', views.tasks, name='task'),
  path('export/', views.export, name='export'),
  
]