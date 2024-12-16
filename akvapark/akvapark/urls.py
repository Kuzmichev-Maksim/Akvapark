"""
URL configuration for akvapark project.
"""
from django.contrib import admin
from django.urls import path
from coral import views 


urlpatterns = [
    path('', views.login_view, name='login'),
    path('regis/', views.regis, name='regis'),  
    path('home/', views.home, name='home'),  
    path('attractions/', views.attractions, name='attractions'), 
    path('tariffs/', views.tariffs, name='tariffs'), 
    path('account/', views.account, name='account'), 
    path('tickets/', views.tickets, name='tickets'), 
    path('admin/', views.admin_view, name='admin_page'),
      path('add-review/', views.add_review, name='add_review'),
]