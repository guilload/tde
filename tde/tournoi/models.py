# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Count, F


class Club(models.Model):
    name = models.CharField(max_length=64)
    shortname = models.CharField(max_length=64, unique=True)
    fullname = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Game(models.Model):
    fixture = models.ForeignKey('Fixture')
    home = models.ForeignKey('Club', related_name='home_fk')
    visitors = models.ForeignKey('Club', related_name='visitors_fk')
    date = models.DateTimeField()
    hscore = models.DecimalField(max_digits=2, decimal_places=0, default=-1)
    vscore = models.DecimalField(max_digits=2, decimal_places=0, default=-1)
    result = models.DecimalField(max_digits=1, decimal_places=0, default=-1)

    class Meta:
        unique_together = ('fixture', 'home', 'visitors')

    def __unicode__(self):
        return '{}: {} – {}'.format(self.fixture.week,
                                    self.home.name,
                                    self.visitors.name)

    @property
    def updated(self):
        return self.hscore != -1 and self.vscore != -1

    @property
    def started(self):
        return timezone.now() > self.date

    def save(self, *args, **kwargs):
        if self.updated:
            if self.hscore < self.vscore:
                self.result = 2
            elif self.hscore > self.vscore:
                self.result = 1
            else:
                self.result = 0

        super(Game, self).save(*args, **kwargs)


class Fixture(models.Model):
    season = models.DecimalField(max_digits=4, decimal_places=0)
    week = models.DecimalField(max_digits=2, decimal_places=0)

    class Meta:
        unique_together = ('season', 'week')

    def __unicode__(self):
        if self.week == 1:
            ordinal = '1ère'
        else:
            ordinal = '{}ème'.format(self.week)

        return '{} journée'.format(ordinal)

    @classmethod
    def current(cls):
        pass

    @property
    def prev(self):
        return self.week - 1

    @property
    def next(self):
        return self.week + 1

    def leaderboard(self):
        return Bet.objects.filter(result__gt=-1, fixture=self, game__result=F('result')).values('user__username').annotate(score=Count('user')).order_by('score')


class Bet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    fixture = models.ForeignKey('Fixture')
    game = models.ForeignKey('Game')
    result = models.DecimalField(max_digits=1, decimal_places=0, default=-1)
    placed_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fixture', 'game')

    @classmethod
    def leaderboard(cls):
        return cls.objects.filter(result__gt=-1, game__result=F('result')).values('user__username').annotate(score=Count('user')).order_by('score')

    @classmethod
    def populate(cls, fixture, user):
        bets = cls.objects.filter(fixture=fixture, user=user)

        if not bets:
            bets = []
            games = Game.objects.filter(fixture=fixture)

            for game in games:
                bet = Bet(fixture=fixture, user=user, game=game)
                bet.save()
                bets.append(bet)

        return bets

    @classmethod
    def update(cls, data):
        for key, result in data.items():
            if key.startswith('bet_'):
                bet = cls.objects.get(pk=int(key[4:]))

                if not bet.game.started:
                    bet.result = result
                    bet.save()
