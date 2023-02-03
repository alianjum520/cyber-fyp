from rest_framework import serializers
from message.models import Message
from accounts.models import User

class MessageUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class MessageSerializer(serializers.ModelSerializer):
    msg_sender = MessageUserSerializer(read_only = True)
    msg_receiver = MessageUserSerializer(read_only = True)
    class Meta:
        model = Message
        fields = ['msg_sender', 'msg_receiver','body']
    