from social_network.models import Tweet, Comment, Like
from rest_framework import serializers
from accounts.models import User
import CyberbullyingDetectionClass as model

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


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


class LikeSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only = True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'like']


class ShareSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only = True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'text']


class UserTweetSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only = True, many = False)

    class Meta:
        model = Tweet
        fields = ['id','user', 'text',  'updated_at']

    def validate(self, attrs):
        #import CyberbullyingDetectionClass as model
        model.text[0] = attrs['text']
        result_val = model.scan.detectBullying(model.text)
        #print(result_val)
        if(result_val['Offensive Words'] != "None"):
            raise serializers.ValidationError({"comment": "You have entered offensive words: " + str(result_val['Offensive Words'])\
                + ",Severity Level of your Content is: " + str(result_val['Severity Level']) 
                + ",Type of Bullying you are doing is: " + str(result_val['Type'])

                                               })
        elif(result_val['Offensive Words']=="None"):
            return attrs
        return attrs
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        tweet = Tweet.objects.create(**validated_data)

        return tweet


class ShareTweetSerializer(serializers.ModelSerializer):

    parent = UserTweetSerializer(read_only = True)
    user = UserSerializer(read_only = True)

    class Meta:
        model = Tweet
        fields = ['id', 'text','user', 'parent']


class TweetDetailSerializer(serializers.ModelSerializer):

    likes = LikeSerializer(many = True)
    comments = CommentSerializer(many = True)
    share = ShareSerializer(many = True)
    user = UserSerializer(read_only = True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'text', 'share', 'comments', 'likes', 'updated_at']


class AddCommentSerializer(serializers.ModelSerializer):

    tweet = UserTweetSerializer(read_only = True)
    user = UserSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'comment']

    def validate(self, attrs):
        #import CyberbullyingDetectionClass as model
        model.text[0] = attrs['comment']
        result_val = model.scan.detectBullying(model.text)
        #print(result_val)
        if(result_val['Offensive Words'] != "None"):
            raise serializers.ValidationError({"comment": "You have entered offensive words: " + str(result_val['Offensive Words'])\
                + ",Severity Level of your Content is: " + str(result_val['Severity Level']) 
                + ",Type of Bullying you are doing is: " + str(result_val['Type'])

                                               })
        elif(result_val['Offensive Words']=="None"):
            return attrs
        return attrs

class AddReplySerializer(serializers.ModelSerializer):

    tweet = UserTweetSerializer(read_only = True)
    user = UserSerializer(read_only = True)
    parent = AddCommentSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'comment', 'parent']

    def validate(self, attrs):
        model.text[0] = attrs['comment']
        result_val = model.scan.detectBullying(model.text)
        #print(result_val)
        if(result_val['Offensive Words'] != "None"):
            raise serializers.ValidationError({"comment": "You have entered offensive words: " + str(result_val['Offensive Words'])\
                + ",Severity Level of your Content is: " + str(result_val['Severity Level']) 
                + ",Type of Bullying you are doing is: " + str(result_val['Type'])

                                               })
        elif(result_val['Offensive Words']=="None"):
            return attrs
        return attrs


class AddLikeSerializer(serializers.ModelSerializer):

    tweet = UserTweetSerializer(read_only = True)
    user = UserSerializer(read_only = True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'like']
