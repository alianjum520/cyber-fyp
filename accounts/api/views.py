from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer,
                          UserSerializer, ChangePasswordSerializer, FollowRequestSerializer,
                          FollowersAndFollowingSerializer
                        )
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from rest_framework import status
from accounts.models import User, FollowRequest
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

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
