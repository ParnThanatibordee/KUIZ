from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),    
]