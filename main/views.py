# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from models import Variete, Famille
from django.template.defaultfilters import random
from django.core import serializers
import forms
from django.contrib.messages.storage.base import Message
import datetime

import Constant
from models import Evenement, Planche, PlantBase, TypeEvenement
from forms import PlancheForm

#################################################

def home(request):
    l_planches = Planche.objects.all()
    return render(request,
                 'main/home.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "appName":Constant.APP_NAME,
                  "l_planches":l_planches
                  })
    
#################################################

def chronoPlanche(request):

    l_vars = Variete.objects.all()
    l_typesEvt = []
    for et in TypeEvenement.objects.all():
        l_typesEvt.append({"id" : et.id, 
                           "nom" : et.nom, 
                           "titre" : Constant.d_TitresTypeEvt[et.nom]})

    planche = Planche.objects.get(num = int(request.GET.get('num_planche', 1)))
    l_plants = PlantBase.objects.filter(planche = planche)
    l_evts = Evenement.objects.filter(plant_base__in = l_plants)
    if request.GET:
        date_debut_vue = datetime.datetime.strptime(request.GET.get("date_debut_vue",""), Constant.FORMAT_DATE)
        date_fin_vue = datetime.datetime.strptime(request.GET.get("date_fin_vue",""), Constant.FORMAT_DATE)
        
    return render(request,
                 'main/chrono_planche.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "planche": planche,
                  "l_typesEvt":l_typesEvt,
                  "l_plants":l_plants,
                  "l_evts": l_evts,
                  "date_debut_vue": date_debut_vue,
                  "date_fin_vue": date_fin_vue

                  })
#################################################

class CreationPlanche(CreateView):
    
    model = Planche
    form_class = PlancheForm
    template_name = 'main/creation_planche.html'
    success_url = reverse_lazy('creation_planche')
    http_method_names = ['get', 'post']
    
    def get_initials(self):
        return {  "appVersion":Constant.APP_VERSION,
                  "appName":Constant.APP_NAME
                }
    
    def dispatch(self, *args, **kwargs):
        return super(CreationPlanche, self).dispatch(*args, **kwargs)

    
#     def form_valid(self, form):    si besoin de surcharge
#         form.save()
#         return http.HttpResponse("form is valid.")


   


#################################################

def editionPlanche(request):

    l_vars = Variete.objects.all()
    l_typesEvt = []
    for et in TypeEvenement.objects.all():
        l_typesEvt.append({"id":et.id, 
                           "nom":et.nom, 
                           "titre":Constant.d_TitresTypeEvt[et.nom]})

    planche = Planche.objects.get(num = int(request.GET.get('num_planche', 1)))
    l_plants = PlantBase.objects.filter(planche = planche)

    return render(request,
                 'main/edition_planche.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "planche": planche,
                  "l_vars":l_vars,
                  "l_typesEvt":l_typesEvt,
                  "l_plants":l_plants
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
         
        if repIdFam == varAsked.famille.id:
            message = "BRAVO"
        else:
            message = "PERDU"

        message += ", %s est de la famille des %ss " % (varAsked.nom, varAsked.famille)

        ## restart a new form
        form = forms.FormFamilyQuiz()

    form.var = random(Variete.objects.filter(famille__isnull=False).values("nom", "id"))

    return render(request, 'main/quiz.html',
            {
             "message" : message,
             "form": form,
             "appVersion":Constant.APP_VERSION
            }
          )  
    
    


#################################################
