from django.contrib import admin
from video.models import (Channel, Video)

# Register your models here.
admin.site.register(Video)
admin.site.register(Channel)