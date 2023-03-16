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
    def validate(self, attrs):
        import CyberbullyingDetectionClass as model
        model.text[0] = attrs['body']
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