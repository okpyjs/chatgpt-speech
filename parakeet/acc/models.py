from django.db import models
from plan.models import Plan


# Create your models here.
class Account(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    plan_id = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=30)
    family_name = models.CharField(max_length=100)
    given_name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    mail_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)

    class Meta:
        verbose_name = "User Account"

    def __str__(self):
        return self.user_name
