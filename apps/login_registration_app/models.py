from django.db import models
import re
from datetime import datetime, timedelta

class UserManager(models.Manager):
    def basic_validator(self,data):
        errors={}
        if len(data['email'])<=0:
            errors['email']='Input Email'
        if len(data['password'])<=0:
            errors['password']='Input Password'
        if len(data['password'])>=10:
            errors['password']='Password must be under 10 characters'
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            errors['email']='Invalid email-address'
        if len(User.objects.filter(email=data['email']))!=0:
            errors['email']='email is already in use'
        if data['password'] != data['comfirm_password']:
            errors['password']='passwords do not match'
        return errors

class User(models.Model):
    email=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class TripManager(models.Manager):
    def basic_validator(self,data):
        now=datetime.now()
        errors={}
        if len(data['destination'])<=3:
            errors['destination']='Destination must by at least 3 characters'
        if len(data['plan'])<=0:
            errors['plan']='Input Plan'
        if datetime.strptime(data['start_date'], '%Y-%m-%d')<now:
            errors['start_date']='Start date must be in the future'
        if datetime.strptime(data['end_date'], '%Y-%m-%d')<datetime.strptime(data['start_date'], '%Y-%m-%d'):
            errors['end_date']='End date must be later then start date'
        return errors

class Trip(models.Model):
    destination=models.CharField(max_length=50)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    plan=models.CharField(max_length=200)
    users=models.ManyToManyField(User, related_name='trips')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    creator=models.ForeignKey(User, related_name='creator')
    objects=TripManager()


