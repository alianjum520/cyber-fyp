from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer,
                          UserSerializer, ChangePasswordSerializer, FollowRequestSerializer,
                          FollowersAndFollowingSerializer, FindUserSerializer, ForgetPasswordSerializer
                        )
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status
from accounts.models import User, FollowRequest, OTPVerification
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
import random
from datetime import datetime,timedelta
import pytz
from .permissions import IsVerifiedUser
from django.core.mail import send_mail


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            
            user_data = serializer.validated_data
            try:
                serializer.save()
                user_data = serializer.data
                user = User.objects.get(username=user_data['username'] ,email=user_data['email'])
                user.is_verified = False
                user.save()
                otp = random.randint(1000,9999)
                create_otp= OTPVerification.objects.create(user=user,otp = otp)
                future_time = create_otp.created_at + timedelta(minutes=2)
                create_otp.expiration_time  = future_time
                create_otp.save()
                send_mail(
                    'Otp To Verify Account',
                    'Your Otp is: {}'.format(otp),
                    'alt.do-doxpg7ov@yopmail.com',
                    [user.email],
                    fail_silently=False,
                )
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):

    def post(self, request):

        user = OTPVerification.objects.get(user = request.user)
        check_otp = request.data.get('otp')
        
        utc=pytz.UTC
        if utc.localize(datetime.now()) < user.expiration_time:
            if user.otp == check_otp:
                user.user.is_verified = True
                user.expired = True
                user.user.save()
                
                return Response({"Token":'User Verified Successfully'}, status = status.HTTP_200_OK)
            else:
                return Response({'Token':'Invalid Token'},status =status.HTTP_400_BAD_REQUEST)
            
        else:
            user.expired = True
            user.save()
            return Response({"Token":'Token Expired'}, status= status.HTTP_400_BAD_REQUEST)


class RenewOtp(APIView):

    def post(self, request):

        otp = OTPVerification.objects.get(user = request.user)
       
        if otp.user.is_verified == False:
            create_otp = random.randint(1000,9999)
            utc=pytz.UTC
            otp.otp = create_otp
            future_time = utc.localize(datetime.now()) + timedelta(minutes=2)
        
            otp.expiration_time  = future_time
            otp.expired = False
            otp.save()
            send_mail(
                    'Otp To Verify Account',
                    'Your Otp is: {}'.format(otp.otp),
                    'alt.do-doxpg7ov@yopmail.com',#zudaxukutro-4405@yopmail.com
                    [otp.user.email],
                    fail_silently=False,
                )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

"""From here the work of forgot password starts"""
class FindAccountView(APIView):
    serializer_class = FindUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            query = User.objects.get(email=request.data.get("email"))
            serializer = self.serializer_class(query)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"Fail": "This user doest not exists"}, status = status.HTTP_400_BAD_REQUEST)


class SendOtp(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            otp = OTPVerification.objects.get(user__email = request.data.get("email"))
            create_otp = random.randint(1000,9999)
            utc=pytz.UTC
            otp.otp = create_otp
            future_time = utc.localize(datetime.now()) + timedelta(minutes=2)
            
            otp.expiration_time  = future_time
            otp.expired = False
            otp.save()
            send_mail(
                    'Otp To Verify Account',
                    'Your Otp is: {}'.format(otp.otp),
                    'alt.do-doxpg7ov@yopmail.com',
                    [otp.user.email],
                    fail_silently=False,
                )
            return Response({"Success": "Otp sent successfully"}, status=status.HTTP_200_OK)
        except OTPVerification.DoesNotExist:
            return Response({"Fail": "Otp sent failure"}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmOtp(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user = OTPVerification.objects.get(user__email = request.data.get("email"))
        check_otp = request.data.get('otp')

        print(user.user.username)
        utc=pytz.UTC
        if utc.localize(datetime.now()) < user.expiration_time:
            print(user.created_at)
            print(user.expiration_time)
            if user.otp == check_otp:
                user.expired = True
                user.user.save()
                return Response({"Success":'Otp matched'}, status=status.HTTP_200_OK)
            else:
                return Response({"Fail":'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            user.expired = True
            user.save()
            return Response({"Fail":'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)


class ResendOtp(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):

        try:
            otp = OTPVerification.objects.get(user__email = request.data.get("email"))
            create_otp = random.randint(1000,9999)
            utc=pytz.UTC
            otp.otp = create_otp
            future_time = utc.localize(datetime.now()) + timedelta(minutes=2)
            otp.expiration_time  = future_time
            otp.expired = False
            otp.save()
            send_mail(
                    'Otp To Verify Account',
                    'Your Otp is: {}'.format(otp.otp),
                    'alt.do-doxpg7ov@yopmail.com',
                    [otp.user.email],
                    fail_silently=False,
                )
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ForgetPasswordView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def put(self, request):
        try:
            queryset = User.objects.get(email=request.data.get("email"))
            serializer = self.serializer_class(queryset, data = request.data,  context={'request': request.data.get("email")})
            if serializer.is_valid():

                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)

"""End of Forgot password work"""


class AccountView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsVerifiedUser]

    def get(self, request):

        queryset = User.objects.get(username=request.user.username)

        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def patch(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = self.serializer_class(queryset, data = request.data, partial = True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsVerifiedUser]

    def put(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = self.serializer_class(queryset, data = request.data,  context={'request': request})
        if serializer.is_valid():

            serializer.save()
            return Response({"Password":'Password Changed Successfully'}, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class FollowUserAPIView(APIView):

    """
    APIView to make a request (or directly follow is user to be followed
    has a public account) by an authenticated user.
    """
    permission_classes = (IsVerifiedUser,)

    def post(self,request, to_follow_id):

        if not to_follow_id:
            return Response(
                {'error': 'Follow request\'s user ID not provided.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, id=to_follow_id)
        request.user.follow(user)
        return Response({'detail': 'requested'})


class FollowRequestActionAPIView(APIView):

    """
    APIView to accept or reject a FollowRequest by the person
    who is being requested to act upon said request.
    """

    permission_classes = (IsVerifiedUser,)

    def post(self, request, action, follow_request_id):

        follow_request = get_object_or_404(
            FollowRequest, id=follow_request_id
        )

        resp = {'detail': 'pending'}

        if action == 1:
            resp['detail'] = 'accepted'
            follow_request.accept()
        elif action == 0:
            resp = {'detail': 'rejected'}
            follow_request.reject()


        return Response(resp)


class FollowRequestListView(ListAPIView):

    permission_classes = (IsVerifiedUser,)
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        return self.request.user.requests.all()

class FollowingAndFollowersView(APIView):

    permission_classes = [IsVerifiedUser]
    serializer_class = FollowersAndFollowingSerializer

    def get(self, request):

        queryset = User.objects.get(username=request.user.username)

        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def delete(self,request,pk):

        """
        This function is used to delete the like from liked table
        """
        remover = User.objects.get(username = request.user.username)
        user = User.objects.get(pk = pk)
        remover.follows.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveFollower(APIView):

    permission_classes = [IsVerifiedUser]
    serializer_class = FollowersAndFollowingSerializer

    def delete(self,request,pk):

        """
        This function is used to delete the like from liked table
        """
        remover = User.objects.get(username = request.user.username)
        user = User.objects.get(pk = pk)
        remover.followed_by.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)
