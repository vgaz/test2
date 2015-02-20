# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand       
from main.models import Famille, Variete
import csv

class Command(BaseCommand):
    
    help = "updateDB"

    def handle(self, *args, **options):
        
        reader = csv.DictReader(open("famillesLegumes.csv", "rb"))
        
        ## build family and variety tables        
        for l in reader:
            
            va = unicode(l.get("variete").lower().strip())            
            fam = unicode(l.get("famille").lower().strip())
            assert fam, "pas de famille pour : %s" % va
            l_fams = [unicode(f) for f in  Famille.objects.all().values_list("nom", flat=True)]

                
            if fam and fam not in l_fams:
                hFam = Famille()
                hFam.nom = fam
                hFam.save()

            if va and va not in Variete.objects.all().values_list("nom", flat=True):
                hVa = Variete()
                hVa.nom = va
                hVa.famille = Famille.objects.get(nom=fam)
                hVa.save()
        
        ## mise à jour associations
        reader = csv.DictReader(open("associationsPlantes.csv", "rb"))

        ## Vérif que toutes les variétés sont saisies en base
        for d_line in reader:
            
            variet = unicode(d_line.get("variete").lower())
            l_varAvec = [unicode(va.lower().strip()) for va in d_line.get("avec").split(",")]
            l_varSans = [unicode(va.lower().strip()) for va in d_line.get("sans").split(",")]

            l_ajoutSiBesoin = []
            l_ajoutSiBesoin.append(variet)
            l_ajoutSiBesoin.extend(l_varAvec)
            l_ajoutSiBesoin.extend(l_varSans)
            
            print l_ajoutSiBesoin
            l_dejaLa = [v for v in Variete.objects.all().values_list("nom", flat=True)]
            
            for _v in set(l_ajoutSiBesoin):
                if _v not in l_dejaLa:
                    v = Variete()
                    v.nom = _v
                    v.save()
                    print "ajout" , v


            v = Variete.objects.get( nom = variet )
                
            ## mise à jour des variétés qui peuvent ou pas aller avec celle-ci
            for var in l_varAvec:
                v.avec.add(Variete.objects.get( nom = var ))
            for var in l_varSans:
                v.sans.add(Variete.objects.get( nom = var ))
            
            v.save()


        self.stdout.write("end of command " + self.help)  
        
        
    