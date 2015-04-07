# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from main.models import Evenement, Famille, Variete, PlantBase, Planche, TypeEvenement
admin.site.register(Evenement)
admin.site.register(Famille)
admin.site.register(Variete)
admin.site.register(Planche)
admin.site.register(PlantBase)
admin.site.register(TypeEvenement)
