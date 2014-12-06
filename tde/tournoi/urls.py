from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.index_v, name='index'),
    url(r'^leaderboard$', views.leaderboard_v, name='leaderboard'),
    url(r'^login', views.login_v, name='login'),
    url(r'^logout', views.logout_v, name='logout'),
    url(r'^(?P<season>\d+)/(?P<week>\d+)$', views.fixture_v, name='fixture')
)
