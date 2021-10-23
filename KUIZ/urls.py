from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exam/<int:pk>', views.exam, name='exam'),
]
