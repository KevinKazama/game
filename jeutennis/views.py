# -*- coding: utf-8 -*-
import warnings
from django.utils import timezone
import datetime
from datetime import date, timedelta
import random
import math
import time
import MySQLdb
import string
from .forms import UserReg, MPReg
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.shortcuts import resolve_url, render, render_to_response
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango110Warning
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import table_joueurs, table_match, table_tournoi, message, table_equipement, table_level
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.db.models import Q, Count
from collections import OrderedDict

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='jeutennis/connexion.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            #if not is_safe_url(url=redirect_to, host=request.get_host()):
               #redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
	    
            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())
            username = form.cleaned_data['username']
	    u = User.objects.get(username=request.user.username)
	    m = table_joueurs.objects.get(user_id=u.id)
	    test = m.prenom
	    niveau = m.niveau_id
	    	    
	    context = RequestContext(request, {
	        'test' : test,
	        'niveau' : niveau,
	        'm' : m,
	    }) 
            return HttpResponseRedirect(redirect_to)
	    #return render(request, 'jeutennis/connexion.html', context)
    else:
        form = authentication_form(request)
    current_site = get_current_site(request)

    try:
	user = User.objects.get(username=request.user.username)
        joueur = table_joueurs.objects.get(user_id = user.id)
        niveau = joueur.niveau_id
        energie = joueur.vie
        pts = joueur.points
        tableau = table_joueurs.objects.filter().exclude(points__lte = pts).annotate(total=Count('points'))
        classement = len(tableau) + 1
        argent = joueur.argent

        context = RequestContext(request, {
                'niveau' : niveau,
                'energie' : energie,
                'classement' : classement,
                'argent' : argent,
            })
        return render(request, 'jeutennis/connexion.html', context)
    except:

        context = {
            'form': form,
            redirect_field_name: redirect_to,
            'site': current_site,
            'site_name': current_site.name,
        }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def logout(request, next_page=None,
           template_name='jeutennis/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
            redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out')
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def logout_then_login(request, login_url=None, current_app=None, extra_context=None):
    """
    Logs out the user if they are logged in. Then redirects to the log-in page.
    """
    if not login_url:
        login_url = settings.LOGIN_URL
    login_url = resolve_url(login_url)
    return logout(request, login_url, current_app=current_app, extra_context=extra_context)


def redirect_to_login(next, login_url=None,
                      redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirects the user to the login page, passing the given 'next' page
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))


# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {
        'title': _('Password reset sent'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

@login_required
def detail(request):
    #template = loader.get_template('jeutennis/training.html')    
    #stats = table_joueurs.objects.order_by('id')
    #output = ', '.join([p.prenom for p in stats])
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id) 
    service = joueur.service
    retour = joueur.retour
    concentration = joueur.concentration
    endurance = joueur.endurance
    argent = joueur.argent
    date_train = joueur.date_train
    date_time = datetime.datetime.now()
    # Format date OK
    date_format = datetime.date(date_time.year,date_time.month,date_time.day)
    # Liste caracts
    output = []
    output.append(service)
    output.append(retour)
    output.append(concentration)
    output.append(endurance)
    # Liste nom stats
    stats = []
    stats.append("service")
    stats.append("retour")
    stats.append("concentration")
    stats.append("endurance")
    context_fail = RequestContext(request, {'message' : "Tu t\'es déja entrainé aujourd\'hui !"})
    context = RequestContext(request, {
        'output' : output,
        'stats' : stats,
        'error_message' : "Commencer l\'entrainement ?",
    })
    # Si clic sur Quotidien
    try:
        selected_choice = request.POST['Day']
        if selected_choice == "Day":
	    # Si deja entraine aujourd'hui
	    if date_format == date_train:
    		return render(request, 'jeutennis/detail.html', context_fail)
	    else:
		return render(request, 'jeutennis/detail.html', context)
    except:
	# Test POST caract choisie
	try:
            selected_choice = request.POST['training']
	    if selected_choice == "service":
                joueur.service += 1
                joueur.save()
            elif selected_choice == "retour":
                joueur.retour += 1
                joueur.save()
            elif selected_choice == "concentration":
                joueur.concentration += 1
                joueur.save()
            elif selected_choice == "endurance":
                joueur.endurance += 1
                joueur.save()
            # MaJ date train
            joueur.date_train = date_format
            joueur.save()
            return HttpResponseRedirect('/index/results/')
    	#except (KeyError, table_joueurs.DoesNotExist):
        #	    return render(request, 'jeutennis/detail.html', context)

        except:
	    # Clic sur C'est parti
	    try:
	        selected_choice = request.POST['Train']
	        if selected_choice == "Train":
		    return HttpResponseRedirect('/index/train_session/')
	
	    # Par défaut
	    except:
	        zipstat = zip(stats,output) 
                context2 = RequestContext(request, {
                    'zipstat' : zipstat,
                    'express_message' : "Commencer l\'entrainement ?",
	            'argent' : argent,
                })
	        return render(request, 'jeutennis/detail.html', context2)	


