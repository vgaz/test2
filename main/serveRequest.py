# -*- coding: utf-8 -*-
'''
Created on Nov 26, 2013

@author: vgazeill
'''

from django.http import HttpResponse
from models import * ##Evenement, PlanBase, Planche, Variete
import sys

def serveRequest(request):
    """Received a request and return specific response"""

    ## --------------- request to get detail tests results
    cde = request.POST.get("cde","")
    print "cde =", cde
    if cde == "eeeee":          
        s_ = "okl"                                                                           
        s_json = '{"tests":[%s]}'% s_
        return HttpResponse( s_json, content_type="application/json")

    ## --------------- request to update database 
    if cde =='sauve_matrice':
        print __name__, "sauve_matrice"
        plant = PlantBase()
        plant.variete = Variete.objects.get(id = request.POST.get("variete",""))
        plant.nb_graines = int(request.POST.get("nb_graines",0))
        plant.largeur_cm = int(request.POST.get("largeur_cm",0))
        plant.hauteur_cm = int(request.POST.get("hauteur_cm",0))
        plant.coord_x_cm = int(request.POST.get("coord_x_cm",0))
        plant.coord_y_cm = int(request.POST.get("coord_y_cm",0))
        plant.planche = Planche.objects.get(id=request.POST.get("id_planche",0))
        plant.date_creation = datetime.datetime.now()
        try:
            plant.save()
            return HttpResponse('{"status":"true","id_plant":%d}'%plant.pk)
        except:
            return HttpResponse('{"status":"false","err":%s}'%sys.exc_info()[1])

    
    ## --------------- request to update database 
    if cde == "ajoutEvt":
        print "ajoutPlan request"
        date = datetime.datetime.strptime(request.POST.get("date",""), "%d-%m-%Y")
        evt = Evenement()
        evt.nom = request.POST.get("nom","")
        evt.date = date
        evt.plan_en_place = request.POST.get("ref_plan","")
        evt.date_creation = datetime.datetime.now()
        
        evt.save()
        return HttpResponse("OK")


    print "No action engaged for", request.POST

    return HttpResponse("No request treated inside serveRequest")
