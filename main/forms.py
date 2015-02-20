# -*- coding: utf-8 -*-

from django import forms

from main.models import Famille

class FormFamilyQuiz(forms.Form):
    var = None
    l_choices = [(fam.pk, fam.nom) for fam in Famille.objects.all().order_by('nom')]
    famChoice = forms.ChoiceField( label = "Liste des familles",
                                    choices = l_choices, 
                                    widget=forms.RadioSelect())   
    
#    def clean(self):
#        pkResp = self.cleaned_data.get('famChoices')
#        if True:
#            msg = "rep = %s"%str(pkResp)
#            self._errors["done"] = self.error_class([msg])
#            self.stdout.write(msg)  
#
#        return self.cleaned_data
