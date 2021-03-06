# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from models import Variete, Famille
from django.template.defaultfilters import random

import forms
from django.contrib.messages.storage.base import Message
import datetime

from models import Evenement, Planche, PlantBase, Prevision, TypeEvenement
from forms import PlancheForm
import constant, planification

#################################################


def home(request):
    l_planches = Planche.objects.all()
    return render(request,
                 'main/home.html',
                 {
                  "appVersion":constant.APP_VERSION,
                  "appName":constant.APP_NAME,
                  "l_planches":l_planches
                  })
    
#################################################

def chronoPlanche(request):

    try:
        laPlanche, bRet = Planche.objects.get(num = int(request.POST.get("num_planche", request.GET.get("num_planche", 0))))
        print laPlanche
    except:
        s_msg = "Planche non trouvée... Est elle bien existante ?"
        return render(request, 'main/erreur.html',  { "appVersion":constant.APP_VERSION, "appName":constant.APP_NAME, "message":s_msg})

    delta20h = datetime.timedelta(hours=20)
    date_du_jour = datetime.datetime.now()

    if request.POST.get("date_debut_vue",""):
        date_debut_vue = datetime.datetime.strptime(request.POST.get("date_debut_vue", ""), constant.FORMAT_DATE)
        date_fin_vue = datetime.datetime.strptime(request.POST.get("date_fin_vue", ""), constant.FORMAT_DATE) + delta20h
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
                  "appVersion":constant.APP_VERSION,
                  "appName":constant.APP_NAME,
                  "planche": laPlanche,
                  "l_typesEvt":l_typesEvt,
                  "d_TitresTypeEvt": constant.d_TitresTypeEvt,
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
        return {  "appVersion":constant.APP_VERSION,
                  "appName":constant.APP_NAME
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
        dateVue = datetime.datetime.strptime(s_date, constant.FORMAT_DATE)
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
                           "titre":constant.d_TitresTypeEvt[et.nom]})
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
                  "appVersion":constant.APP_VERSION,
                  "planche": planche,
                  "l_vars":l_vars,
                  "l_typesEvt":l_typesEvt,
                  "l_plants":l_plants,
                  "date":dateVue
                  })

#################################################

def prevision_recolte(request):

    ## récup de la fenetre de temps
    delta20h = datetime.timedelta(hours=20)
    date_du_jour = datetime.datetime.now()
    if request.POST.get("date_debut_vue",""):
        date_debut_vue = datetime.datetime.strptime(request.POST.get("date_debut_vue", ""), constant.FORMAT_DATE)
        date_fin_vue = datetime.datetime.strptime(request.POST.get("date_fin_vue", ""), constant.FORMAT_DATE) + delta20h
    else:
        delta = datetime.timedelta(days=30)
        date_debut_vue = date_du_jour - delta
        date_fin_vue = date_du_jour + delta + delta20h
    date_debut_sem_vue = date_debut_vue - datetime.timedelta(days=date_debut_vue.weekday()) 
    date_fin_sem_vue = date_fin_vue + datetime.timedelta(days= 6 - date_fin_vue.weekday()) 
            
    ## sauvegarde des prévisions des récoltes
    if request.POST:
        for k, v in request.POST.items():
            ## gestion prévisions de récoltes
            if k.startswith("p__") and v:
                _, ds, var = k.split("__")
                obj = Prevision.objects.get_or_none(variete_id=var, date_semaine = ds)
                if not obj:
                    obj=Prevision()
                    obj.variete_id = var
                    obj.date_semaine = ds
                masse = int(v)
                if masse == 0: ## issu d'un enregistrement ayant précédement une masse différente de zéro
                    obj.delete()
                else:
                    obj.qte = masse
                    obj.save()
        
        if request.POST.get("option_planif", ""):
            print "planif"
            planification.planif(date_debut_sem_vue, date_fin_sem_vue)
                
    
    l_vars = Variete.objects.exclude(diametre_cm = 0)
    
    ## création de la liste des semaines     
    # on recadre sur le lundi pour démarrer en debut de semaine
    l_semaines = []
    date_debut_sem = date_debut_sem_vue
    while True:
        date_fin_sem = date_debut_sem + datetime.timedelta(days=6)
        l_semaines.append((date_debut_sem.isocalendar(), date_debut_sem, date_fin_sem))
        if date_fin_sem > date_fin_vue: 
            break
        date_debut_sem = date_fin_sem + datetime.timedelta(days=1)
    
    tab_previsions = "[" 
    for prev in Prevision.objects.filter(date_semaine__gte = date_debut_sem_vue, date_semaine__lte = date_fin_sem_vue):
        tab_previsions += "['%s', %d, %d],"%(prev.date_semaine.strftime("%Y-%m-%d"), prev.variete_id, prev.qte)
    tab_previsions += "]" 
    return render(request,
                 'main/prevision_recolte.html',
                 {
                  "appVersion":constant.APP_VERSION,
                  "date_debut_vue": date_debut_vue,
                  "date_fin_vue": date_fin_vue,
                  "l_vars":l_vars,
                  "l_semaines":l_semaines,
                  "tab_previsions" :tab_previsions,
                  "info":""
                  })
    
#################################################

def tab_varietes(request):
    
    l_vars = Variete.objects.filter(diametre_cm__isnull=False)
    for v in l_vars:
        v.nomUniteProd = constant.D_UNITE_PROD_NAME[v.unite_prod]
     
    return render(request,
                 'main/tab_varietes.html',
                 {
                  "l_vars":l_vars,
                  "l_fams":Famille.objects.all(),
                  "appVersion":constant.APP_VERSION,
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
             "appVersion": constant.APP_VERSION
            }
          )  
    
    


#################################################