def training(request):
    return render(request, 'jeutennis/template.html')

@login_required
def results(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    service = joueur.service
    retour = joueur.retour
    concentration = joueur.concentration
    endurance = joueur.endurance
    context = RequestContext(request, 
		{'service' : service,
		 'retour' : retour,
		 'concentration' : concentration,
		 'endurance' : endurance,
		})

    return render(request, 'jeutennis/results.html', context)

@login_required
def versus(request):
    user = User.objects.get(username=request.user.username)
    mine = table_joueurs.objects.get(user_id = user.id)
    vie = mine.vie
    dvie = mine.date_vie
    d_format = datetime.datetime(dvie.year,dvie.month,dvie.day,dvie.hour,dvie.minute,dvie.second)
    dnow = datetime.datetime.now()
    if vie < 10:
	sec = dnow - d_format
	minute = sec.seconds // 60
	reste = sec.seconds % 60
	if minute > 0:
	    dnow -= timedelta(seconds=reste)
	    mine.date_vie = dnow
	vie += minute
	if vie > 10:
	    vie = 10
	mine.vie = vie
	mine.save()
	
    joueur = table_joueurs.objects.filter().exclude(user_id = user.id).order_by('?')[:5]
    list_joueurs = []
    for s in joueur:
        list_joueurs.append(s)
    context = RequestContext(request, {
		'vie' : vie,
		'list_joueurs' : list_joueurs})
    try:
	selected_choice = request.POST['match']
    except (KeyError, table_joueurs.DoesNotExist):
	return render(request, 'jeutennis/versus.html', context)
    else:
	id_joueur = int(selected_choice)
        me = table_joueurs.objects.get(user_id = user.id)
        me.adversaire = id_joueur
        me.save()    
	return HttpResponseRedirect('/index/match') 

@login_required
def match(request):
    user = User.objects.get(username=request.user.username)
    joueur1 = table_joueurs.objects.get(user_id = user.id) 
    adv = joueur1.adversaire
    datematch = joueur1.date_match
    d_format = datetime.datetime(datematch.year,datematch.month,datematch.day,datematch.hour,datematch.minute,datematch.second)
    #Attributs Equipements
    raq = joueur1.is_equip_id
    raquette = table_equipement.objects.get(id=raq)
    durabilite = raquette.durabilite
    if int(durabilite) == 0:
	raqservice = 0
	raqretour = 0
	raqconcentration = 0
	raqendurance = 0
    else:
	raqservice = raquette.ptsservice
	raqretour = raquette.ptsretour
	raqconcentration = raquette.ptsconcentration
	raqendurance = raquette.ptsendurance

    inv = table_equipement.objects.filter(proprio = joueur1.id).annotate(total=Count('id'))
    inventaire = len(inv)
    date_time = datetime.datetime.now()
    delta = date_time - d_format
    delta_s = delta.seconds
    joueur2 = table_joueurs.objects.get(id = adv)
    raq2 = joueur2.is_equip_id
    raquette2 = table_equipement.objects.get(id=raq2)
    durabilite2 = raquette2.durabilite
    if int(durabilite2) == 0:
        raqservice2 = 0
        raqretour2 = 0
        raqconcentration2 = 0
        raqendurance2 = 0
    else:
        raqservice2 = raquette2.ptsservice
        raqretour2 = raquette2.ptsretour
        raqconcentration2 = raquette2.ptsconcentration
        raqendurance2 = raquette2.ptsendurance



    j1 = str(joueur1.prenom+" "+joueur1.nom)
    j2 = str(joueur2.prenom+" "+joueur2.nom)
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
    serv1 = joueur1.service + raqservice
    serv2 = joueur2.service + raqservice2
    ret1 = joueur1.retour + raqretour
    ret2 = joueur2.retour + raqretour2
    end1 = joueur1.endurance + raqendurance
    end2 = joueur2.endurance + raqendurance2
    con1 = joueur1.concentration + raqconcentration
    con2 = joueur2.concentration + raqconcentration2
    arg1 = joueur1.argent 
    arg2 = joueur2.argent
    ptsj1 = joueur1.points
    ptsj2 = joueur2.points
    victj1 = joueur1.victoire
    victj2 = joueur2.victoire
    defj1 = joueur1.defaite
    defj2 = joueur2.defaite
    tableauj1 = table_joueurs.objects.filter().exclude(points__lte = ptsj1).annotate(total=Count('points'))
    classj1 = len(tableauj1) + 1
    tableauj2 = table_joueurs.objects.filter().exclude(points__lte = ptsj2).annotate(total=Count('points'))
    classj2 = len(tableauj2) + 1

    niv = joueur1.niveau_id


    diff = 0
    comm = []
    message = []
    nbtour = [] 
    comptset = 0   
    exp = joueur1.exp
    vie = joueur1.vie
    vie = int(vie)    
    looter = "Loot : Rien"
 
    if vie > 0:
	joueur1.vie -= 1
	joueur1.date_match = date_time
    	joueur1.save()
    	while (set1 < 3) and (set2 < 3):
	#	comm.append("")
		nb1 = 0
        	nb2 = 0

 	#Boucle sets
		while (nb1 < 6) and (nb2 < 6):
			tour += 1
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
			mess = j1+" gagne le set "+str(set1+set2)+" : "+str(nb1)+"/"+str(nb2)
			comm.append(mess)
		else:
			set2 += 1
			mess = j2+" gagne le set "+str(set1+set2)+" : "+str(nb2)+"/"+str(nb1)
			comm.append(mess)
	nset = len(res1)
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
		context2 = j1+" gagne "+strwin+" !"
		joueur1.argent += int(niv)*10+100
		joueur1.victoire += 1
		joueur2.defaite += 1
		joueur1.points += 60
		joueur2.points -= 50
		winner = 1
		if inventaire < 20:	
		    loot = int(random.randrange(0,100))
		else:
		    loot = 0
		if loot == 100:
			looter = "Loot legendaire"
			objet = table_equipement.objects.create(type_equip = "raquette", durabilite = 50, ptsservice = 50, ptsretour = 50, ptsconcentration = 50, ptsendurance = 50, prix = 500, nom = "Test", proprio = joueur1.id, nivreq_id = 10)
        		objet.save()
		elif loot >= 95:
			looter = "Loot epique"
			objet = table_equipement.objects.create(type_equip = "raquette", durabilite = 30, ptsservice = 30, ptsretour = 30, ptsconcentration = 30, ptsendurance = 30, prix = 300, nom = "Test", proprio = joueur1.id, nivreq_id = 5)
                        objet.save()
		elif loot >= 80:
			looter = "Loot rare"
                        objet = table_equipement.objects.create(type_equip = "raquette", durabilite = 20, ptsservice = 20, ptsretour = 20, ptsconcentration = 20, ptsendurance = 20, prix = 200, nom = "Test", proprio = joueur1.id, nivreq_id = 3)
                        objet.save()
		elif loot >= 50:
			looter = "Loot commun"
			objet = table_equipement.objects.create(type_equip = "raquette", durabilite = 10, ptsservice = 10, ptsretour = 10, ptsconcentration = 10, ptsendurance = 10, prix = 100, nom = "Test", proprio = joueur1.id, nivreq_id = 1)
                        objet.save()
		if arg2 > 800:
			arg = math.ceil(arg2*0.1)
			joueur1.argent += arg
			joueur2.argent -= arg		
	else:
		context2 = j2+" gagne "+strwin2+" !" 
		joueur1.defaite += 1
		joueur2.victoire += 1
		joueur1.points -= 60
		joueur2.points += 50
		winner = 2

	#Durabilite -1
	raquette.durabilite -= 1
	raquette.save()
	#Add exp
	
	for i in res1:
		exp += i
	joueur1.exp = exp

	joueur1.save()
	joueur2.save()

	res = []
	tour = len(nbtour) + 1
	score = len(nbtour) + 2
    	context = RequestContext(request, {
		'j1' : j1,
		'j2' : j2,
		'res1' : res1,
		'res2' : res2,
		'set1' : set1,
		'set2' : set2,
                'comm' : comm,
		'message' : message,
		'context2' : context2,
		'tour' : tour,
		'score' : score,
		's1j1' : s1j1,
		's1j2' : s1j2,
                's2j1' : s2j1,
                's2j2' : s2j2,
                's3j1' : s3j1,
                's3j2' : s3j2,
                's4j1' : s4j1,
                's4j2' : s4j2,
                's5j1' : s5j1,
                's5j2' : s5j2,
		'ptsj1' : ptsj1,
		'ptsj2' : ptsj2,
		'victj1' : victj1,
		'victj2' : victj2,
		'defj1' : defj1,
		'defj2' : defj2,
		'classj1' : classj1,
		'classj2' : classj2,
		'nbtour' : nbtour,
		'looter' : looter,
		'exp' : exp,
    	})
	

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

	add = table_match.objects.create(s1j1 = g1j1, s2j1 = g2j1, s3j1 = g3j1, s4j1 = g4j1, s5j1 = g5j1, s1j2 = g1j2, s2j2 = g2j2, s3j2 = g3j2, s4j2 = g4j2, s5j2 = g5j2, date_match = date_time, j1_id = joueur1.id, j2_id = joueur2.id, winner = winner)    
	add.save()
	return render(request, 'jeutennis/match.html', context)
    else:
	failmess = "Plus de vie"
	context = RequestContext(request, {
		'failmess' : failmess,
		})
	return render(request, 'jeutennis/match.html', context)
	#return HttpResponseRedirect('/index/')

def register(request):
    if request.method == "POST":
        form = UserReg(request.POST)
	if form.is_valid():
	    form.save()
	    username = form.cleaned_data['username']
	    prenom = form.cleaned_data['prenom']
	    nom = form.cleaned_data['nom']
	    date_naissance = form.cleaned_data['date_naissance']
	    user = User.objects.get(username=username)
	    add = table_joueurs.objects.create(nom = nom, prenom = prenom, date_naissance = date_naissance, user_id = user.id, date_train = "1970-01-01", adversaire = -1, date_match = "1970-01-01 00:00:00")
	    add.save()
	    return HttpResponseRedirect('/index/register_success/')
    args = {}
    args.update(csrf(request))

    args['form'] = UserReg()
    print args
    return render_to_response('jeutennis/register.html', args)	

def register_success(request):
    return render_to_response('jeutennis/register_success.html')

def index(request):
    return render(request, 'jeutennis/index4.html')

@login_required
def charts(request):
    joueur = table_joueurs.objects.filter().order_by('-points')
    class_joueurs = []
    list_joueurs = []
    class_user = []
    dayjoueurs = []
    daywin = []
    dnow = timezone.now()
    formdnow = str(dnow.year)+"-"+str(dnow.month)+"-"+str(dnow.day)    
    tomorrow = dnow + timedelta(days=1)
    formrrow = str(tomorrow.year)+"-"+str(tomorrow.month)+"-"+str(tomorrow.day)  
 
    for s in joueur:
	uid = s.user_id
	user = User.objects.get(id=uid)
        #nom_user = user_filter.username
	class_user.append(user.username)
	class_joueurs.append(s)
	list_joueurs.append(s.points)
    try:
    	selected_choice = request.POST['Day']
	if selected_choice == "Day":
            for p in table_match.objects.raw('SELECT *, COUNT(*) as total FROM `jeutennis_table_match` WHERE winner = 1 and date_match >= "%s" and date_match < "%s" GROUP BY j1_id ORDER BY total DESC' % (formdnow, formrrow)):
		dayjoueurs.append(p.j1)
		daywin.append(p.total)
            context2 = RequestContext(request, {'list_joueurs' : daywin, 'class_joueurs' : dayjoueurs,})
	    return render(request, 'jeutennis/charts.html', context2)	 
    except:
    	context = RequestContext(request, {'class_user' : class_user, 'list_joueurs' : list_joueurs, 'class_joueurs' : class_joueurs,})   
    	return render(request, 'jeutennis/charts.html', context)

@login_required
def calendar(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    aff_match = table_match.objects.filter(Q(j1 = joueur.id) | Q(j2 = joueur.id)).order_by('-date_match')[:20]
    res_s1j1 = []
    res_s2j1 = []
    res_s3j1 = []
    res_s4j1 = []
    res_s5j1 = []
    res_s1j2 = []
    res_s2j2 = []
    res_s3j2 = []
    res_s4j2 = []
    res_s5j2 = []
    res_j1 = []
    res_j2 = []
    adv = []
    adv1 = []
    comm = []
    winner = []
    date = []
	
    for s in aff_match:
	adv1.append(s.j1)
	adv.append(s.j2)
	if s.s5j1 == None:
		if s.s4j1 == None:
			comm.append(str(s.s1j1)+"/"+str(s.s1j2)+" - "+str(s.s2j1)+"/"+str(s.s2j2)+" - "+str(s.s3j1)+"/"+str(s.s3j2))
		else:
			comm.append(str(s.s1j1)+"/"+str(s.s1j2)+" - "+str(s.s2j1)+"/"+str(s.s2j2)+" - "+str(s.s3j1)+"/"+str(s.s3j2)+" - "+str(s.s4j1)+"/"+str(s.s4j2))
	else:
		comm.append(str(s.s1j1)+"/"+str(s.s1j2)+" - "+str(s.s2j1)+"/"+str(s.s2j2)+" - "+str(s.s3j1)+"/"+str(s.s3j2)+" - "+str(s.s4j1)+"/"+str(s.s4j2)+" - "+str(s.s5j1)+"/"+str(s.s5j2))	
        res_s1j1.append(s.s1j1)
        res_s2j1.append(s.s2j1)
        res_s3j1.append(s.s3j1)
        res_s4j1.append(s.s4j1)
        res_s5j1.append(s.s5j1)
        res_s1j1.append(s.s1j2)
        res_s2j1.append(s.s2j2)
        res_s3j1.append(s.s3j2)
        res_s4j1.append(s.s4j2)
        res_s5j1.append(s.s5j2)
	winner.append(s.winner)
	date.append(s.date_match)

    context = RequestContext(request, {
				'res_s1j1' : res_s1j1,
				'res_s2j1' : res_s2j1,
				'res_s3j1' : res_s3j1,
				'res_s4j1' : res_s4j1,
				'res_s5j1' : res_s5j1,
				'res_s1j2' : res_s1j2,
                                'res_s2j2' : res_s2j2,
                                'res_s3j2' : res_s3j2,
                                'res_s4j2' : res_s4j2,
                                'res_s5j2' : res_s5j2,
				'adv'	: adv,
				'adv1'  : adv1,
				'winner' : winner,
				'date' : date,
				'comm' : comm,
				})
    return render(request, 'jeutennis/calendar.html', context)

@login_required
def tournois(request, redirect_field_name=REDIRECT_FIELD_NAME):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    identity = joueur.id
    list_tournoi=[]
    id_tournoi=[]
    j_tournoi = joueur.idtournoi
    date_time = datetime.datetime.now()
    list_part = []
    tournoi1 = []
    tournoi2 = []
    tournoi3 = []
    notournoi = "Pas de tournoi pour le moment"
    dmax = date_time + timedelta(days=7)	
    pastlist = []
    winlist = []
    pastid = []
    try:
	selected_choice = request.POST['Past']
	if selected_choice == "Past":
    	    past_tournoi = table_tournoi.objects.filter(date_tournoi__lte=date_time).order_by('-date_tournoi')
	    for x in past_tournoi:
		pastlist.append(x.nom)
		winlist.append(x.wintour)
		pastid.append(x.id)
	    ziplist = zip(pastid, pastlist)
	    context2 = RequestContext(request, {'pastlist' : ziplist, 'winlist' : winlist, })
	    return render(request, 'jeutennis/tournois.html', context2)    

    except:
        req_tournoi = table_tournoi.objects.filter(date_tournoi__gte=date_time, date_tournoi__lte=dmax).order_by('-date_tournoi')[:3]
        try:
	    test = req_tournoi[0]
    	    for s in req_tournoi:
                list_tournoi.append(s.nom)	
	        id_tournoi.append(s.id)        

            try:
	        req_part = table_joueurs.objects.filter(idtournoi = id_tournoi[0]).order_by('-points')
    	        for s in req_part:
	            list_part.append(s)
            except:
	        message = "Pas de participants"
            try: 	
    	        tournoi1.append(id_tournoi[0])
    	        tournoi1.append(list_tournoi[0])
            except:
	        tournoi1.append("notournoi")
            try:
    	        tournoi2.append(id_tournoi[1])
    	        tournoi2.append(list_tournoi[1])
            except:
	        tournoi2.append("notournoi")
            try:
    	        tournoi3.append(id_tournoi[2])
    	        tournoi3.append(list_tournoi[2])
            except:
	        tournoi3.append("notournoi")
            id1 = tournoi1[0]    
            id2 = tournoi2[0]
            id3 = tournoi3[0]

            context = RequestContext(request, {
                'identity' : identity,
                'list_tournoi' : list_tournoi,
	        'id_tournoi' : id_tournoi,
	        'j_tournoi' : j_tournoi,
	        'list_part' : list_part,
	        'tournoi1' : tournoi1,
	        'tournoi2' : tournoi2,
	        'tournoi3' : tournoi3,
	        'id1' : id1,
	        'id2' : id2,
	        'id3' : id3,
                })

            redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

            try:
                selected_choice = request.POST['inscrit1']
	        joueur.idtournoi = id1
	        joueur.save()
	        return HttpResponseRedirect(redirect_to)
            except:
	        try:
	  	    selected_choice = request.POST['inscrit2']
		    joueur.idtournoi = id2
		    joueur.save()
		    return HttpResponseRedirect(redirect_to)
	        except (KeyError, table_joueurs.DoesNotExist):
		    try:
			selected_choice = request.POST['inscrit3']
			joueur.idtournoi = id3
        		joueur.save()
        		return HttpResponseRedirect(redirect_to)

 
    		    except (KeyError, table_joueurs.DoesNotExist):
    			try:
        			selected_choice = request.POST['desinscrit']
        			joueur.idtournoi=0
        			joueur.save()
				return HttpResponseRedirect(redirect_to)
  
    			except (KeyError, table_joueurs.DoesNotExist):
        			return render(request, 'jeutennis/tournois.html', context)

            return render(request, 'jeutennis/tournois.html', context)

        except:
	    contextfail = RequestContext(request, { 'message' : notournoi,})
	    return render(request, 'jeutennis/tournois.html', contextfail)

@login_required
def eventtournoi(request, idtournoi):
    numtournoi = table_tournoi.objects.get(id=idtournoi)
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    series = {}
    list_part = []
    serie = []
    i = 0
    message = "ok"
    newserie = []
    tableau = []
    tirage = numtournoi.tirage
    dtournoi = numtournoi.date_tournoi
    jid = []
    date_time = timezone.now()

    try:
        req_part = table_joueurs.objects.filter(idtournoi = numtournoi.id).order_by('-points')
	for s in req_part:
	    i += 1
	    series[i] = s
	    serie.append(i)
            list_part.append(s)
	    jid.append(s.id)
	    newserie.append("0")
    except:
        message = "Pas de participants"
  
     
    orderedseries = OrderedDict(sorted(series.items(), key=lambda t: t[0])) 
    if date_time >= dtournoi:
        
        #testserie = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]    
        #variable tirage bd 0/1
        if tirage == 0:
            testserie = serie
            n = len(testserie)
            random.shuffle(testserie)
            a = testserie.index(1)
            testserie[0], testserie[a] = testserie[a], testserie[0]
            b = testserie.index(2)
            testserie[n-1], testserie[b] = testserie[b], testserie[n-1]
            c = testserie.index(3)
            testserie[n/2], testserie[c] = testserie[c], testserie[n/2]
            d = testserie.index(4)
            testserie[n/2-1], testserie[d] = testserie[d], testserie[n/2-1]
	    fichier = open("/kevin/python/Projets/tennis/jeu/jeutennis/tournois/"+str(numtournoi.nom)+".txt","w")
	    for x in testserie:
                name = series.get(int(x))
                fichier.write(str(name.id)+"\n")
	    fichier.close()
	    for x in testserie:
                tableau.append(orderedseries[x])
            numtournoi.tirage = 1
            numtournoi.save()

        else:
	    testserie = []
	    fichier = open("/kevin/python/Projets/tennis/jeu/jeutennis/tournois/"+str(numtournoi.nom)+".txt","r")
	    line = fichier.read().splitlines()
	    for x in line:
	        testserie.append(x)
	    fichier.close()
	    for x in testserie:
	        req_part2 = table_joueurs.objects.get(id = x)
                tableau.append(req_part2)
	
    z = 0
    elimine = []
    
    context = RequestContext(request, {
	    'series' : orderedseries,
	    'message' : message,
	    'serie' : serie,
	    'list_part' : list_part,
	    'newserie' : tableau,
	    #'elimine' : elimine,
	    })

    return render(request, 'jeutennis/tournaments.html', context)

@login_required
def mp(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    aff_mp = message.objects.filter(dest = joueur.id)
    list_date = []
    list_sujet = []
    list_emet = []
    list_dest = []
    list_cont = []
    list_id = []
    list_crypt = []
    for x in aff_mp:
	list_date.append(x.date_mp)
	list_emet.append(x.emetteur)
	list_sujet.append(x.sujet)
	list_cont.append(x.contenu)
	list_id.append(x.id)
	list_crypt.append(x.crypt)

    ziplist = zip(list_id,list_sujet,list_crypt)

    aff_mp = message.objects.filter(emetteur = joueur.id)
    emet_date = []
    emet_sujet = []
    emet_dest = []
    emet_cont = []
    emet_id = []
    emet_crypt = []
    for x in aff_mp:
        emet_date.append(x.date_mp)
        emet_dest.append(x.dest)
        emet_sujet.append(x.sujet)
        emet_cont.append(x.contenu)
        emet_id.append(x.id)
        emet_crypt.append(x.crypt)

    ziplist2 = zip(emet_id,emet_sujet,emet_crypt)


    context = RequestContext(request, {
            'list_date' : list_date,
            'list_emet' : list_emet,
            'list_cont' : list_cont,
	    'list_sujet' : list_sujet,
            'list_id' : list_id,
	    'ziplist' : ziplist,
	    'emet_date' : emet_date,
            'emet_dest' : emet_dest,
            'emet_cont' : emet_cont,
            'emet_sujet' : emet_sujet,
            'emet_id' : emet_id,
            'ziplist2' : ziplist2,

	    })

    return render(request, 'jeutennis/mp.html', context)



@login_required
def viewmp(request, idmp, sujetmp):
    nummp = message.objects.get(id=idmp)
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    date_time = datetime.datetime.now()
    contenu = nummp.contenu
    sujet = nummp.sujet
    emetteur = nummp.emetteur
    date_mp = nummp.date_mp

    context = RequestContext(request, {
            'contenu' : contenu,
            'emetteur' : emetteur,
            'sujet' : sujet,
            'date_mp' : date_mp,
    })

    return render(request, 'jeutennis/viewmp.html', context)
@login_required
def newmp(request):
    user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        form = MPReg(request.POST)
        if form.is_valid():
            #form.save()
            destinataire = form.cleaned_data['destinataire']
	    try:
	    	prenom, nom = destinataire.split()
	    	dest = table_joueurs.objects.get(prenom = prenom, nom=nom)  
            except:
		bad_message = "Mauvais joueur"
		print(message)
		return HttpResponseRedirect('/index/mp/newmp/')
	    sujet = form.cleaned_data['sujet']
            contenu = form.cleaned_data['contenu']
            datenow = datetime.datetime.now()
    	    joueur = table_joueurs.objects.get(user_id = user.id)
            def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))
	    crypt = id_generator()
	    add = message.objects.create(emetteur_id = joueur.id, dest_id = dest.id, contenu = contenu, date_mp = datenow, sujet = sujet, crypt=crypt)
            add.save()
            return HttpResponseRedirect('/index/mp/mp_success/')
    args = {}
    args.update(csrf(request))

    args['form'] = MPReg()
    print args
    return render_to_response('jeutennis/newmp.html', args)

@login_required
def mp_success(request):
    return render_to_response('jeutennis/mp_success.html')

@login_required
def banque(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)    
    arg = joueur.argent
    cof = joueur.coffre
    message = "Ajout ok"
    error_message = "Veuillez entrer une valeur correcte !"
    trop_grand = "Vous n'avez pas cette somme !"
    contextfail = RequestContext(request, {
            'arg' : arg,
            'cof' : cof,
            'err' : error_message,
    })
    context = RequestContext(request, {
            'arg' : arg,
            'cof' : cof,
            'err' : message,
    })
    context2 = RequestContext(request, {
            'arg' : arg,
            'cof' : cof,
            'err' : trop_grand,
    })	


    try:
        selected_choice = request.POST['coffre']
	safearg = int(selected_choice)
    except (KeyError, table_joueurs.DoesNotExist):
        return render(request, 'jeutennis/banque.html', contextfail)
    except (ValueError):
	return render(request, 'jeutennis/banque.html', contextfail)	
    else:
	if (safearg > arg) or (safearg < 0):
	    return render(request, 'jeutennis/banque.html', context2)
	else:
	    safearg2 = safearg * 0.95
            joueur.coffre += safearg2
	    joueur.argent -= safearg
            joueur.save()
	    return HttpResponseRedirect('/index/banque')
	    #return render(request, 'jeutennis/banque.html', context)

@login_required
def myplayer(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    prenom = joueur.prenom
    nom = joueur.nom
    vict = joueur.victoire
    defaite = joueur.defaite
    serv = joueur.service
    ret = joueur.retour
    con = joueur.concentration
    endu = joueur.endurance
    points = joueur.points
    exp = joueur.exp
    argent = joueur.argent
    niveau = table_level.objects.get(id = joueur.niveau_id)
    nid = niveau.id
    max_exp = niveau.max_exp
    nargent = niveau.nargent
    nvictoire = niveau.nvictoire 
    tableau = table_joueurs.objects.filter().exclude(points__lte = points).annotate(total=Count('points'))
    classement = len(tableau) + 1
    equipement = table_equipement.objects.filter(proprio = joueur.id)
    tournoi = table_tournoi.objects.filter(wintour_id = joueur.id)
    list_equip = []
    list_tour = []
    levelup = 0
    if (exp > max_exp) and (vict > nvictoire) and (argent > nargent):
	levelup = 1 
    try:
        selected_choice = request.POST['levelup']
        if selected_choice == "levelup":
	    joueur.argent -= nargent
	    joueur.niveau_id += 1
	    joueur.save()
	return HttpResponseRedirect('/index/myplayer')
    except:
	try:
            for x in tournoi:
                list_tour.append(x.nom)
            y = list_tour[0]
        except:
            list_tour.append("Pas de palmares")
        context = RequestContext(request, {
		'prenom' : prenom,
		'nom' : nom,
		'vict' : vict,
		'defaite' : defaite,
		'serv' : serv,
		'ret' : ret,
		'endu' : endu,
		'con' : con,
		'points' : points,
		'list_equip' : list_equip,
		'list_tour' : list_tour,
		'classement' : classement,
		'exp' : exp,
		'niveau' : nid,
		'max_exp' : max_exp,
		'nvictoire' : nvictoire,
		'nargent' : nargent,		
		'levelup' : levelup,
		})
        return render(request, 'jeutennis/myplayer.html', context)

@login_required
def inventaire(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    niveau = joueur.niveau_id
    equip = table_equipement.objects.filter(proprio = joueur.id)
    tequip = []
    dur = []
    ptsserv = []
    ptsret = []
    ptscon = []
    ptsend = []
    prix = []
    lid = []
    nivreq = []
    is_equip = joueur.is_equip_id
    for x in equip:
	tequip.append(x.type_equip)
	dur.append(x.durabilite)
	ptsserv.append(x.ptsservice)
	ptsret.append(x.ptsretour)
	ptscon.append(x.ptsconcentration)
	ptsend.append(x.ptsendurance)
	arg = math.ceil(x.prix/2)
	prix.append(int(arg))
    	lid.append(x.id)
	nivreq.append(x.nivreq_id)
    try:
	y = tequip[0]
	ziplist = zip(lid,tequip,dur,ptsserv,ptsret,ptscon,ptsend,prix,nivreq)
    except:
	message = "Rien"
	context2 = RequestContext(request, { 'message' : message })
	return render(request, 'jeutennis/inventaire.html', context2)

    try:
        selected_choice = request.POST['Equiper']
	joueur.is_equip_id = int(selected_choice)
        joueur.save()
        return HttpResponseRedirect('/index/inventaire/')
    
    except:
	mess = "Pas de choix"

    try:
        selected_choice = request.POST['Vendre']
        sellequip = table_equipement.objects.get(id = int(selected_choice))
	joueur.argent += math.ceil(sellequip.prix/2)
	joueur.save()
	sellequip.proprio = 0
	sellequip.save()
        return HttpResponseRedirect('/index/inventaire/')

    except:
        mess = "Pas de choix"


    context = RequestContext(request, {
		'lid' : lid,
		'tequip' : tequip,
		'dur' : dur,
		'ptsserv' : ptsserv,
		'ptsret' : ptsret,
		'ptscon' : ptscon,
		'ptsend' : ptsend,
		'prix' : prix,
		'nivreq' : nivreq,
		'ziplist' : ziplist,
		'is_equip' : is_equip,
		'niveau' : niveau,
		} )
    return render(request, 'jeutennis/inventaire.html', context)

@login_required
def train_session(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    service = joueur.service
    retour = joueur.retour
    concentration = joueur.concentration
    endurance = joueur.endurance
    argent = joueur.argent
    listcaract = ["service","retour","concentration","endurance"]
    caract = [service,retour,concentration,endurance]
    newcaract = []
    cout = [300,500,700]
    intervalle = [3,5,7]
    level = ["Facile","Moyenne","Difficile"]
    ziptrain = zip(cout,intervalle,level)
    stats = []
    i = 0

    try:
	selected_choice = request.POST['Facile']
        joueur.argent -= cout[0]
	joueur.save()
	while i < 4:
            alea = int(random.randrange(0,2*intervalle[0]))
	    alea -= intervalle[0]
	    new = caract[i] + alea
	    if new < 0:
		new = 0
	    stats.append(alea)
	    newcaract.append(new)
	    i += 1
	zipup = zip(listcaract,newcaract)
	contextup = RequestContext(request, {
		'zipup' : zipup,
		'stats' : stats,
		'caract' : listcaract,
		'newcaract' : newcaract,
		})
	return render(request, 'jeutennis/train_session.html', contextup)

    except:
	try:
	    selected_choice = request.POST['Moyenne']
	    joueur.argent -= cout[1]
	    joueur.save()
            while i < 4:
                alea = int(random.randrange(0,2*intervalle[1]))
                alea -= intervalle[1]
                new = caract[i] + alea
		if new < 0:
                    new = 0
                stats.append(alea)
                newcaract.append(new)
                i += 1
	    zipup = zip(listcaract,newcaract)
            contextup = RequestContext(request, {
		'zipup' : zipup,
                'stats' : stats,
                'caract' : listcaract,
                'newcaract' : newcaract,
                })
            return render(request, 'jeutennis/train_session.html', contextup)



	except:
	    try:
		selected_choice = request.POST['Difficile']
		joueur.argent -= cout[2]
		joueur.save()
	        while i < 4:
	            alea = int(random.randrange(0,2*intervalle[2]))
        	    alea -= intervalle[2]
        	    new = caract[i] + alea
		    if new < 0:
                        new = 0
        	    stats.append(alea)
        	    newcaract.append(new)
        	    i += 1
		zipup = zip(listcaract,newcaract)
       		contextup = RequestContext(request, {
		    'zipup' : zipup,
        	    'stats' : stats,
                    'caract' : listcaract,
                    'newcaract' : newcaract,
                    })
        	return render(request, 'jeutennis/train_session.html', contextup)

	    except:
		try:
		    selected_service = request.POST[listcaract[0]]
		    selected_retour = request.POST[listcaract[1]]
                    selected_concentration = request.POST[listcaract[2]]
                    selected_endurance = request.POST[listcaract[3]]
 		    joueur.service = selected_service
    		    joueur.retour = selected_retour
    		    joueur.concentration = selected_concentration
    		    joueur.endurance = selected_endurance
		    joueur.save()
		    #contexttest = RequestContext(request, {
		    #	'selected_choice' : selected_service,
		    #	})
		    #return render(request, 'jeutennis/train_session.html', contexttest)		    
		    return HttpResponseRedirect('/index/train_session/')

		except:
    		    context = RequestContext(request, {
			'ziptrain' : ziptrain,
			'service' : service,
			'retour' : retour,
			'concentration' : concentration,
			'endurance' : endurance,
			'argent' : argent,
			})
    		    return render(request, 'jeutennis/train_session.html', context)

@login_required
def matchmenu(request):
    user = User.objects.get(username=request.user.username)
    joueur = table_joueurs.objects.get(user_id = user.id)
    niveau = joueur.niveau_id
    energie = joueur.vie
    argent = joueur.argent
    pts = joueur.points
    tableau = table_joueurs.objects.filter().exclude(points__lte = pts).annotate(total=Count('points'))
    classement = len(tableau) + 1

    context = RequestContext(request, {
	'niveau' : niveau,
	'energie' : energie,
	'argent' : argent,
	'classement' : classement,
	})
	
    return render(request, 'jeutennis/matchmenu.html', context)
