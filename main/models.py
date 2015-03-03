# -*- coding: utf-8 -*-
from django.db import models
import datetime

class Famille(models.Model):

    nom = models.CharField(max_length=100)
    
    class Meta: 
        ordering = ['nom']
        
    def __unicode__(self):
        return self.nom
    

class Variete(models.Model):

    nom = models.CharField(max_length=100)
    famille = models.ForeignKey(Famille, default="", blank=True)
    avec = models.ManyToManyField("self", related_name="avec", null=True, blank=True)
    sans = models.ManyToManyField("self", related_name="sans", null=True, blank=True)

    ## image = models.ImageField()
#    objects = MyManager()  ## objects est le nom par defaut du manager, ici surcharge eventuelle
    
    class Meta: 
        ordering = ['nom']
            
    def __unicode__(self):
        return self.nom

    
class Planche(models.Model):
    """object composant la structure de base qui sera dupliquée sur toute la longueur de la planche """
    
    num = models.IntegerField()
    nom = models.CharField(max_length=100, default="")
    longueur_m = models.IntegerField()
    largeur_cm = models.IntegerField()
    
    def __unicode__(self):
        return "Planche %d : %s, %d m x %d cm" % (self.num, self.nom, self.longueur_m, self.largeur_cm)
    
    
class PlanBase(models.Model):
    
    class Meta:
        verbose_name = "Plan de base"
        
    variete = models.ForeignKey(Variete)
    nb_of_seeds = models.IntegerField(default=1)
    largeur_cm = models.PositiveIntegerField()
    hauteur_cm = models.PositiveIntegerField()
        
    def __unicode__(self):
        return "%s (%d), %d x %d" %( self.variete, self.nb_of_seeds, self.largeur_cm, self.hauteur_cm)


class PlanBaseEnPlace(models.Model):
        
    class Meta:
        verbose_name = "Plan de base en place"

    plan_base  = models.ForeignKey('PlanBase')
    pos_x = models.PositiveIntegerField("Position en x")
    pos_y = models.PositiveIntegerField("Position en y")
    planche = models.ForeignKey('Planche')
    date_creation = models.DateField()
 
    def __unicode__(self):
        return "%s / position %d %d" %(self.plan_base, self.pos_x, self.pos_y)

class Evenement(models.Model):

    plan_en_place = models.ForeignKey(PlanBaseEnPlace)
    date_creation = models.DateTimeField(default=datetime.datetime.now())
    date = models.DateTimeField()
    bFini = models.BooleanField(default=False)
    nom = models.CharField(max_length=100, default="")
    texte = models.TextField(default="")
    
    class Meta: 
        ordering = ['date']
        
    def __unicode__(self):
        return self.nom
    