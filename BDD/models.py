# -*- coding: utf-8 -*-
"""
    The ''models'' module
    ======================
    
    It defines what is on the database
    
    :Exemple:
    
    >> uv=UV() 
    >> uv.nom="nom de l\'uv"
    >> uv.save()
    save an UV in the database
    
    
@author: IWIMBDSL
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from BDD.choices import SEXE, TYPE, INCONNU_STATUT, \
    INCONNU_STATUT_TYPE, SALLES, INCONNU_STATUT_SALLE, SEMAINE, LUNDI, TYPENEWS, \
    TYPENEWSG, AJOUT


class Personne(models.Model):
    """
        It defines how a person is stocked in the database.
        
        A person is related to an user (OnetoOne relation)
        (A user has especially a first name, last name, email, login and a password)
        
        A Person has a sex, an address, a promotion, a type (professor/admin/student...), a date of birth,  
        a place of birth, a phone number.
        
        It has also an upload date.
        
        It has also a filter (which defines a person in a unique way), used in forms.
        
        :exemple:
        >> from django.contrib.auth.models import User
        >> from BDD.choices import HOMME_STATUT, ELEVE_STATUT
        >> user=User(first_name="Jimmy", last_name="Page", username="LedZep", password="123456", email="jimmy@ledzep.com")
        >> user.save()
        >> p = Personne()
        >> p.sexe=HOMME_STATUT
        >> p.type=ELEVE_STATUT
        >> p.user=user
        >> p.save()
        save a person in the database (some files like promotion are optional)
        
    """
    
    sexe = models.IntegerField(choices=SEXE, default=INCONNU_STATUT)  # true = femme; false = homme
    adresse = models.CharField(max_length=200, null=True)  # adresse de le personne
    promotion = models.IntegerField(null=True)  # ex : 2017
    type = models.IntegerField(choices=TYPE, default=INCONNU_STATUT_TYPE)
    dateDeNaissance = models.DateField(null=True)  # date
    lieuDeNaissance = models.CharField(max_length=200, null=True)  # lieu de la naissance
    numeroDeTel = models.CharField(null=True, max_length=40)  # son 06
    user = models.OneToOneField(User)  # l'authentification est gérée pas django
    uploadDate = models.DateTimeField(default=timezone.now())  # date de l'upload
    filter = models.CharField(max_length=200)  # adresse de le personne
    
    def __str__ (self):
        return self.filter
class horaireProf(models.Model):
    """ 
        Pas encore utilisé
    """
    prof = models.ForeignKey(Personne)
    jdelaSemaine = models.IntegerField(choices=SEMAINE, default=LUNDI)
    hminMatin = models.IntegerField()
    hmaxMatin = models.IntegerField()
    hminApresMidi = models.IntegerField()
    hmaxApresMidi = models.IntegerField()
    
    def __str__ (self):
        return self.get_jdelaSemaine_display() + " : " + str(self.hminMatin) + "/" + str(self.hmaxMatin) + " + " + str(self.hminApresMidi) + "/" + str(self.hmaxApresMidi)
class Groupe(models.Model):
    """
        It defines how a group is stocked in the database.
        
        A group has a name
         
        A group is related to persons and modules (ManytoMany relation)
    
        It has also an upload date.
        
        :exemples:
        
        >> g = Group()
        >> g.nom="MPSI 1"
        >> g.save()
        save a groupe in the database (some files like promotion are optional and the upload date is made automatically)
        
        >> uv=UV(nom="2.9")
        >> uv.save()
        >> m = Module(nom="connaissance de soi", uv=uv)
        >> m.save()
        >> g = Groupe(nom="CM2")
        >> g.modules.add(m) 
        >> g.save()
        add a module in a group
        
    """
    nom = models.CharField(max_length=30)  # nom du groupe
    personnes = models.ManyToManyField(Personne, blank=True)  # un groupe a plusieurs oersonne et une personne a plusieur groupe
    uploadDate = models.DateTimeField(default=timezone.now())  # date de l'upload
    #########"   modif momo #########################
    
    modules=models.ManyToManyField('Module', blank=True)
    
    #########"   fin modif momo #########################
    def __str__ (self):
        return self.nom
class UV(models.Model):
    """
        It defines how an UV is stocked in the database.
        
        An UV has a name
       
        :exemple:
        
        >> uv=UV(nom="7.5")
        >> uv.save()
        save an UV in the database 
        
    """
    nom = models.CharField(max_length=30)  # nom de l'UV
        
    
    def __str__ (self):
        return self.nom   
class Module(models.Model):
    """
        It defines how a module is stocked in the database.
        
        A module has a name and it is related to an UV (OnetoMany relation)
        
        :exemple:
        
        >> uv=UV(nom="2.9")
        >> uv.save()
        >> m = Module(nom="géopolitique de brest", uv=uv)
        >> m.save()
        save a module in the database 
    """  
    nom = models.CharField(max_length=30)  # nom du module    
    uv = models.ForeignKey(UV)
    
    def __str__ (self):
        
        return "%s - %s" % (self.nom, self.uv.nom)
    
 
class Salle(models.Model):
    """
        It defines how a classroom is stocked in the database.
        
        A classroom has a name, a capacity, and a type (classroom with comptuer/lab...)
        
        :exemple:
        >> from BDD.choices import INFO_STATUT
        >> s=SALLE(nom="404", capacite=30, type= INFO_STATUT)
        >> s.save()
        save a classroom in the database 
    """
   
    nom = models.CharField(max_length=30)
    capacite = models.IntegerField(null=True)
    type = models.IntegerField(choices=SALLES, default=INCONNU_STATUT_SALLE) 
    def __str__ (self):
        return self.nom  
class Note(models.Model):
    """
        It defines how a mark is stocked in the database.
        
        It has a number (the mark), and an upload date.
        
        Tt is related to persons (the persons marked and in an other place professors) 
        and modules (OnetoMany relation)
        
        :exemple:
        
        >> p= Personne.objects.get(id=3) # get a person which his id is equal to 3
        >> m = Module.objects.get(id=2)
        >> prof = Module.objects.get(id=1)
        >> note = Note(note=0, personne=p, module=m, prof=prof)
        >> note.save()
        save a mark in the database 
    """
   
    note = models.IntegerField()
    personne = models.ForeignKey(Personne) 
    module = models.ForeignKey(Module)
    prof= models.ForeignKey(Personne, related_name="ANoter")
    uploadDate = models.DateTimeField(default=timezone.now())  # date de l'upload
    def __str__ (self):
        return str(self.note)    
class TypeCour(models.Model):
    """
        It defines a type of lesson.
        
        It has a name and a boolean value which defines if it is an exam or not.
        
        Tt is related to persons (professors) and groups (ManytoMany relations)
        
        :exemple:
        
        >> m = Groupe.objects.get(id=2)
        >> prof = Module.objects.get(id=1)
        >> t = TypeCour(nom="Sport")
        >> t.profs.add(prof)
        >> t.groups.add(groupe)
        >> t.save()
        save a type of lesson in the database 
    """
    nom = models.CharField(max_length=30)
    profs = models.ManyToManyField(Personne, blank=True)
    groupe = models.ManyToManyField(Groupe, blank=True)
    isExam = models.BooleanField()
    def __str__ (self):
        return self.nom
class Cour(models.Model):
    """
        It defines a lesson.
        
        It has a name, an upload date, 2 integers which represent the start and the end of the lesson in weeks,
        2 others for the hours and another for the day.
        
        It is related to a type of lesson (OneToMany relation) and classrooms (ManyToMany relation)
        
        :exemple:
        >> from BDD.choices import MARDI
        >> t = TypeCour.objects.get(id=2)
        >> s = SALLE.objects.get(id=1)
        >> l = Cour(typeCour=t, jour=MARDI, hmin=0, hmax=2, semaineMin=1, semaineMax=2)
        >> l.salles.add(s)
        >> l.save()
        save a lesson in the database 
    """
    
    typeCour = models.ForeignKey(TypeCour)
    salles = models.ManyToManyField(Salle, blank=True)
    uploadDate = models.DateTimeField(default=timezone.now())  # date de l'upload
    semaineMin = models.IntegerField()
    semaineMax = models.IntegerField()
    jour = models.IntegerField(choices=SEMAINE, default=LUNDI)
    hmin = models.IntegerField()
    hmax = models.IntegerField()
    def __str__ (self):
        return self.typeCour.nom

class News(models.Model):
    """
        It defines a news.
        
        It has a text, an upload date and 2 types of news (delete, add... and the kind of object)
        
        It is related to  persons (ManyToMany relation)
        
        :exemple:
        >> from BDD.choices import AJOUT, PERSONNESTATUT
        >> p = Personne.objects.get(id=2)
        >> l = News(txt="Welcome", type=PERSONNESTATUT, typeG=AJOUT)
        >> l.personne.add(p)
        >> l.save()
        save a lesson in the database (the upload date is automatic)
    """
    
    personne=models.ManyToManyField(Personne)
    txt=models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPENEWS, default=INCONNU_STATUT_TYPE)
    typeG= models.IntegerField(choices=TYPENEWSG, default=AJOUT)
    uploadDate = models.DateTimeField(default=timezone.now())  # date de l'upload
    def __str__ (self):
        return self.txt

    
     
    
    
