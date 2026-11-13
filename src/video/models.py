from django.db import models
from datetime import datetime


# Create your models here.
class Video(models.Model):
    link = models.CharField(max_length=100)
    channel = models.CharField(max_length=64, null=True)
    air_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.channel}, {self.air_date}'
