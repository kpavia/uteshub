from django.db import models
from django.utils.functional import cached_property
from datetime import datetime, time
from zoneinfo import ZoneInfo
from team.models import (Team, Icon)

MOUNTAIN = ZoneInfo('America/Denver')


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
    opponent = models.ForeignKey(Team, on_delete=models.DO_NOTHING, null=True, blank=True)
    points_for = models.IntegerField(null=True, blank=True)
    points_against = models.IntegerField(null=True, blank=True)
    is_home_game = models.BooleanField(default=True)
    is_bowl_game = models.BooleanField(default=False)
    bowl_game = models.CharField(max_length=64, null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    opponent_icon = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)
    network = models.CharField(max_length=16, null=True, blank=True)
    start_time = models.CharField(max_length=15, null=True, blank=True)
    is_conference_game = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return f'{self.date} - Utah vs {self.opponent.name}'

    # Read-only helpers for the uteshub templates. These are plain Python
    # properties, not database fields, so they need no migration.

    @property
    def is_home(self):
        return self.is_home_game

    @property
    def utah_score(self):
        return self.points_for

    @property
    def opponent_score(self):
        return self.points_against

    @property
    def result(self):
        """'W', 'L' or 'T' once both scores are in; None before the game."""
        if self.points_for is None or self.points_against is None:
            return None
        if self.points_for > self.points_against:
            return 'W'
        if self.points_for < self.points_against:
            return 'L'
        return 'T'

    @cached_property
    def _parsed_start_time(self):
        """start_time is free text like '7:00PM MST'; returns a time or None."""
        if not self.start_time:
            return None
        try:
            return datetime.strptime(self.start_time.split()[0].upper(), '%I:%M%p').time()
        except (ValueError, IndexError):
            return None

    @property
    def time_tba(self):
        return self._parsed_start_time is None

    @cached_property
    def kickoff(self):
        """Timezone-aware kickoff in Mountain time (midnight on the date if TBA).

        start_time says 'MST' year-round but means local Mountain time, so
        America/Denver handles the MDT/MST switch.
        """
        return datetime.combine(self.date, self._parsed_start_time or time.min, tzinfo=MOUNTAIN)

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
