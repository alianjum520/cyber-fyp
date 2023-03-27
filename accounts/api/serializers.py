from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User, FollowRequest, OTPVerification
from django.contrib.auth.hashers import check_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only = True,required=True,)


    class Meta:
        model = User
        fields = [
            'username', 'email', 'date_of_birth', 'first_name',
            'last_name', 'phone_number', 'password', 'password2'
                  ]

    def validate(self, attrs):

        from datetime import date

        today = date.today()
        get_year = today.year - attrs['date_of_birth'].year

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if get_year < 18:
            raise serializers.ValidationError({"date_of_birth": "You are not compatiable to use this app"})

        return attrs

    def create(self, validated_data):

        user = User.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data ['last_name'],
            date_of_birth = self.validated_data ['date_of_birth'],
            phone_number = self.validated_data ['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()



        return user


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = '__all__'
        '''fields = ['username', 'email', 'first_name',
            'last_name', 'phone_number', 'bio', 'is_private']'''


    def update(self, instance, validated_data):

        #this is used to update user serializer
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.save()

        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def update(self, instance, validated_data):
        current_password = self.context['request'].user.password
        password_check = validated_data.get('old_password')
        match_password = check_password(password_check, current_password)
        if match_password == True :
            user = User.objects.get(username = self.context['request'].user)
            user.set_password(validated_data.get('new_password'))
            user.save()
        else:
            raise serializers.ValidationError({"password": "Your password did not matched"})
        return instance


class FollowUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class FollowRequestSerializer(serializers.ModelSerializer):

    requester = FollowUserSerializer(read_only = True)
    to_follow = FollowUserSerializer(read_only = True)

    class Meta:
        model = FollowRequest
        fields = ['id', 'requester', 'to_follow']


class FollowersAndFollowingSerializer(serializers.ModelSerializer):

    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_following(self, model):
        return model.following()

    def get_followers(self, model):
        return model.followers()

    def get_following_count(self, model):
        return model.following_count()

    def get_followers_count(self, model):
        return model.followers_count()

    class Meta:
        model = User
        fields = ['username', 'following', 'followers', 'following_count', 'followers_count']


class OTPVerificationSerializer(serializers.ModelSerializer):
    otp2 = serializers.CharField(required=True)

    class Meta:
        model = OTPVerification
        fields = "__all__"


class FindUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']

class ForgetPasswordSerializer(serializers.ModelSerializer):

    new_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['new_password']

    def update(self, instance, validated_data):
        
        user = User.objects.get(email = self.context['request'])
        user.set_password(validated_data.get('new_password'))
        user.save()
    
        return instance