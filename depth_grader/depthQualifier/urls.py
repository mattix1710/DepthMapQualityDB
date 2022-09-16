"""
    File created for management of the URLs (URLconf)
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sequences/', views.SequenceList.as_view(), name='sequences_list'),
    path('addSequence/', views.addSequence, name='sequence_form'),
    path('testy/', views.testing, name = 'seq_test'),
]