from social_network.models import Tweet, Comment
from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['username']


class UserTweetSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only = True, many = False)

    class Meta:
        model = Tweet
        fields = ['user', 'text']

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        tweet = Tweet.objects.create(**validated_data)

        return tweet


class ReplySerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment']


class CommentSerializer(serializers.ModelSerializer):

    user  = UserSerializer(read_only = True)
    replies = ReplySerializer(many = True)

    class Meta:
        model = Comment
        fields =['id','user', 'comment', 'replies']


class TweetDetailSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many = True)

    class Meta:
        model = Tweet
        fields = ['id' ,'text', 'comments']


class AddCommentSerializer(serializers.ModelSerializer):

    tweet = UserTweetSerializer(read_only = True)
    user = UserSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'comment']


class AddReplySerializer(serializers.ModelSerializer):

    tweet = UserTweetSerializer(read_only = True)
    user = UserSerializer(read_only = True)
    parent = AddCommentSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'comment', 'parent']





