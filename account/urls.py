from django.urls import path

from account import views

urlpatterns = [
    path('register/', views.registration_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('user/', views.profile_view, name="user")
]