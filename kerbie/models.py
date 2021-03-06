from django.db import models
from django.contrib.auth.models import User
import datetime
import os

class comment(models.Model):
    messageId = models.IntegerField(default=0) #connects it to a specific post
    commentId = models.IntegerField(default=0)
    username = models.CharField(max_length=30)
    commentBody = models.CharField(max_length=200)
    date = models.DateTimeField()
    def __unicode__(self):
        return self.commentBody

class post(models.Model):
    user_wall = models.CharField(max_length=30) #matches the userId of the wall being written on
    messageId = models.IntegerField(default=0)
    username = models.CharField(max_length=30) #keeps track of who posted the message
    postBody = models.CharField(max_length=200)
    date = models.DateTimeField()
    def __unicode__(self):
        return self.postBody

#class wall(models.Model):
	#username = models.CharField(max_length=30)
	#def __init__(username):
	#	self.username = username

class search(models.Model):
    name = models.CharField(max_length=50)

def get_image_path(instance, filename):
	return os.path.join(str(instance.userId), filename)
	
class addImage(models.Model):
	photoId = models.IntegerField(default=0)
	userId = models.IntegerField(default=0)
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to=get_image_path, blank=True)
	date = models.DateTimeField()
	
class userProfile(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=30)
    userId = models.IntegerField(default=0)
    photoId = models.IntegerField(default=0)
    gender = models.CharField(max_length=1)
    location = models.CharField(max_length=50)
    joined = models.DateTimeField()
    birthday = models.DateTimeField()
    def __unicode__(self):
		return self.user.username
