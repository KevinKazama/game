from django.db import models
import datetime

from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class table_joueurs(models.Model):
	prenom = models.CharField(max_length=20)
	nom = models.CharField(max_length=20)
	date_naissance = models.DateField('naissance')
	service = models.IntegerField(default=0)
	retour = models.IntegerField(default=0)
	concentration = models.IntegerField(default=0)
	endurance = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	victoire = models.IntegerField(default=0)
	defaite = models.IntegerField(default=0)
	def __str__(Prenom):
		return Prenom.prenom+" "+Prenom.nom
        date_train = models.DateField('train')
	date_match = models.DateTimeField('match')
        adversaire = models.IntegerField()
	user = models.ForeignKey(User)
	idtournoi = models.IntegerField(default=0)
	argent = models.IntegerField(default=1000)
	coffre = models.IntegerField(default=0)
	vie = models.IntegerField(default=10)
	date_vie = models.DateTimeField('dvie')
	is_equip = models.IntegerField(default=0)

class table_tournoi(models.Model):
        nom = models.CharField(max_length=20)
        participants = models.IntegerField(default=16)
        date_tournoi = models.DateTimeField()
        wintour = models.ForeignKey(table_joueurs, related_name="win_j1")
        tirage = models.IntegerField(default=0)


class table_match(models.Model):
        j1 = models.ForeignKey(table_joueurs, related_name="table_j1")
        j2 = models.ForeignKey(table_joueurs, related_name="table_j2")
        s1j1 = models.IntegerField(default=0)
        s2j1 = models.IntegerField(default=0)
        s3j1 = models.IntegerField(default=0)
        s4j1 = models.IntegerField(default=0)
        s5j1 = models.IntegerField(default=0)
        s1j2 = models.IntegerField(default=0)
        s2j2 = models.IntegerField(default=0)
        s3j2 = models.IntegerField(default=0)
        s4j2 = models.IntegerField(default=0)
        s5j2 = models.IntegerField(default=0)
        date_match = models.DateTimeField('match')
	winner = models.IntegerField()
	idtournoi = models.ForeignKey(table_tournoi, blank=True)

class message(models.Model):
        emetteur = models.ForeignKey(table_joueurs, related_name="emetteur")
        dest = models.ForeignKey(table_joueurs, related_name="dest")
	sujet = models.CharField(max_length=25)
	contenu = models.TextField()
	status = models.IntegerField(default=0)
	date_mp = models.DateTimeField('mp')
	crypt = models.CharField(max_length=6)

class table_equipement(models.Model):
	type_equip = models.CharField(max_length=20)
	durabilite = models.IntegerField(default=50)
	ptsservice = models.IntegerField(default=0)
	ptsretour = models.IntegerField(default=0)
	ptsconcentration = models.IntegerField(default=0)
	ptsendurance = models.IntegerField(default=0)
	prix = models.IntegerField(default=0)
	proprio = models.ForeignKey(table_joueurs)

class staff(models.Model):
        prenom = models.CharField(max_length=20)
        nom = models.CharField(max_length=20)
	 
