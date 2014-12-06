from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from tournoi.models import Bet, Fixture, Game


@login_required
def index_v(request):
    fixture = Game.objects.filter(date__gte=timezone.now()).first().fixture
    return redirect('fixture', season=fixture.season, week=fixture.week)


@login_required
def leaderboard_v(request):
    fixture = Game.objects.filter(date__gte=timezone.now()).first().fixture
    leaderboard = Bet.leaderboard()
    context = {'fixture': fixture, 'leaderboard': leaderboard}
    return render(request, 'leaderboard.html', context)

def login_v(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Invalid username and/or password!")


def logout_v(request):
    logout(request)
    return redirect('login')


@login_required
def fixture_v(request, season, week):
    fixture = Fixture.objects.get(season=season, week=week)
    username = request.GET.get('bettor', request.user.username)
    bettor = User.objects.get(username=username)

    if request.method == 'GET':
        bets = Bet.populate(fixture=fixture, user=bettor)
        users = User.objects.all()
        context = {'bets': bets, 'bettor': bettor, 'fixture': fixture, 'users': users}
        return render(request, 'fixture.html', context)

    elif request.method == 'POST':
        Bet.update(request.POST)
        return redirect('fixture', season=fixture.season, week=fixture.week)
