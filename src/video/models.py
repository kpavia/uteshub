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


class Channel(models.Model):

    PLATFORMS = {
        'YT': 'YouTube'
    }
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    external_id = models.CharField(max_length=100, unique=True)
    platform = models.CharField(max_length=10, choices=PLATFORMS, default='YT')
    title_filter = models.CharField(max_length=100, default='', blank=True)
    priority = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Create your models here.
class Video(models.Model):
    link = models.CharField(max_length=100)
    channel = models.CharField(max_length=64, null=True, db_index=True)
    channel_fk = models.ForeignKey(Channel, on_delete=models.PROTECT, null=True)
    air_date = models.DateTimeField(default=datetime.now, db_index=True)

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
