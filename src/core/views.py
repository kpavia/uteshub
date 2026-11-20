from datetime import timedelta
from types import SimpleNamespace

from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from football.models import (
    Game, MOUNTAIN, Ranking, Season
)
from video.models import CHANNEL_NAMES, Video


# Football is the only sport with data for now. The header nav and hero
# expect "sport" objects with a name, an in_season flag and a URL.
FOOTBALL = SimpleNamespace(name='Football', in_season=True, get_absolute_url='/')

LOCAL_HOSTS = ['localhost', 'localhost:8000', '127.0.0.1', '127.0.0.1:8000']


def _record(games):
    """Overall and conference records as 'W-L' strings. Ties are skipped."""
    wins = losses = conf_wins = conf_losses = 0
    for game in games:
        if game.result == 'W':
            wins += 1
            conf_wins += game.is_conference_game
        elif game.result == 'L':
            losses += 1
            conf_losses += game.is_conference_game
    return {
        'overall': f'{wins}-{losses}',
        'conference': f'{conf_wins}-{conf_losses}',
        'conference_name': 'Big 12',
    }


def _rankings(season):
    """Latest AP and CFP ranking for the season, each as {label, rank, week}."""
    rankings = []
    for key, label in Ranking.RANKING_CHOICES.items():
        latest = Ranking.objects.filter(season=season, ap_or_cfp=key).order_by('-id').first()
        if latest:
            rankings.append({'label': label, 'rank': latest.rank, 'week': latest.week})
    return rankings


# Channels shown first, in this order. The grid shows two videos per row, so
# the first pair is row 1 and the second pair is row 2.
PINNED_CHANNELS = [
    'u_of_u_athletics', 'game_highlights',   # row 1
    'locked_on_utes', 'utah_blockcast',      # row 2
]


# Unpinned channels are hidden when their newest video is older than this.
VIDEO_MAX_AGE = timedelta(days=30)


def _latest_videos():
    """Newest video from each known channel: pinned channels first, then the rest newest first.

    Unpinned channels with no video in the last VIDEO_MAX_AGE are left out.
    Pinned channels always show their newest video, however old.
    """
    cutoff = timezone.now() - VIDEO_MAX_AGE
    videos = []
    for channel in CHANNEL_NAMES:
        channel_videos = Video.objects.filter(channel=channel)
        if channel not in PINNED_CHANNELS:
            channel_videos = channel_videos.filter(air_date__gte=cutoff)
        videos.append(channel_videos.order_by('-air_date').first())
    videos = [v for v in videos if v]
    pinned = sorted(
        (v for v in videos if v.channel in PINNED_CHANNELS),
        key=lambda v: PINNED_CHANNELS.index(v.channel),
    )
    others = sorted(
        (v for v in videos if v.channel not in PINNED_CHANNELS),
        key=lambda v: v.air_date, reverse=True,
    )
    return pinned + others


def index(request):
    current_season = settings.CURRENT_SEASON

    season = Season.objects.filter(year=current_season).first()
    schedule = list(
        Game.objects.filter(season=season).select_related('opponent').order_by('date')
    )

    today = timezone.now().astimezone(MOUNTAIN).date()
    played = [game for game in schedule if game.result]
    upcoming = [game for game in schedule if not game.result and game.date >= today]

    context = {
        'season': season.year if season else current_season,
        'schedule': schedule,
        'next_game': upcoming[0] if upcoming else None,
        'last_game': played[-1] if played else None,
        'record': _record(schedule) if played else None,
        'rankings': _rankings(season) if season else [],
        'videos': _latest_videos(),
        'featured_sport': FOOTBALL,
        'current_sport': FOOTBALL,
        'sports': [FOOTBALL],
        'display_ga': request.headers.get('Host') not in LOCAL_HOSTS,
    }

    return render(request, 'uteshub/home.html', context)
