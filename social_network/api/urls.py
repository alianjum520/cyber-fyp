from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
   UserTweetViewset, TweetDetailView,
   AddCommentView, AddReplyView
)
router = DefaultRouter()
router.register('tweet',UserTweetViewset)

urlpatterns = [
   path('get-tweet/', include(router.urls)),
   path('get-tweet/<int:pk>/', include(router.urls)),
   path('tweet/<int:id>/', TweetDetailView.as_view(), name = 'tweet'),
   path('tweet-comment/<int:tweet_id>/', AddCommentView.as_view(), name = 'tweet-comment'),
   path('tweet-reply/<int:tweet_id>/<int:comment_id>/', AddReplyView.as_view(), name = 'tweet-reply')
]

