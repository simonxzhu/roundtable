from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
from enum import Enum


class UserManager(models.Manager):
    # Validate register
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # Validate registration
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email is not valid."
            # check if unique email
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors["email"] = "The email is already taken."
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['c_password'] != postData['password']:
            errors["c_password"] = "Confirm password doesn't match password."

        return errors

    # Validate login
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['login_email'])
        print(user)
        if len(user) == 0:
            errors["login"] = "You could not be logged in."
        else:
            # if user exists, check if the password matches the hashed password in the db.
            if bcrypt.checkpw(postData['login_password'].encode(), user[0].password.encode()):
                print("password match")
            else:
                print("password doesn't match")
                errors["login"] = "You could not be logged in."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.first_name


class EventManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print(postData['time'])
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title']) < 2:
            errors["title"] = "Title should be at least 2 characters."
        if len(postData['location']) < 2:
            errors["location"] = "Location should be at least 2 characters."

        # postData['time'] returns 2019-02-13T13:00
        if postData['time'] is "":
            errors["time"] = "Time is required"
        else:
            event_time = postData['time']
            current_time = datetime.now().isoformat()

            if event_time < current_time:
                errors["time"] = "Time should not be in the past."

        return errors



class Event(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateTimeField()
    location = models.CharField(max_length=100)
    hosted_by = models.ForeignKey(User, related_name="host_events", on_delete=models.CASCADE)
    users_who_join = models.ManyToManyField(User, related_name="join_events")
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    alias = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255)
    url = models.CharField(max_length=400)
    display_phone = models.CharField(max_length=45)
    review_count = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    events = models.ManyToManyField(Event, related_name="restaurants")

    display_address = models.TextField()

    photo1_url = models.CharField(max_length=100, default=None, blank=True, null=True)
    photo2_url = models.CharField(max_length=100, default=None, blank=True, null=True)
    photo3_url = models.CharField(max_length=100, default=None, blank=True, null=True)

    price = models.CharField(max_length=45, default="", blank=True, null=True)

    # XXX HOURS!

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    rater = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="ratings", on_delete=models.CASCADE)

