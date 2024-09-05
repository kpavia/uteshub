from django.contrib import admin
from football.models import (
    Season, Game, Ranking, Video,
    Icon
)


admin.site.register(Season)
admin.site.register(Game)
admin.site.register(Ranking)
admin.site.register(Video)
admin.site.register(Icon)
