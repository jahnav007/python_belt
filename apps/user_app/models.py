# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import date
import re
import bcrypt

#had this page almost ready previously from the practice that i did from will's recorded video

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, conf_password, birthday):
        errors = []

        if len(first_name)<2 or len(last_name) <2:
            errors.append('Not less than 2 characters on name field')
        if not last_name.isalpha() or not first_name.isalpha():
            errors.append('Only letters are allowed in name field')

        if len(email) < 1:
            errors.append('email is required')
        elif not EMAIL_REGEX.match(email):
            errors.append('Invalid Email')
        else:
            user = User.userManager.filter(email=email.lower())
            if len(user) > 0:
                errors.append('Email already in use')

        if len(password) < 1:
            errors.append('Password is required')
        elif len(password) < 8:
            errors.append('Password must be 8 characters or more')

        if len(conf_password) < 1:
            errors.append('Confirm Password is required')
        elif password != conf_password:
            errors.append('Password and Confirm password must match')

        if len(birthday) < 1:
            errors.append('Please enter your birthday')

        if len(errors) > 0:
            return (False, errors)
        else:
            user= User.userManager.create(first_name=first_name, last_name=last_name, email=email.lower(), password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()), birthday=birthday)
            return (True, user)

    def login(self, email, password):
        errors = []

        if len(email) < 1:
            errors.append('email is required')
        elif not EMAIL_REGEX.match(email):
            errors.append('Invalid Email')
        else:
            user = User.userManager.filter(email=email.lower())
            if len(user) == 0:
                errors.append('Email not found')

        if len(password) < 1:
            errors.append('Password is required')
        elif len(password) < 8:
            errors.append('Password must be 8 characters or more')

        if len(errors) > 0:
            return (False, errors)
        else:
            if bcrypt.checkpw(password.encode(), user[0].password.encode()):
                return (True, user[0])
            else:
                return (False, ['Incorrect Password'])



class User(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    birthday= models.DateField()
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    userManager= UserManager()

    def __repr__(self):
        return "<User: {} {}>".format(self.first_name, self.email)
