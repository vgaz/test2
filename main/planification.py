# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import random

import forms
from django.contrib.messages.storage.base import Message
import datetime

from models import Prevision, Production, PlantBase, Variete
from main import constant

#################################################


def planif(dateDebut, dateFin):
    
    ## on balaye semaine par semaine
    dateSemaine = dateDebut
    while dateSemaine <= dateFin:
        
        ## 1 récupération des productions demandées
        for prev in Prevision.objects.filter(date_semaine = dateSemaine):
            
            ## 2 test si dispo en tout ou partie sur production actuelle
            for prod in Production.objects.get_or_none(date_semaine = dateSemaine, variete_id = prev.variete_id):
                if prod:
                    print "production trouvée", prod
                    ## déduction de tout ou partie de la quantité demandée
                    reste = prod.qte - prod.qte_bloquee - prev.qte 
                    print "reste", reste
                    if reste >= 0:
                        prod.qte_bloquee = reste
                        break ## on a assez donc on bloque et on passe à la variété suivante
                    else:
                        print "création de plants supplémentaires pour répondre au besoin"
                        plant = PlantBase()
                        var = Variete.objects.get(variete_id = prev.variete_id)
                        plant.variete = var
                        plant.nb_graines = reste * var.
                        plant.largeur_cm = models.PositiveIntegerField('largeur cm')
                        plant.hauteur_cm = models.PositiveIntegerField('hauteur cm')
                        plant.coord_x_cm = models.PositiveIntegerField("pos x cm")
                        plant.coord_y_cm = models.PositiveIntegerField("pos y cm")
                        #plant.planche = @todo:   pas de planche attribuée , 
                        
        
    
