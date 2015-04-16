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

    try:
        laPlanche = Planche.objects.get(num = int(request.POST.get("num_planche", request.GET.get("num_planche", 0))))
        print laPlanche
    except:
        s_msg = "Planche non trouvée... Est elle bien existante ?"
        return render(request, 'main/erreur.html',  { "appVersion":Constant.APP_VERSION, "appName":Constant.APP_NAME, "message":s_msg})

    delta20h = datetime.timedelta(hours=20)
    date_du_jour = datetime.datetime.now()

    if request.POST.get("date_debut_vue",""):
        date_debut_vue = datetime.datetime.strptime(request.POST.get("date_debut_vue", ""), Constant.FORMAT_DATE)
        date_fin_vue = datetime.datetime.strptime(request.POST.get("date_fin_vue", ""), Constant.FORMAT_DATE) + delta20h
    else:
        delta = datetime.timedelta(days=60)
        date_debut_vue = date_du_jour - delta
        date_fin_vue = date_du_jour + delta + delta20h
    
    decalage_j = int(request.POST.get("decalage_j", 10))
    delta = datetime.timedelta(days = decalage_j)
    if request.POST.get("direction", "") == "avance":
        date_debut_vue += delta 
        date_fin_vue += delta
    if request.POST.get("direction", "") == "recul":
        date_debut_vue -= delta 
        date_fin_vue -= delta        
        
    l_typesEvt = TypeEvenement.objects.all()
    
    ## on prend tous les evts de l'encadrement et pour la planche courrante
    l_evts = Evenement.objects.filter(date__gte = date_debut_vue, 
                                      date__lte = date_fin_vue, 
                                      plant_base__in = PlantBase.objects.filter(planche_id = laPlanche))
    ## on en deduit les plants impliqués, même partiellement
    l_plantsId = list(set([evt.plant_base_id for evt in l_evts]))
    ## on recupère de nouveau tous les évenements des plants impactés , même ceux hors fenetre temporelle
    l_evts = Evenement.objects.filter(plant_base_id__in = l_plantsId).order_by('plant_base_id', 'date')
    l_plants = PlantBase.objects.filter(planche_id = laPlanche, id__in = l_plantsId )

    return render(request,
                 'main/chrono_planche.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "appName":Constant.APP_NAME,
                  "planche": laPlanche,
                  "l_typesEvt":l_typesEvt,
                  "d_TitresTypeEvt": Constant.d_TitresTypeEvt,
                  "l_plants":l_plants,
                  "l_evts": l_evts,
                  "date_debut_vue": date_debut_vue,
                  "date_fin_vue": date_fin_vue,
                  "date_du_jour" : date_du_jour,
                  "decalage_j":decalage_j
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

    planche = Planche.objects.get(num = int(request.GET.get('num_planche', 0)))
    s_date = request.POST.get("date", "")
    if s_date:
        dateVue = datetime.datetime.strptime(s_date, Constant.FORMAT_DATE)
    else:
        dateVue = datetime.datetime.now()
        
    if request.POST.get("delta", "") == "demain":
        dateVue += datetime.timedelta(days=1)
    if request.POST.get("delta", "") == "hier":
        dateVue += datetime.timedelta(days=-1)

    l_vars = Variete.objects.all()
    l_typesEvt = []
    for et in TypeEvenement.objects.all():
        l_typesEvt.append({"id":et.id, 
                           "nom":et.nom, 
                           "titre":Constant.d_TitresTypeEvt[et.nom]})
    ## filtrage par date
    l_evts_debut = Evenement.objects.filter(type = TypeEvenement.objects.get(nom = "debut"), date__lte = dateVue)
    l_PlantsIds = list(l_evts_debut.values_list('plant_base_id', flat=True))
    print l_PlantsIds
    ## recup des evenement de fin ayant les memes id_plants que les evts de debut 
    l_evts = Evenement.objects.filter(type = TypeEvenement.objects.get(nom = "fin"), plant_base_id__in = l_PlantsIds, date__gte = dateVue)
    
    l_PlantsIds = l_evts.values_list('plant_base_id', flat=True)
    print l_PlantsIds
    l_plants = PlantBase.objects.filter(planche = planche, id__in = l_PlantsIds)
    
    return render(request,
                 'main/edition_planche.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "planche": planche,
                  "l_vars":l_vars,
                  "l_typesEvt":l_typesEvt,
                  "l_plants":l_plants,
                  "date":dateVue
                  })

#################################################

def tab_varietes(request):
    l_vars = Variete.objects.filter(diametre_cm__isnull=False)
    return render(request,
                 'main/tab_varietes.html',
                 {
                  "l_vars":l_vars,
                  "l_fams":Famille.objects.all(),
                  "appVersion":Constant.APP_VERSION
                  })
    
#################################################

def quizFamilles(request):
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

    form.var = random(Variete.objects.filter(famille__isnull=False, diametre_cm__isnull=False).values("nom", "id"))

    return render(request, 'main/quizFamilles.html',
            {
             "message" : message,
             "form": form,
             "appVersion": Constant.APP_VERSION
            }
          )  
    
    


#################################################
