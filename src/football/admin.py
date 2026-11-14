from django.contrib import admin
from football.models import (
    Season, Game, Ranking
)


admin.site.register(Season)
admin.site.register(Game)
admin.site.register(Ranking)