from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.TextField()
    description = models.TextField()
    publish_datetime = models.DateTimeField()
    thumbnail_url = models.TextField()
