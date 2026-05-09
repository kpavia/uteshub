from django.db import models
from datetime import datetime


class Season(models.Model):
    wins = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    year = models.CharField(max_length=4, null=True)
    final_ap_ranking = models.IntegerField(null=True)
    final_cfp_ranking = models.IntegerField(null=True)
    season_meta = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.year} season'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year'], name='Year unique constraint')
        ]


class Game(models.Model):
    date = models.DateField()
    opponent = models.ForeignKey('Team', on_delete=models.DO_NOTHING, null=True, blank=True)
    points_for = models.IntegerField(null=True, blank=True)
    points_against = models.IntegerField(null=True, blank=True)
    is_home_game = models.BooleanField(default=True)
    is_bowl_game = models.BooleanField(default=False)
    bowl_game = models.CharField(max_length=64, null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    opponent_icon = models.ForeignKey('Icon', on_delete=models.CASCADE, null=True, blank=True)
    network = models.CharField(max_length=16, null=True, blank=True)
    start_time = models.CharField(max_length=15, null=True, blank=True)
    is_conference_game = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return f'{self.date} - Utah vs {self.opponent.name}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'opponent', 'season'], name='Date, season and Opponent unique constraint')
        ]


class Ranking(models.Model):
    RANKING_CHOICES = {
        'ap': 'AP',
        'cfp': 'CFP'
    }
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    week = models.IntegerField()
    rank = models.CharField(max_length=2, null=True)
    ap_or_cfp = models.CharField(max_length=3, choices=RANKING_CHOICES)

    def __str__(self):
        return f'Utah {self.ap_or_cfp.upper()} rank, week {self.week}, #{self.rank}'


class Video(models.Model):
    link = models.CharField(max_length=100)
    channel = models.CharField(max_length=64, null=True)
    air_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.channel}, {self.air_date}'


class Icon(models.Model):
    name = models.CharField(max_length=32)
    icon_link = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} icon'


class Team(models.Model):
    name = models.CharField(max_length=64)
    logo = models.URLField(max_length=120, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'
