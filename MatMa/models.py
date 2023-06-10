from django.db import models

# Create your models here.

class User1(models.Model):
    name = models.CharField(max_length=100)
    cardID = models.CharField(max_length=8)
    phone = models.IntegerField()

class Log(models.Model):
    cardID = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)