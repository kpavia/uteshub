from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=64)
    logo = models.URLField(max_length=120, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class Icon(models.Model):
    name = models.CharField(max_length=32)
    icon_link = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} icon'
