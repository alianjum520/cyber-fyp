from django.db import models
from accounts.models import DateModel, User
# Create your models here.

class Tweet(DateModel):
    text  = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='share')
    
    def __str__(self):
        return  self.text


class Comment(DateModel):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete = models.CASCADE, related_name = 'comments')
    comment  = models.CharField(max_length = 500 )
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.user) + ' comment ' + str(self.comment)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class Like(DateModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete = models.CASCADE, related_name="likes")
    like = models.BooleanField(default=False)