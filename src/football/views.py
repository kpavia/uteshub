from django.shortcuts import render
from django.conf import settings
from football.models import (Season, Game, Ranking, Video)
from django.core.paginator import Paginator
from pprint import pprint


def index(request):
    current_season = settings.CURRENT_SEASON
    season = Season.objects.filter(year=current_season).first()
    schedule = Game.objects.filter(season=season).order_by('date')
    ap_rank = Ranking.objects.filter(ap_or_cfp='ap').latest('id')
    cfp_rank = Ranking.objects.filter(ap_or_cfp='cfp')
    ut_football_fans = Video.objects.filter(channel='utah_football_fans').latest('air_date')
    lou = Video.objects.filter(channel='locked_on_utes').latest('air_date')
    u_athletics = Video.objects.filter(channel='u_of_u_athletics').latest('air_date')
    game_highlights = Video.objects.filter(channel='game_highlights').latest('air_date')
    rising_report = Video.objects.filter(channel='rising_report').latest('air_date')
    wins = 0
    losses = 0
    for game in schedule:
        if game.opponent_icon:
            print(game.opponent_icon)
        if game.points_for:
            if game.points_for > game.points_against:
                wins += 1
            elif game.points_for == game.points_against:
                continue
            else:
                losses += 1
    season_record = {
        'wins': wins,
        'losses': losses
    }

    if cfp_rank:
        cfp_rank = cfp_rank.latest('id')
    

    if request.headers.get('Host') in ['localhost', 'localhost:8000', '127.0.0.1', '127.0.0.1:8000']:
        display_ga = False
    else:
        display_ga = True
    
    context = {
        'schedule': [game for game in schedule],
        'ap_rank': ap_rank,
        'cfp_rank': cfp_rank.latest('id') if cfp_rank else None,
        'season': season,
        'utff': ut_football_fans,
        'lou': lou,
        'u_of_u_athletics': u_athletics,
        'record': season_record,
        'game_highlights': game_highlights,
        'rr': rising_report,
        'display_ga': display_ga
    }
    return render(request, 'football/index.html', context)
