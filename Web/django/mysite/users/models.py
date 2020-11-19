from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Channel(models.Model):
    user = models.CharField(max_length=200)
    channel_id = models.CharField(max_length=200)