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

    return render(request,
                 'main/planche.html',
                 {
                  "appVersion":Constant.APP_VERSION
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
        
        pkVarAsked = request.POST.get('variety', -2)
        
        varAsked = Variete.objects.get(pk=pkVarAsked)
         
        print "var ", varAsked.pk, varAsked.nom, varAsked.famille, varAsked.famille.pk
        
        repIdFam = int(request.POST.get('famChoice', -1))
        print 'rep', repIdFam, type(repIdFam), ' / ', type(varAsked.famille.pk)
         
        if repIdFam == varAsked.famille.pk:
            message = "BRAVO"
        else:
            message = "PERDU"
            
        message += ", %s est de la famille des %ss " % (varAsked.nom, varAsked.famille)
            
        ## restart a new form
        form = forms.FormFamilyQuiz()

  
    form.var = random(Variete.objects.all().values("nom", "pk"))

    return render(request, 'main/quiz.html',
            {
             "message" : message,
             "form": form,
             "appVersion":Constant.APP_VERSION
            }
          )  
    
    


#################################################
