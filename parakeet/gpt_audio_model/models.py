from django.db import models


# Create your models here.
class GPT(models.Model):
    model_name = models.CharField(max_length=30)
    model_description = models.TextField()


class Audio(models.Model):
    model_name = models.CharField(max_length=30)
    model_description = models.TextField()
