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

import Constant
from models import Planche
from forms import PlancheForm

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

def bilanPlanche(request):

    num_planche = int(request.GET.get('num_planche', "1"))
    return render(request,
                 'main/bilan_planche.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "num_planche": num_planche
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

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")
    
#     def form_valid(self, form):    si besoin de surcharge
#         form.save()
#         return http.HttpResponse("form is valid.")


   


#################################################

def editionPlanche(request):

    num_planche = int(request.GET.get('num_planche', 1))
    l_vars = Variete.objects.all()

    return render(request,
                 'main/edition_planche.html',
                 {
                  "appVersion":Constant.APP_VERSION,
                  "planche": Planche.objects.get(num = num_planche),
                  "l_vars":l_vars
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
