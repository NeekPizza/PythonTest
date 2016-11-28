from __future__ import unicode_literals
from django.contrib import messages
import bcrypt
from django.db import models
import re
import datetime

# Create your models here.

class UsersManager(models.Manager):

    def registration(self,form):
        ncheck = re.compile(r'[a-z A-Z]')
        echeck = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pwcheck = re.compile(r'.*\d.*[A-Z].*|.*[A-Z].*\d.*')
        hashed=bcrypt.hashpw(form['password'].encode('utf-8'),bcrypt.gensalt())
        errors=[]
        if len(form['first_name'])<2:
            errors.append('Name too short')
        if not ncheck.match(form['alias']):
            errors.append('Name invalid')
        if len(form['alias'])<1:
            errors.append('Last name too short')
        if not ncheck.match(form['alias']):
            errors.append('Alias Invalid')
        if not echeck.match(form['email']):
            errors.append('Invalid email')
        if not pwcheck.match(form['password']):
            errors.append('Invalid password')
        if not form['password'] == form['confirm_password']:
            errors.append('Passwords do not match')
        if len(form['password'])<8:
            errors.append('Password too short')
        if datetime.datetime.strptime(form['date'],'%Y-%m-%d')>datetime.datetime.today():
            errors.append('Invalid Date')
            return (False,errors)
        if len(errors)>0:
            return (False,errors)
        else:
            user=Users.objects.create(first_name=form['first_name'],alias=form['alias'],email=form['email'],password=hashed,birth=form['date'])
            print Users.objects.all()
            return (True,user)

    def login(self,form):
        errors=[]
        user=Users.objects.filter(email=form['email'])
        if not user:
            errors.append('Email does not match records')
        elif not bcrypt.hashpw(form['password'].encode('utf-8'),user[0].password.encode('utf-8'))==user[0].password:
            errors.append('Password does not match email')
        if len(errors)>0:
            return (False,errors)
        else:
            return (True,user)

    def add(self,form,id):
        errors=[]
        if len(form['author'])<4:
            errors.append('Quoted By field is too short')
        if len(form['message'])<11:
            errors.append('Message field is too short')
            return (False,errors)
        else:
            quote=Quotes.objects.create(author=form['author'],message=form['message'],creator=id)
            return(True,quote)

class Users(models.Model):
    first_name=models.CharField(max_length=21)
    alias=models.CharField(max_length=21)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    birth=models.DateField(auto_now=False, auto_now_add=False,null=True)
    objects=UsersManager()

class Quotes(models.Model):
    author=models.CharField(max_length=21)
    message=models.TextField()
    creator=models.ForeignKey(Users,related_name='creator')
    favorite=models.ManyToManyField(Users)
