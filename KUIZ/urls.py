from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('exam/<int:pk>', views.exam, name='exam'),
    path('detail/<str:topic>', views.detail_by_topic, name='detail_by_topic'),
    path('exam/<int:pk>/question/<int:question_id>', views.question, name='question'),
    path('exam/<int:pk>/question/<int:question_id>/answer', views.answer, name='answer'),
    path('exam/<int:pk>/result', views.result, name='result'),
    path('create/', views.new_quiz, name='new_quiz'),
    path('edit/<int:pk>', views.edit_quiz, name='edit_quiz'),
    path('check/', views.check, name='check'),
    path('check/<int:pk>/', views.check_quiz, name='check_per_quiz'),
    path('check/<int:pk>/user/<int:id>', views.check_student, name='check_per_student'),
    path('check/<int:pk>/user/<int:id>/answer', views.update_answer, name='update_answer'),
    path('exam/<int:pk>/password', views.password, name='password'),
]
