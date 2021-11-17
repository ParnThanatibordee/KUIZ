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
    path('create/qiuz', views.new_quiz, name='new_quiz'),
    path('edit/quiz/<int:pk>', views.edit_quiz, name='edit_quiz'),
    path('create/question', views.new_question, name='new_question'),
    path('select/question/<int:pk>', views.select_question, name='select_question'),
    path('edit/question/<int:question_id>', views.edit_question, name='edit_question'),
    path('create/multiple/choice', views.new_multiple_choice, name='new_multiple_choice'),
    path('create/typing/choice', views.new_typing_choice, name='new_typing_choice'),
    path('select/question/choice/<int:pk>', views.select_question_to_edit_choice, name='select_question_to_edit_choice'),
    path('select/choice/<int:question_id>', views.select_choice, name='select_choice'),
    path('edit/multiple/choice/<int:choice_id>', views.edit_multiple_choice, name='edit_multiple_choice'),
    path('edit/typing/choice/<int:choice_id>', views.edit_typing_choice, name='edit_typing_choice'),
    path('feedback/', views.get_feedback, name='feedback')
]
