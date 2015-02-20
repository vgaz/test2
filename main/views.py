# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import Variete, Famille
from django.template.defaultfilters import random

import forms
from django.contrib.messages.storage.base import Message

import Constant

#################################################

def home(request):
#    return HttpResponse( 'coucou', content_type="application/json")

    return render(request,
                 'main/home.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "appName":Constant.APP_NAME,
                  })
#################################################

def planche(request):

    num_planche = int(request.GET.get('num_planche', "1"))
    l_vars = Variete.objects.all().values_list("nom", flat=True)
    s_selectVars = ""
    xhtmlEditPlan = "".join(( "<p>Sur la planche %s. Plan N° $$PLAN_ID$$</p>"%num_planche,
                             "Variété : <input type='text' value=' ? ' name='Variete'/>",
                             "<br />Date de début d'activité",
                             "<br/>Evenements<br/><input type='button' value='Ajouter un évènement' name='ajout'/><br/>",
                             "<input type='button' value='Sauver le plan' name='sauver'/><br/>"
                             ))
    nb_col = 3
    nb_lig = 4
    nb_plans = nb_col * nb_lig
    return render(request,
                 'main/planche.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "num_planche": num_planche,
                  "l_lig":range(1, nb_lig + 1),
                  "l_col":range(1, nb_col + 1),
                  "l_plans": range(1, nb_plans +1),
                  "xhtmlEditPlan":xhtmlEditPlan,
                  "l_vars":l_vars,
                  })

#################################################

def var(request):

    return render(request,
                 'main/var.html',
                 {
                  "l_vars":Variete.objects.all(),
                  "l_fams":Famille.objects.all(),
                  "appVersion":Constant.APP_VERSION
                  })
    
#################################################

def quiz(request):
    message = ""
    
    form = forms.FormFamilyQuiz(request.POST or None)

    if form.is_valid():
        
        idVarAsked = request.POST.get('variete')
        
        varAsked = Variete.objects.get(id=idVarAsked)
     
        print "var ", varAsked.id, varAsked.nom, varAsked.famille 
        
        repIdFam = int(request.POST.get('famChoice', -1))
        
        print 'rep', repIdFam
         
        if repIdFam == varAsked.famille.pk:
            message = "BRAVO"
        else:
            message = "PERDU"
            
        message += ", %s est de la famille des %ss " % (varAsked.nom, varAsked.famille)
            
        ## restart a new form
        form = forms.FormFamilyQuiz()

  
    form.var = random(Variete.objects.filter(famille_id__in=[14,16,17,21]).values("nom", "id"))

    return render(request, 'main/quiz.html',
            {
             "message" : message,
             "form": form,
             "appVersion":Constant.APP_VERSION
            }
          )  
    
    


#################################################
