from django.db import models


# Create your models here.
class Account(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    plan_id = models.IntegerField(max_length=2)
    gender = models.CharField(max_length=30)
    family_name = models.CharField(max_length=100)
    given_name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    mail_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
