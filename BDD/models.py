from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

from BDD.choices import SEXE, TYPE, INCONNU_STATUT, \
    INCONNU_STATUT_TYPE, SALLES, INCONNU_STATUT_SALLE, SEMAINE, LUNDI


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
    filter = models.CharField(max_length=200)  # adresse de le personne
    


    
    def __str__ (self):
        return self.filter
class horaireProf(models.Model):
    prof = models.ForeignKey(Personne)
    jdelaSemaine = models.IntegerField(choices=SEMAINE, default=LUNDI)
    hminMatin = models.IntegerField()
    hmaxMatin = models.IntegerField()
    hminApresMidi = models.IntegerField()
    hmaxApresMidi = models.IntegerField()
    
    def __str__ (self):
        return self.get_jdelaSemaine_display() + " : " + str(self.hminMatin) + "/" + str(self.hmaxMatin) + " + " + str(self.hminApresMidi) + "/" + str(self.hmaxApresMidi)
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
        
        return "%s - %s" % (self.nom, self.uv.nom)
    


        return self.semaine        
class Salle(models.Model):
    nom = models.CharField(max_length=30)
    capacite = models.IntegerField(null=True)
    type = models.IntegerField(choices=SALLES, default=INCONNU_STATUT_SALLE) 
    def __str__ (self):
        return self.nom  
class Note(models.Model):
    note = models.IntegerField()
    personne = models.ForeignKey(Personne) 
    module = models.ForeignKey(Module)
    uploadDate = models.DateTimeField(default=datetime.now)  # date de l'upload
    def __str__ (self):
        return self.note     
class TypeCour(models.Model):
    nom = models.CharField(max_length=30)
    profs = models.ManyToManyField(Personne, blank=True)
    groupe = models.ManyToManyField(Groupe, blank=True)
    isExam = models.BooleanField()
    semaineMin = models.IntegerField()
    semaineMax = models.IntegerField()
    nbhpparsemaine = models.IntegerField()
    
class Cour(models.Model):
    typeCour = models.ForeignKey(TypeCour)
    salles = models.ManyToManyField(Salle, blank=True)
    uploadDate = models.DateTimeField(default=datetime.now)  # date de l'upload
    semaineMin = models.IntegerField()
    semaineMax = models.IntegerField()
    jour = models.IntegerField()
    hmin = models.IntegerField()
    hmax = models.IntegerField()
    def __str__ (self):
        return self.nom 


   
       
    
    
    
    
    
    
    
     
    
    
