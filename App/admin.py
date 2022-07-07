from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(News)
admin.site.register(Follow)
admin.site.register(Turnament)
admin.site.register(WorldStatistic)
admin.site.register(RegisterTeam)
admin.site.register(Team)
admin.site.register(RoundEvent)
