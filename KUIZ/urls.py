from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('exam/<int:pk>', views.exam, name='exam'),
    path('detail/<str:topic>', views.detail_by_topic, name='detail_by_topic'),
    path('exam/<int:pk>/question/<int:question_id>', views.question, name='question'),
    path('exam/<int:pk>/question/<int:question_id>/answer', views.answer, name='answer'),
    path('exam/<int:pk>/question/result', views.result, name='result'),
    path('create/', views.new_quiz, name='new_quiz'),
]
