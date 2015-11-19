'''
Created on 25 oct. 2015

@author: Moran
'''
from django.contrib.auth.models import User
from django.utils import timezone

from BDD import models


def checkNaddPersonne(nom, prenom, login, mdp, sexe, typeP, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None, errors=None):
    if User.objects.filter(username=login).exists():
        errors[0] = "Login exixtse dja"
    else :
        addPersonne(nom, prenom, login, mdp, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, email)
   
def addPersonne(nom, prenom, login, mdp, sexe, typeP, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None):
   
    user = User.objects.create_user(username=login , password=mdp)
    user.first_name = prenom
    user.last_name = nom
    if email != None:
        user.email = email
    if int(typeP) == 3:
        user.is_superuser = True
    user.save()
    p = models.Personne()
    p.user = user
    p.type = typeP
    
    p.sexe = sexe
   
    if adresse != None:
        p.adresse = adresse
    if promotion != None:
        p.promotion = promotion
    if dateDeNaissance != None:
        p.dateDeNaissance = dateDeNaissance
    if lieuDeNaissance != None:
        p.lieuDeNaissance = lieuDeNaissance
    if numeroDeTel != None:
        p.numeroDeTel = numeroDeTel
    
    p.uploadDate = timezone.now()
    p.save()
            
        
def addGroupe(nomm):
   
    c = models.Groupe()
    c.nom = nomm
   
    
    c.uploadDate = timezone.now()
    c.save()
    
    return c.id
def addCour(nom, isExam=False):
   
    c = models.Cour()
    c.nom = nom
    c.isExam = isExam
    c.uploadDate = timezone.now()
    c.save()            
def addUV(nom):
   
    c = models.UV()
    c.nom = nom
    c.save()
def addModule(nom, uv=None):
   
    c = models.Module()
    c.nom = nom
    c.uv = uv
    c.save()
def addNote(note, personne, module):
   
    c = models.Note()
    c.note = note
    c.personne = personne
    c.module = module
    c.uploadDate = timezone.now()
    c.save()
def addSalle(nom, capacite=None, type=None):
   
    c = models.Salle()
    c.nom = nom
    if type != None:
        c.type = type
    if capacite != None:
        c.capacite = capacite
    c.save()           
def newYear(an):
    a = models.Annee()
    a.annee = an
    a.save()
    MOIS = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
    j = 1
    for i in range(1, 13):
        m = models.Moi()
        m.nom = MOIS[i - 1]
        m.nbMoi = i
        m.annee = a
        m.save()
        for k in range(1, 5):
            s = models.Semaine()
            s.semaine = j
            s.moi = m
            s.save()
            j = j + 1
            
         
        
