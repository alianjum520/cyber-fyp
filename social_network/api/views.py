from .serializers import (UserTweetSerializer, TweetDetailSerializer,
                          AddCommentSerializer, AddReplySerializer,
                          )
from social_network.models import Tweet, Comment
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated,AllowAny


class UserTweetViewset(viewsets.ModelViewSet):

    """
    This viewset is used by authenticated user only
    user can crete update and delete its album
    """

    permission_classes= [IsAuthenticated]
    queryset = Tweet.objects.all()
    serializer_class = UserTweetSerializer

    def get_queryset(self):

        """
        This function is used to set user of the album
        """
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set


class TweetDetailView(APIView):

    permission_classes = [AllowAny]#in future will see according to public and private account

    def get(self,request,id):

        try:
            tweet = Tweet.objects.get(id=id)
            serializer = TweetDetailSerializer(tweet)

            return Response(serializer.data)

        except Tweet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddCommentView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AddCommentSerializer


    def post(self, request, tweet_id):
        try:
            tweet = Tweet.objects.get(id = tweet_id)

        except Tweet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():

            serializer.save(tweet=tweet, user=self.request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class AddReplyView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AddReplySerializer


    def post(self, request, tweet_id, comment_id):
        try:
            tweet = Tweet.objects.get(id = tweet_id)
            comment = Comment.objects.get(id = comment_id)

        except Comment.DoesNotExist or Tweet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():

            serializer.save(tweet = tweet, user = self.request.user, parent = comment)
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)