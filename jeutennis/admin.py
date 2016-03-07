import django.contrib.auth

from django.contrib import admin
from django.contrib.auth.models import User

from .models import table_joueurs 

class ComptesJoueurs(admin.ModelAdmin):
	fieldsets = [
		("Vos informations : ",	{'fields':['prenom', 'nom', 'date_naissance']}),
	]
	list_display = ('prenom','nom','date_naissance')

# Register your models here.
admin.site.register(table_joueurs, ComptesJoueurs)
