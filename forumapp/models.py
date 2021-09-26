from django.db import models
import re 
import bcrypt
from .models import *

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postData['fname']) < 2:
            errors['firstname']='First name must be at least 2 characters'
        if len(postData['lname']) < 2:
            errors['lastname']='First name must be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        elif User.objects.filter(email=postData['email']):
            errors['email'] = 'Email already exists'
        if len(postData['pword'])< 8:
            errors['password']= 'Password must be at least 8 characters'
        elif postData['pword'] != postData['cpword']:
            errors['password'] = 'Password and confirm password must match'
        return errors

    def login_validator(self, postData):
        errors = {}
        LoginUser = User.objects.filter(email=postData['email'])
        if len(LoginUser)>0:
            if bcrypt.checkpw(postData['pword'].encode(), LoginUser[0].password.encode()):
                print("Password matches")
            else:
                errors['password'] = 'password does not match!'
        else:
            errors['email'] = "There is no such user"
        return errors

    def post_validator(self, postData):
        errors = {}
        if len(postData['text'])<10:
            errors['text'] = "The quote must be at least ten characters"
        return errors

    def update_validator(self, postData):     
        errors={}
        if len(postData['fname'])<2:
            errors['firstname'] = "Your first name must be at least two characters"
        if len(postData['lname'])<2:
            errors['lastname'] = "Your last name must be at least two characters"
        UserRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if not UserRegex.match(postData['email']):
            errors['email'] = "Not a valid email"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete = models.CASCADE)
    text =  models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    text =  models.TextField(blank=True)
    post=models.ForeignKey(Post, related_name='comments',  on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()