from django.conf.urls import include, url
from django.contrib import admin, auth
from django.contrib.auth import *

from . import views
from models import table_joueurs

urlpatterns = [
        url(r'^$', views.index, name='index'),
	url(r'^detail/$', views.detail, name='detail'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^training/$', views.training, name='training'),
        url(r'^results/$', views.results, name='results'),
        url(r'^versus/$', views.versus, name='versus'),
        url(r'^match/$', views.match, name='match'),
#	url(r'^match/(?P<match_id>[0-9]+)/$', views.resmatch, name='resmatch'),
	url(r'^register/$', views.register, name='register'),
	url(r'^register_success/$', views.register_success, name='register_success'),
	url(r'^charts/$', views.charts, name='charts'),
	url(r'^calendar/$', views.calendar, name='calendar'),
	url(r'^tournois/$', views.tournois, name='tournois'),
	url(r'^tournois/(?P<idtournoi>[0-9]+)/$', views.eventtournoi, name='eventtournoi'),
	url(r'^mp/$', views.mp, name='mp'),
	url(r'^mp/newmp/$', views.newmp, name='newmp'),
        url(r'^mp/mp_success/$', views.mp_success, name='mp_success'),
        url(r'^mp/(?P<idmp>[0-9]+)-(?P<sujetmp>[\w-]+)/$', views.viewmp, name='viewmp'),
	url(r'^banque/$', views.banque, name='banque'),
	url(r'^myplayer/$', views.myplayer, name='myplayer'),
	url(r'^inventaire/$', views.inventaire, name='inventaire'),
]

