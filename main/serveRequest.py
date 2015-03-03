# -*- coding: utf-8 -*-
'''
Created on Nov 26, 2013

@author: vgazeill
'''

from django.http import HttpResponse
from models import Evenement
import datetime

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
    if cde =='ajoutPlan':
        print "ajoutPlan request"
        return HttpResponse("OK")
    
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
