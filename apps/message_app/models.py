# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from ..user_app.models import User
import re

class QuoteManager(models.Manager):
    def postquote(self, quoted_by, user, text ):
        message = []
        if len(quoted_by)<3:
            message.append('More than 3 characters needed in this field')

        if len(text)<10:
            message.append('More than 10 characters needed in this field')
        if len(message)>0:
            return False, message
        else:
            data= Quote.quoteManager.create(quoted_by=quoted_by, user_id=user, text= text)  # uers_id comes from the Secrets table it's actually user, but have to add _id. user comes from the parameter that came from the Users.secretsManager.postsecret
            return True, data

class FavManager(models.Manager):
    def fav(self, user, quoteID):
        x= Fav.favManager.filter(user_id=user,quote_id=quoteID)
        if len(x)>0:
            return (False, "You already added this on your favorite list")
        else:
            faved= Fav.favManager.create(user_id=user, quote_id=quoteID)
            return (True, faved)

    def delete(self, quoteID):
        Fav.favManager.filter(quote_id=quoteID).delete()
        return True



class Quote(models.Model):
    quoted_by= models.CharField(max_length=100)
    text= models.TextField()
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    quoteManager=QuoteManager()
    user=models.ForeignKey(User, related_name ="posted_user")


class Fav(models.Model):
    user= models.ForeignKey(User, related_name= "fav_user")
    quote=models.ForeignKey(Quote, related_name= "fav_quote")
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    favManager=FavManager()
