from django.urls import path
from .views import MessageView

urlpatterns = [
    path('chats/<int:friend_id>',MessageView.as_view()),
]
