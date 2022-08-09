from knox.views import LogoutView
from django.urls import path, include
from . import views


urlpatterns = [
    path("register/", views.RegisterAPI.as_view(), name='register'),
    path("login", views.LoginAPI.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


