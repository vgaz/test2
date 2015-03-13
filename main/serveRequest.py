# -*- coding: utf-8 -*-
'''
Created on Nov 26, 2013

@author: vgazeill
'''

from django.http import HttpResponse
from models import Evenement, PlantBase, Planche, Variete
import sys

def serveRequest(request):
    """Received a request and return specific response"""

    ## --------------- request to get detail tests results
    cde = request.POST.get("cde","")
    print "cde =", cde
    if cde == "getEvtsPlant": 
        try:
            id = int(request.POST.get("id", 0))
            l_evts = Evenement.objects.filter(plant_base_id = id)
            s_ = ','.join(['{"nom":"%s","date":"%s","type":"%s"}'%(   item.nom, 
                                                                      item.date, 
                                                                      item.type) for item in l_evts])           
            s_json = '{"status":"true","l_evts":[%s]}'% s_
        except:
            print(__name__ + ': ' + str(sys.exc_info()[1]) )
            s_json = '{"status":"false","err":%s}'%sys.exc_info()[1]
             
        return HttpResponse( s_json, content_type="application/json")


    ## --------------- request to update database 
    if cde =='sauve_plant':
        print __name__, "sauve_plant"

        try:
            id_plant = request.POST.get("id")
            if '_' in id_plant:
                plant = PlantBase() ## un nouveau
            else:
                plant = PlantBase.objects.get(id=int(id_plant))
     
            plant.variete = Variete.objects.get(id = request.POST.get("variete",""))
            plant.nb_graines = int(request.POST.get("nb_graines",0))
            plant.largeur_cm = int(request.POST.get("largeur_cm",0))
            plant.hauteur_cm = int(request.POST.get("hauteur_cm",0))
            plant.coord_x_cm = int(request.POST.get("coord_x_cm",0))
            plant.coord_y_cm = int(request.POST.get("coord_y_cm",0))
            plant.planche = Planche.objects.get(num=int(request.POST.get("id_planche",0)))
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
