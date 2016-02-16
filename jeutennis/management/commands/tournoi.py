from django.core.management.base import BaseCommand, CommandError
from jeutennis.models import table_joueurs, table_match, table_tournoi
from django.utils import timezone
import datetime
from datetime import date, timedelta
import random
import time
from collections import OrderedDict
from django.db.models import Q

list_tournoi = []
id_tournoi = []
list_part = []
domicile = []
exterieur = []
date_time = datetime.datetime.now()
dmin = date_time - timedelta(days=1)
dmax = date_time - timedelta(days=6)


class Command(BaseCommand):
    help = 'Gestion tournoi'

    def handle(self, *args, **options):
        if len(args) == 0:
            print 'no args'


    try:
        req_part = table_tournoi.objects.filter(date_tournoi__lte=dmin, date_tournoi__gte=dmax)
        #print("tournoi "+req_part.nom)
        for s in req_part:
            print(s.nom,s.date_tournoi)
	    list_tournoi.append(s.nom)
            id_tournoi.append(s.id)   
	             
            fichier = open("/kevin/python/Projets/tennis/jeu/jeutennis/tournois/"+str(s.nom)+".txt","r")
            line = fichier.read().splitlines()
	    fichier.close()
	    if len(line) < 2:
		s.winner = line[0]
		s.save()
		print(line[0])
	    else:
	        fichier = open("/kevin/python/Projets/tennis/jeu/jeutennis/tournois/"+str(s.nom)+".txt","w")
	        #print(line)
                for x in line:
	            #print(x)
	            list_part.append(x)
            i = 0
            while i < len(list_part):
	        if i % 2 == 0:
	            domicile.append(list_part[i])
	        else:
	            exterieur.append(list_part[i])
	        i += 1
            j = 0
	    #print(domicile)
            while j < len(exterieur):
	        #print(str(domicile[j])+' vs '+str(exterieur[j]))
                joueur1 = table_joueurs.objects.get(id = domicile[j])
                joueur2 = table_joueurs.objects.get(id = exterieur[j])
                j1 = str(joueur1.prenom+" "+joueur1.nom)
                j2 = str(joueur2.prenom+" "+joueur2.nom)
                #print(j1+" vs "+j2)
	    	#Jeux
            	nb1 = 0
            	nb2 = 0

            	#Sets
            	sets = 0
            	set1 = 0
            	set2 = 0
            	sj1 = []
            	sj2 = []
            	s1j1 = []
            	s2j1 = []
            	s3j1 = []
            	s4j1 = []
            	s5j1 = []
            	s1j2 = []
            	s2j2 = []
            	s3j2 = []
            	s4j2 = []
            	s5j2 = []


            	#Scores
            	res1 = []
            	res2 = []

            	#Tour de jeu
            	tour = 0

            	#Caracteristiques
            	serv1 = joueur1.service
            	serv2 = joueur2.service
            	ret1 = joueur1.retour
            	ret2 = joueur2.retour
            	end1 = joueur1.endurance
            	end2 = joueur2.endurance
            	con1 = joueur1.concentration
            	con2 = joueur2.concentration
            	diff = 0
            	comm = []
            	message = []
            	nbtour = []
            	comptset = 0


            	while (set1 < 3) and (set2 < 3):
                    nb1 = 0
                    nb2 = 0
	    
                    #Boucle sets
                    while (nb1 < 6) and (nb2 < 6):
                        tour += 1
	                #print(tour)
                        nbtour.append(tour)
                        if tour % 2 == 0:
                            diff = serv1 - ret2
                        else:
                            diff = ret1 - serv2
                        alea = int(random.randrange(0,100))
                        if alea < 50+diff:
                            nb1 += 1
                        else:
                            nb2 += 1
                        #Baisse des stats endurance
                        if serv1 < 1:
                            serv1 = 0
                        else:
                            serv1 = serv1 - end2/100
                        if ret1 < 1:
                            ret1 = 0
                        else:
                            ret1 = ret1 - end2/100
                        if con1:
                            con1 = 0
                        else:
                            con1 = con1 - end2/100
                        if serv2 < 1:
                            serv2 = 0
                        else:
                            serv2 = serv2 - end1/100
                        if ret2 < 1:
                            ret2 = 0
                        else:
                            ret2 = ret2 - end1/100
                        if con2 < 1:
                            con2 = 0
                    	else:
                            con2 = con2 - end1/100
                    	sj1.append(str(nb1))
                    	sj2.append(str(nb2))
                    #Tie-Break
                    if nb1 + nb2 == 11:
                    	while ((nb1 < 7) and (nb2 < 7)) and (abs(nb1-nb2) != 2):
                            tour += 1
                            nbtour.append(tour)
                            if tour % 2 == 0:
                                diff = serv1 + con1 - ret2 - con2
                            else:
                                diff = ret1 + con1 - ret2 - con2
                            alea = int(random.randrange(100))
                            if alea < 50+diff:
                                nb1 += 1
                            else:
                                nb2 += 1
                            #Baisse stats
                            if serv1 < 1:
                                serv1 = 0
                            else:
                                serv1 = serv1 - end2/100
                            if ret1 < 1:
                                ret1 = 0
                            else:
                                ret1 = ret1 - end2/100
                            if con1 < 1:
                                con1 = 0
                            else:
                                con1 = con1 - end2/100
                            if serv2 < 1:
                                serv2 = 0
                            else:
                                serv2 = serv2 - end1/100
                            if ret2 < 1:
                                ret2 = 0
                            else:
                                ret2 = ret2 - end1/100
                            if con2 < 1:
                                con2 = 0
                            else:
                                con2 = con2 - end1/100
                            rendu = j1+" : "+str(nb1)+" | "+j2+" : "+str(nb2)
                            sj1.append(str(nb1))
                            sj2.append(str(nb2))

                            comm.append(rendu)

