"""
    File created for management of the URLs (URLconf)
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('downloads/', views.downloads, name='downloads'),
    path('testy/', views.testing, name = 'testing'),
    path('methods/', views.MethodList, name='methods_list'),
    path('addMethod/', views.addDepthMethod, name='method_form')
]