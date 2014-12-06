from django.contrib import admin

from tournoi.models import Bet, Fixture, Game, Club

# Register your models here.

for model in (Bet, Fixture, Game, Club):
    admin.site.register(model)
