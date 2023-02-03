from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    body = models.CharField(max_length=500)
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_sender')
    msg_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_receiver')
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body

