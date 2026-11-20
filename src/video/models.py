from django.db import models
from datetime import datetime


# Display names for the channel slugs saved by football/tasks.py.
CHANNEL_NAMES = {
    'locked_on_utes': 'Locked On Utes',
    'utes_digest': 'Utah Utes Football Digest',
    'utah_football_fans': 'Utah Football Fans',
    'rising_report': 'Rising Report',
    'game_highlights': 'Game Highlights',
    'u_of_u_athletics': 'Utah Athletics',
    'utah_blockcast': 'Utah Blockcast',
}


# Create your models here.
class Video(models.Model):
    link = models.CharField(max_length=100)
    channel = models.CharField(max_length=64, null=True)
    air_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.channel}, {self.air_date}'

    # Read-only helpers for the uteshub templates (no migration needed).

    @property
    def youtube_id(self):
        """ID from an embed link like https://www.youtube.com/embed/<id>?si=..."""
        return self.link.split('?')[0].rstrip('/').rsplit('/', 1)[-1]

    @property
    def source(self):
        return CHANNEL_NAMES.get(self.channel, self.channel or '')

    @property
    def published(self):
        return self.air_date