#Ajout scores
                    comm.append("")
                    res1.append(nb1)
                    res2.append(nb2)
                    #Nb sets
                    sets += 1

                    #Add game number in set list
                    if sets == 1:
                        for x in sj1:
                            s1j1.append(x)
                    	for x in sj2:
                            s1j2.append(x)
                    elif sets == 2:
                    	for x in sj1:
                            s2j1.append(x)
                    	for x in sj2:
                            s2j2.append(x)
                    elif sets == 3:
                    	for x in sj1:
                            s3j1.append(x)
                    	for x in sj2:
                            s3j2.append(x)
                    elif sets == 4:
                    	for x in sj1:
                            s4j1.append(x)
                    	for x in sj2:
                            s4j2.append(x)
                    elif sets == 5:
                    	for x in sj1:
                            s5j1.append(x)
                    	for x in sj2:
                            s5j2.append(x)

                    while comptset < len(sj1):
                    	sj1[comptset] = "."
                    	comptset += 1

                    comptset = 0
                    while comptset < len(sj2):
                    	sj2[comptset] = "."
                    	comptset += 1

                    comptset = 0
                    if nb1 > nb2:
                    	set1 += 1
			#print(j1+" gagne le set "+str(set1+set2)+" : "+str(nb1)+"/"+str(nb2))
                    	mess = j1+" gagne le set "+str(set1+set2)+" : "+str(nb1)+"/"+str(nb2)
                    	comm.append(mess)
                    else:
                    	set2 += 1
			#print(j2+" gagne le set "+str(set1+set2)+" : "+str(nb2)+"/"+str(nb1))
                    	mess = j2+" gagne le set "+str(set1+set2)+" : "+str(nb2)+"/"+str(nb1)
                    	comm.append(mess)
	        nset = len(res1)
	        #print('nset = '+str(nset))
	        i = 0
	        win = []
	        win2 = []
	        while i < nset:
                    win.append(str(res1[i])+"/"+str(res2[i]))
                    win2.append(str(res2[i])+"/"+str(res1[i]))
                    i += 1

	        strwin = ' - '.join(win)
	        strwin2 = ' - '.join(win2)
	        if set1 > set2:
		    fichier.write(str(joueur1.id)+"\n")
                    context2 = j1+" gagne "+strwin+" !"
                    joueur1.victoire += 1
                    joueur2.defaite += 1
                    joueur1.points += 60
                    joueur2.points -= 50
                    winner = 1
	        else:
		    fichier.write(str(joueur2.id)+"\n")
                    context2 = j2+" gagne "+strwin2+" !"
                    joueur1.defaite += 1
                    joueur2.victoire += 1
                    joueur1.points -= 60
                    joueur2.points += 50
                    winner = 2
                joueur1.save()
                joueur2.save()
                res = []
                tour = len(nbtour) + 1
                score = len(nbtour) + 2

            	g1j1 = res1[0]
            	g2j1 = res1[1]
            	g3j1 = res1[2]
            	try:
                    g4j1 = res1[3]
            	except IndexError:
                    g4j1 = None
            	try:
                    g5j1 = res1[4]
            	except IndexError:
                    g5j1 = None

            	g1j2 = res2[0]
            	g2j2 = res2[1]
            	g3j2 = res2[2]
            	try:
                    g4j2 = res2[3]
            	except IndexError:
                    g4j2 = None
            	try:
                    g5j2 = res2[4]
            	except IndexError:
                    g5j2 = None
		
		if g4j1 == None:
		    print(j1+" vs "+j2+" : "+str(g1j1)+"/"+str(g1j2)+" - "+str(g2j1)+"/"+str(g2j2)+" - "+str(g3j1)+"/"+str(g3j2))
		elif g5j1 == None:
		    print(j1+" vs "+j2+" : "+str(g1j1)+"/"+str(g1j2)+" - "+str(g2j1)+"/"+str(g2j2)+" - "+str(g3j1)+"/"+str(g3j2)+" - "+str(g4j1)+"/"+str(g4j2))
		else:
		    print(j1+" vs "+j2+" : "+str(g1j1)+"/"+str(g1j2)+" - "+str(g2j1)+"/"+str(g2j2)+" - "+str(g3j1)+"/"+str(g3j2)+" - "+str(g4j1)+"/"+str(g4j2)+" - "+str(g5j1)+"/"+str(g5j2))
                
		add = table_match.objects.create(s1j1 = g1j1, s2j1 = g2j1, s3j1 = g3j1, s4j1 = g4j1, s5j1 = g5j1, s1j2 = g1j2, s2j2 = g2j2, s3j2 = g3j2, s4j2 = g4j2, s5j2 = g5j2, date_match = date_time, j1_id = joueur1.id, j2_id = joueur2.id, winner = winner, idtournoi_id = s.id)
                add.save()
	        #Incremente j
	        j += 1

            fichier.close()
            fichier = open("/kevin/python/Projets/tennis/jeu/jeutennis/tournois/"+str(s.nom)+".txt","r")
            line = fichier.read().splitlines()
            fichier.close()
	    if len(line) < 2:
                s.winner = line[0]
                s.save()


	    #Reset lists
	    line = []
	    list_part = []
	    domicile = []
	    exterieur = []          
		
    except:
        print("Pas de tournoi")


#    def handle_noargs(self, **options):
#        raise NotImplementedError('subclasses of NoArgsCommand must provide a handle_noargs() method')
#    def handle_base(self, **options):
#        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
