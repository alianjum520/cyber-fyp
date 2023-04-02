from .serializers import (UserTweetSerializer, TweetDetailSerializer,
                          AddCommentSerializer, AddReplySerializer,
                          AddLikeSerializer
                          
                          )
from social_network.models import Tweet, Comment, Like
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.api.permissions import IsVerifiedUser


class UserTweetViewset(viewsets.ModelViewSet):

    """
    This viewset is used by authenticated user only
    user can crete update and delete its tweet
    """

    permission_classes= [IsVerifiedUser]
    queryset = Tweet.objects.all()
    serializer_class = UserTweetSerializer

    def get_queryset(self):

        """
        This function is used to set user of the tweet
        """
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set


class TweetView(APIView):

    permission_classes = [IsVerifiedUser]#in future will see according to public and private account

    def get(self,request):

        tweet = Tweet.objects.all()
        serializer = TweetDetailSerializer(tweet, many = True)

        return Response(serializer.data)


class TweetDetailView(APIView):

    permission_classes = [IsVerifiedUser]#in future will see according to public and private account

    def get(self,request,id):

        try:
            tweet = Tweet.objects.get(id=id)
            serializer = TweetDetailSerializer(tweet)

            return Response(serializer.data)

        except Tweet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddCommentView(APIView):

    permission_classes = [IsVerifiedUser]
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


class CommentView(APIView):

    permission_classes = [IsVerifiedUser]
    serializer_class = AddCommentSerializer


    def put(self, request, comment_id):
        comments = Comment.objects.get(id = comment_id, user = self.request.user)

        serializer = self.serializer_class(comments, data = request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,comment_id):

        """
        This function is used to delete the like from liked table
        """
        try:
            comment = Comment.objects.get(id = comment_id, user = self.request.user)
            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddReplyView(APIView):

    permission_classes = [IsVerifiedUser]
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



class AddLikeView(APIView):

    permission_classes = [IsVerifiedUser]
    serializer_class = AddLikeSerializer


    def post(self, request, tweet_id):
        try:
            tweet = Tweet.objects.get(id = tweet_id)

        except Tweet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if Like.objects.filter(tweet = tweet_id, user = self.request.user, like = True).exists():
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():

                serializer.save(tweet=tweet, user=self.request.user, like=True)
                return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,tweet_id):

        """
        This function is used to delete the like from liked table
        """
        try:
            like = Like.objects.get(tweet = tweet_id, user = self.request.user)
            like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
