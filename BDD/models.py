from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

from BDD.choices import SEXE, TYPE, INCONNU_STATUT, \
    INCONNU_STATUT_TYPE, SALLES, INCONNU_STATUT_SALLE


# Create your models here.
class Personne(models.Model):
    sexe = models.IntegerField(choices=SEXE, default=INCONNU_STATUT)  # true = femme; false = homme
    adresse = models.CharField(max_length=200, null=True)  # adresse de le personne
    promotion = models.IntegerField(null=True)  # ex : 2017
    type = models.IntegerField(choices=TYPE, default=INCONNU_STATUT_TYPE)
    dateDeNaissance = models.DateField(null=True)  # date
    lieuDeNaissance = models.CharField(max_length=200, null=True)  # lieu de la naissance
    numeroDeTel = models.CharField(null=True, max_length=40)  # son 06
    user = models.OneToOneField(User)  # l'authentification est gérée pas django
    uploadDate = models.DateTimeField(default=datetime.now)  # date de l'upload
    filter= models.CharField(max_length=200)  # adresse de le personne
       
    def __str__ (self):
        return self.filter
class Groupe(models.Model):
    nom = models.CharField(max_length=30)  # nom du groupe
    personnes = models.ManyToManyField(Personne, blank=True)  # un groupe a plusieurs oersonne et une personne a plusieur groupe
    uploadDate = models.DateTimeField(default=datetime.now)  # date de l'upload
    
    def __str__ (self):
        return self.nom
class UV(models.Model):
    nom = models.CharField(max_length=30)  # nom de l'UV
        
    
    def __str__ (self):
        return self.nom   
class Module(models.Model):
    nom = models.CharField(max_length=30)  # nom du module    
    uv = models.ForeignKey(UV)
    def __str__ (self):
        return self.nom
    


        return self.semaine      
class Annee(models.Model):
    annee = models.IntegerField()
  
    def __str__ (self):
        return str(self.annee)     
class Moi(models.Model):
    nom = models.CharField(max_length=30) 
    nbMoi = models.IntegerField()
    annee = models.ForeignKey(Annee)
    def __str__ (self):
        return self.nom    
class Semaine(models.Model):
    semaine = models.IntegerField()
    moi = models.ForeignKey(Moi)
    def __str__ (self):
        return self.semaine   
      
class Salle(models.Model):
    nom = models.CharField(max_length=30)
    capacite = models.IntegerField(null=True)
    type = models.CharField(max_length=30, choices=SALLES, default=INCONNU_STATUT_SALLE)  # si c'est type info ou bien 
    def __str__ (self):
        return self.nom  
class Note(models.Model):
    note = models.IntegerField()
    personne = models.ForeignKey(Personne) 
    module = models.ForeignKey(Module)
    uploadDate = models.DateTimeField(default=datetime.now)  # date de l'upload
    def __str__ (self):
        return self.note     
class Cour(models.Model):
    nom = models.CharField(max_length=30)
    personnes = models.ManyToManyField(Personne, blank=True)  # un cour a plusieurs oersonne et une personne a plusieur cours
    groupe = models.ManyToManyField(Groupe, blank=True)  # un cour peut avoir plusieurs groupe et un groupe a plusieur cours
    isExam = models.BooleanField()
    salles = models.ManyToManyField(Salle, blank=True)
    semaine = models.ForeignKey(Semaine, null=True)
    uploadDate = models.DateTimeField(default=datetime.now)  # date de l'upload
    def __str__ (self):
        return self.nom 


   
       
    
    
    
    
    
    
    
     
    
    
