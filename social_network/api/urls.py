from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
   UserTweetViewset, TweetDetailView, ShareTweetView,
   AddCommentView, AddReplyView, TweetView, AddLikeView, CommentView
)
router = DefaultRouter()
router.register('tweet',UserTweetViewset)

urlpatterns = [
   path('get-tweet/', include(router.urls)),
   path('get-tweet/<int:pk>/', include(router.urls)),
   path('tweet/', TweetView.as_view(), name = 'tweets'),
   path('tweet/<int:id>/', TweetDetailView.as_view(), name = 'tweet'),
   path('tweet-comment/<int:tweet_id>/', AddCommentView.as_view(), name = 'tweet-comment'),
   path('comment/<int:comment_id>/', CommentView.as_view(), name = 'comment'),
   path('tweet-reply/<int:tweet_id>/<int:comment_id>/', AddReplyView.as_view(), name = 'tweet-reply'),
   path('tweet-like/<int:tweet_id>/', AddLikeView.as_view(), name = 'tweet-like'),
   path('share-tweet/<int:tweet_id>/', ShareTweetView.as_view(), name = 'share-tweet'),
]

