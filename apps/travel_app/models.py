from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        if len(User.objects.filter(user_name = postData['user_name'])) > 0:
            errors.append("Username already exists")


        if len(postData['name']) < 2:
            errors.append('Name must be at least 2 characters')
        elif not NAME_REGEX.match(postData['name']):
            errors.append('Name must only contain alphabet')
        if len(postData['user_name']) < 2:
            errors.append('User name must be at least 2 characters')
        elif not NAME_REGEX.match(postData['user_name']):
            errors.append('User name must only contain alphabet')

        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif postData['password'] != postData['confirm']:
            errors.append('Passwords do not match')
        if len(errors) == 0:
        #create the user
            newuser = User.objects.create(name= postData['name'], user_name= postData['user_name'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)

        return errors

    def login(self, postData):
        errors = []
        # if email is found in db
        if User.objects.filter(user_name=postData['user_name']):
            form_pw = postData['password'].encode()
            db_pw = User.objects.get(user_name=postData['user_name']).password.encode()
            user = User.objects.get(user_name = postData['user_name'])#
            return (True, user)

            if not bcrypt.checkpw(form_pw, db_pw):
                errors.append('Incorrect password')
        else:
            errors.append('Username has not been registered')
        return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.name + ' ' + self.user_name + ' - ' +  self.password

class travelManager(models.Manager):
    def travelPlan(self, postData, id):
        errors=[]
        if len(postData['destination']) < 1 :
            errors.append("Destination field can not be empty")
        if len(postData['description']) < 1 :
            errors.append("Description field can not be empty")

        if str(date.today()) > str(postData['start']):
            errors.append("Please input a valid Date. Note: Start time can not be in the past.")
        if str(date.today()) > postData['end']:
            errors.append("Please input a valid Date. Note: End date must be in the future")
        if postData['start'] > postData['end']:
            errors.append("Travel Date From can not be in the future of Travel Date To")
        if len(errors) == 0:
            plan= Travel.objects.create(destination=postData['destination'],description=postData['description'], start=postData['start'],end=postData['end'], creator= User.objects.get(id=id))
            print "Successfully created new plan:"
            return (True, plan)
        else:
            print "Cannot input into Data"
            return (False, errors)
        return errors

    def join(self, id, travel_id):
        if len(Travel.objects.filter(id=travel_id).filter(join__id=id))>0:
            return {'errors':'You have already Joined this'}
        else:
            joiner= User.objects.get(id=id)
            plan= self.get(id= travel_id)
            plan.join.add(joiner)
            return {}


class Travel(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    start= models.DateField()
    end= models.DateField()
    creator= models.ForeignKey(User, related_name= "planner")
    join= models.ManyToManyField(User, related_name="joiner") #holds on to instances of User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = travelManager()
