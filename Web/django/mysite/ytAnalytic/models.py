from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    vid_id = models.CharField(max_length=50)
    thumbnail = models.CharField(max_length=200)
    tags = models.CharField(max_length=500)