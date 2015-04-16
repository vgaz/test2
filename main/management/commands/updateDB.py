# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand       
from main.models import Famille, Variete, TypeEvenement, Planche
import csv
from main.Constant import d_TitresTypeEvt
       
class Command(BaseCommand):
    """updateDB command"""
    help = "updateDB"

    def handle(self, *args, **options):
        
        ## maj type d'évenement
        l_typeEvt = TypeEvenement.objects.all().values_list("nom", flat=True)
        for n in d_TitresTypeEvt.keys():    
            if n in l_typeEvt: continue 
            hTE = TypeEvenement()
            hTE.nom = n
            hTE.save()
        
        reader = csv.DictReader(file("famillesLegumes.csv", "rb"))
        
        ## build family and variety tables        
        for l in reader:
            
            va = unicode(l.get("variete").decode('utf-8')).lower().strip()            
            fam = unicode(l.get("famille","").decode('utf-8')).lower().strip()
            l_fams = [unicode(f) for f in Famille.objects.all().values_list("nom", flat=True)]

            if fam and fam not in l_fams:
                hFam = Famille()
                hFam.nom = fam
                hFam.save()
                print "ajout %s"%fam

            if va and va not in Variete.objects.all().values_list("nom", flat=True):
                hVa = Variete()
                hVa.nom = va
                hVa.save()
                print "ajout %s"%va
            
            if va and fam: 
                hVa = Variete.objects.get(nom=va)
                hVa.famille = Famille.objects.get(nom=fam)
                hVa.save()
                print "%s = %s"%(va, fam)

                
        ## mise à jour associations
        reader = csv.DictReader(open("associationsPlantes.csv", "rb"))

        ## Vérif que toutes les variétés sont saisies en base
        for d_line in reader:
            
            variet = unicode(d_line.get("variete").decode("utf-8")).lower()
            
            try:
                s_tmp = unicode(d_line.get("avec","").decode("utf-8")).lower()
                l_varAvec = [ va.strip() for va in s_tmp.split(",") if va ]
            except:
                l_varAvec = []
                
            try:
                s_tmp = unicode(d_line.get("sans","").decode('utf-8')).lower()
                l_varSans = [unicode(va.strip()) for va in s_tmp.split(",") if va]
            except:
                l_varSans = []

            l_ajoutSiBesoin = []
            l_ajoutSiBesoin.append(variet)
            l_ajoutSiBesoin.extend(l_varAvec)
            l_ajoutSiBesoin.extend(l_varSans)
            
            l_dejaLa = Variete.objects.all().values_list("nom", flat=True)
            
            for _v in set(l_ajoutSiBesoin):
                if _v and _v not in l_dejaLa:
                    v = Variete()
                    v.nom = _v
                    v.save()
                    print "ajout" , v

            v = Variete.objects.get(nom = variet)
                
            ## mise à jour des variétés qui peuvent ou pas aller avec celle-ci
            for var in l_varAvec:
                v.avec.add(Variete.objects.get( nom = var ))
            for var in l_varSans:
                v.sans.add(Variete.objects.get( nom = var ))
            
            ## 
            v.date_min_plantation = "20/03"
            v.date_max_plantation = "20/05"
            v.duree_pousse_min_j = 60
            v.duree_pousse_max_j = 90
            v.masse_utile_kg = 0.5
            v.diametre_cm = 30

            v.save()

        self.stdout.write("end of command " + self.__doc__)  
        
        
    