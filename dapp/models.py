from django.db import models

# Create your models here.


class Accounts(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    # score = models.IntegerField


class Missions (models.Model):
    id = models.IntegerField(primary_key=True)
    ownerid = models.IntegerField(default = 0)
    type = models.CharField(max_length=20,default='default')
    name = models.CharField(max_length=40,default='default')
    score = models.IntegerField(default = 0)
    period = models.IntegerField(default = 0)


class Sessions (models.Model):
    userid = models.IntegerField(default = 0)
    cookie = models.CharField(unique=True,max_length=129)

