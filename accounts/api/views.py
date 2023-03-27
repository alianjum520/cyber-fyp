from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer,
                          UserSerializer, ChangePasswordSerializer, FollowRequestSerializer,
                          FollowersAndFollowingSerializer, FindUserSerializer, ForgetPasswordSerializer
                        )
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            serializer.save()
            user_data = serializer.data
            print(user_data)
            user = User.objects.get(username=user_data['username'] ,email=user_data['email'])
            user.is_verified = False
            user.save()
            otp = random.randint(1000,9999)
            create_otp= OTPVerification.objects.create(user=user,otp = otp)
            future_time = create_otp.created_at + timedelta(minutes=2)
            create_otp.expiration_time  = future_time
            create_otp.save()
            print(otp)
            print(create_otp)

            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):

    def post(self, request):

        user = OTPVerification.objects.get(user = request.user)
        check_otp = request.data.get('otp')
        print(check_otp)

        print(user.user.username)
        utc=pytz.UTC
        if utc.localize(datetime.now()) < user.expiration_time:
            print(user.created_at)
            print(user.expiration_time)
            if user.otp == check_otp:
                user.user.is_verified = True
                user.expired = True
                user.user.save()
                print(user.user.is_verified)
                return Response('User Verified Successfully')
            else:
                return Response('Invalid Token')
            
        else:
            user.expired = True
            user.save()
            return Response('Token Expired')


class RenewOtp(APIView):

    def post(self, request):

        otp = OTPVerification.objects.get(user = request.user)
        print(otp.user.is_verified)
        if otp.user.is_verified == False:
            create_otp = random.randint(1000,9999)
            utc=pytz.UTC
            otp.otp = create_otp
            future_time = utc.localize(datetime.now()) + timedelta(minutes=2)
            print(future_time)
            otp.expiration_time  = future_time
            otp.expired = False
            otp.save()
            print(otp)
            print(create_otp)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

"""From here the work of forgot password starts"""
class FindAccountView(APIView):
    serializer_class = FindUserSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            query = User.objects.get(email=request.data.get("email"))
            serializer = self.serializer_class(query)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"Fail": "This user doest not exists"}, status = status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):

        try:
            otp = OTPVerification.objects.get(user__email = request.data.get("email"))
            create_otp = random.randint(1000,9999)
            utc=pytz.UTC
            otp.otp = create_otp
            future_time = utc.localize(datetime.now()) + timedelta(minutes=2)
            print(future_time)
            otp.expiration_time  = future_time
            otp.expired = False
            otp.save()
            print(otp.otp)
            return Response({"Success": "Otp sent successfully"}, status=status.HTTP_200_OK)
        except OTPVerification.DoesNotExist:
            return Response({"Fail": "Otp sent failure"}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmOtp(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user = OTPVerification.objects.get(user__email = request.data.get("email"))
        check_otp = request.data.get('otp')
        print(check_otp)

        print(user.user.username)
        utc=pytz.UTC
        if utc.localize(datetime.now()) < user.expiration_time:
            print(user.created_at)
            print(user.expiration_time)
            if user.otp == check_otp:
                user.expired = True
                user.user.save()
                return Response({'Otp matched'}, status=status.HTTP_200_OK)
            else:
                return Response({'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            user.expired = True
            user.save()
            return Response('Token Expired', status=status.HTTP_400_BAD_REQUEST)


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
            print(otp.otp)
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
    permission_classes = [IsAuthenticated]

    def put(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = self.serializer_class(queryset, data = request.data,  context={'request': request})
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class FollowUserAPIView(APIView):

    """
    APIView to make a request (or directly follow is user to be followed
    has a public account) by an authenticated user.
    """
    permission_classes = (IsAuthenticated,)

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

    permission_classes = (IsAuthenticated,)

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

    permission_classes = (IsAuthenticated,)
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        return self.request.user.requests.all()

class FollowingAndFollowersView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = FollowersAndFollowingSerializer

    def get(self, request):

        queryset = User.objects.get(username=request.user.username)

        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status = status.HTTP_200_OK)
