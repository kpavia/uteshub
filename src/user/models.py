from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    email = models.EmailField()
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='User email unique constraint'
            ),
            models.UniqueConstraint(
                fields=['username'],
                name='User username unique constraint'
            )
        ]

    def __str__(self):
        return f'User: {self.email}'
