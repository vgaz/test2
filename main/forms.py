# -*- coding: utf-8 -*-

from django import forms
from django.contrib.admin import widgets                                       

from main.models import Famille, Planche

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

class PlancheForm(forms.ModelForm):

    class Meta:
        model = Planche
#         exclude = ('done', )

    def clean(self):
        nom = self.cleaned_data.get('nom')
        num = self.cleaned_data.get('num')

        if False:
            msg = "I'm sure you didn't do this task before its deadline!"
            self._errors["done"] = self.error_class([msg])

        print nom, num
        return self.cleaned_data


