from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import User
from message.models import Message
from .serializers import MessageSerializer
from rest_framework.views import APIView

class MessageView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, friend_id):
        sender = User.objects.get(username = request.user.username)
        receiver = User.objects.get(id = friend_id)
        queryset = Message.objects.filter(msg_sender = receiver, msg_receiver = sender)
        model_set2 = Message.objects.filter(msg_sender = sender, msg_receiver = receiver)
        queryset2 = queryset.union(model_set2, all=True)
        serializer = self.serializer_class(queryset2, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, friend_id):
        try:
            sender = User.objects.get(username = request.user.username)
            receiver = User.objects.get(id = friend_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():

            serializer.save(msg_sender = sender, msg_receiver = receiver)
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

