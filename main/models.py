# -*- coding: utf-8 -*-
from django.db import models
import datetime

class Famille(models.Model):
    """famille associée à la plante"""
    nom = models.CharField(max_length=100)
    
    class Meta: 
        ordering = ['nom']
        
    def __unicode__(self):
        return self.nom
    
class Variete(models.Model):
    """variété de plante"""
    nom = models.CharField(max_length=100)
    famille = models.ForeignKey(Famille,  null=True, blank=True)
    avec = models.ManyToManyField("self", related_name="avec", null=True, blank=True)
    sans = models.ManyToManyField("self", related_name="sans", null=True, blank=True)
    date_min_plantation = models.CharField("date (jj/mm) de début de plantation", max_length=10, default="0/0")
    date_max_plantation = models.CharField("date (jj/mm) de fin de plantation", max_length=10, default="0/0")
    duree_avant_recolte_j = models.IntegerField("durée en terre avant récolte (jours)", default=0)
    prod_hebdo_moy_g = models.CommaSeparatedIntegerField("suite de production hebdomadaire moyenne (grammes)", max_length=20, default="0,0") ##attention, pour les légumes "à la pièce" ( choux, salades..), ne saisir qu'une valeur 
    diametre_cm = models.IntegerField("diamètre (cm)", default=0)

    image = models.ImageField()
#    objects = MyManager()  ## objects est le nom par defaut du manager, ici surcharge eventuelle
    
    class Meta: 
        ordering = ['nom']
            
    def __unicode__(self):
        return self.nom

    
class Planche(models.Model):
    """object composant la structure de base qui sera dupliquée sur toute la longueur de la planche """
    
    num = models.IntegerField(unique=True)
    nom = models.CharField(max_length=100, default="")
    longueur_m = models.IntegerField()
    largeur_cm = models.IntegerField()
    
    def __unicode__(self):
        return "Planche %d : %s, %d m x %d cm" % (self.num, self.nom, self.longueur_m, self.largeur_cm)
    
    
class PlantBase(models.Model):
    
    class Meta:
        verbose_name = "Plant de base"
        
    variete = models.ForeignKey(Variete)
    nb_graines = models.IntegerField(default=1)
    largeur_cm = models.PositiveIntegerField('largeur cm')
    hauteur_cm = models.PositiveIntegerField('hauteur cm')
    coord_x_cm = models.PositiveIntegerField("pos x cm")
    coord_y_cm = models.PositiveIntegerField("pos y cm")
    planche = models.ForeignKey('Planche')
       
    def __unicode__(self):
        return "%d %s (%d), %d x %d, pos: %d %d sur planche %d" %( self.id,  self.variete, 
                                                                self.nb_graines, 
                                                                self.largeur_cm, 
                                                                self.hauteur_cm, 
                                                                self.coord_x_cm, 
                                                                self.coord_y_cm, 
                                                                self.planche.num)

class TypeEvenement(models.Model):
    
    nom = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.nom
    
class Evenement(models.Model):

    plant_base = models.ForeignKey(PlantBase)
    date_creation = models.DateTimeField(default=datetime.datetime.now())
    date = models.DateTimeField()
    duree = models.PositiveIntegerField("nb jours d'activité")
    nom = models.CharField(max_length=100, default="")
    texte = models.TextField(default="")
    bFini = models.BooleanField(default=False)
    type =  models.ForeignKey(TypeEvenement)

    class Meta: 
        ordering = ['date']
        
    def __unicode__(self):
        return "%d %s %s"%(self.plant_base_id, self.date, self.type)
    