# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from main.models import Evenement, Famille, Variete, PlanBase, PlanBaseEnPlace, Planche
admin.site.register(Evenement)
admin.site.register(Famille)
admin.site.register(Variete)
admin.site.register(Planche)
admin.site.register(PlanBase)
admin.site.register(PlanBaseEnPlace)

#
#class TaskAdmin(admin.ModelAdmin):
#    list_display = ["name", "group", "creation"]
#    list_display_link = ["name"]
#    list_filter = ["group"]
#    search_fields = ["name", "group"]
#    date_hierarchy = "creation"
#    
#admin.site.register(Task, TaskAdmin)
#    