from django.urls import path, include
from . import views

urlpatterns = [
    path("contents/", views.ContentsAPI.as_view()),
    path("content/<int:id>/", views.ContentAPI.as_view()),
    path("comments/", views.CommentsAPI.as_view()),
    path("comments/<int:id>/", views.CommentAPI.as_view()),
]


