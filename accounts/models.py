from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize
import json


# Create your models here.

class DateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class User(AbstractUser):
    email = models.EmailField( max_length=254, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length = 16, unique = True)
    is_verified = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    bio = models.CharField(max_length = 300, blank = True, null = True)
    follows = models.ManyToManyField('User', blank=True, related_name='followed_by')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name' ,'date_of_birth', 'phone_number']

    def follow(self, user, force = False):
        """ Helper function to add user to a follower list. """
        if user.id == self.id:
            return
        if force:
            self.follows.add(user)
            return

        if user.is_private:
            FollowRequest.objects.create(requester=self, to_follow=user)
        else:
            self.follows.add(user)


    def unfollow(self, user):
        """ Helper function to remove a user from this users following list. """
        self.follows.remove(user)


    def following(self):
        """ Returns a QuerySet of Users that this user follows. """
        follow = self.follows.all()
        serialized_data = serialize("json", follow,  fields=["username",])
        serialized_data = json.loads(serialized_data)
        return serialized_data


    def followers(self):
        """ Returns a QuerySet of Users following this user. """
        follow = self.followed_by.all()
        serialized_data = serialize("json", follow, fields=["username",])
        serialized_data = json.loads(serialized_data)
        return serialized_data

    def following_count(self):
        """ Returns a QuerySet of total Users that this user follows. """
        return self.follows.all().count()


    def followers_count(self):
        """ Returns a QuerySet of total Users following this user. """
        return self.followed_by.all().count()


class FollowRequest(DateModel):

    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    to_follow = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requests'
    )

    def accept(self):
        self.requester.follow(self.to_follow, force=True)
        self.delete()

    def reject(self):
        self.delete()

    def __str__(self):
        return f'{self.id}: {self.requester} -> {self.to_follow}'

