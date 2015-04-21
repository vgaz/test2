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
        
        ## maj croisssance plantes
        reader = csv.DictReader(open("croissancePlantes.csv", "rb"))
        for d_line in reader:
            variet = unicode(d_line.get("variete").decode("utf-8")).lower()
            try:
                v = Variete.objects.get(nom = variet)
            except:
                self.stdout.write("Ajout " + variet)
                v = Variete()
                v.nom = variet
        
            v.date_min_plantation = unicode(d_line.get("date_min_plantation").decode("utf-8"))
            v.date_max_plantation = unicode(d_line.get("date_max_plantation").decode("utf-8"))
            v.duree_avant_recolte_j = int(d_line.get("duree_avant_recolte_j"))
            v.prod_hebdo_moy_g = d_line.get("prod_hebdo_moy_g")
            v.diametre_cm = int(d_line.get("diametre_cm"))
            v.save()
          
        
        ## maj des familles pour chaque variété
        fic = "famillesLegumes.csv"
        reader = csv.DictReader(file(fic, "rb"))
        l_fams = [unicode(f) for f in Famille.objects.all().values_list("nom", flat=True)]
        l_fams_sup = []
        for d_line in reader:
            
            variet = unicode(d_line.get("variete").decode("utf-8")).lower()
            try:
                hVa = Variete.objects.get(nom = variet)
            except:
                self.stdout.write("Ajout " + variet)
                v = Variete()
                v.nom = variet
                v.save()       

            try:
                fam = unicode(d_line.get("famille","").decode('utf-8')).lower().strip()
                
                if fam and fam not in l_fams and fam not in l_fams_sup:
                    print "ajout famille %s"%fam
                    hFam = Famille()
                    hFam.nom = fam
                    hFam.save()
                    l_fams_sup.append(fam)
            
                if not hVa.famille:
                    hVa.famille = Famille.objects.get(nom=fam)
                    hVa.save()
                    print "maj %s / %s"%(hVa.nom, hVa.famille)
                    
            except:
                print "pb, pas de famille accessible pour %s dans le fichier %s" %(variet, fic)
                
        ## mise à jour associations
        l_variets = Variete.objects.all().values_list("nom", flat=True)
        l_variets_sup = []
        reader = csv.DictReader(open("associationsPlantes.csv", "rb"))
        for d_line in reader:
            
            variet = unicode(d_line.get("variete").decode("utf-8")).lower()
            
            try:
                s_tmp = unicode(d_line.get("avec","").decode("utf-8")).lower()
                l_varAvec = [unicode(va.strip()) for va in s_tmp.split(",") if va]
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
                        
            for _v in set(l_ajoutSiBesoin):
                if _v and _v not in l_variets and _v not in l_variets_sup:
                    v = Variete()
                    v.nom = _v
                    v.save()
                    l_variets_sup.append(_v)
                    print "ajout variété" , v

            v = Variete.objects.get(nom = variet)
                
            ## mise à jour des variétés qui peuvent ou pas aller avec celle-ci
            for var in l_varAvec:
                v.avec.add(Variete.objects.get( nom = var ))
            for var in l_varSans:
                v.sans.add(Variete.objects.get( nom = var ))

            v.save()
        

            

        self.stdout.write("end of command " + self.__doc__)  
        
        
    