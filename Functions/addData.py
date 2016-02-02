'''
Created on 25 oct. 2015

@author: Moran
'''
from django.contrib.auth.models import User
from django.utils import timezone

from BDD import models
from BDD.choices import PROF_STATUT, ADMINISTRATEUR_STATUT
from BDD.models import Personne, horaireProf, Cour


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
        #### change###
        user.has_perm("BDD.add_note")
        user.has_perm("BDD.change_note")
        user.has_perm("BDD.delete_note")
        user.is_staff=True
        ### fin ##"
    if typeP == ADMINISTRATEUR_STATUT:
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
    stri = "{0} {1}".format(p.user.last_name, p.user.first_name)
    if Personne.objects.filter(filter=stri).count() > 0:
        stri = stri + " de " + lieuDeNaissance
    if Personne.objects.filter(filter=stri).count() > 0:
        stri = stri + " du " + p.dateDeNaissance.strftime("%d/%m/%y")
    i = 1
    strbase = stri
    while (Personne.objects.filter(filter=stri).count() > 0):
        stri = strbase + i
        i = i + 1
        
        
        
    p.filter = stri
    p.uploadDate = timezone.now()
    p.save()
    
    if typeP == PROF_STATUT:
        
        for ii in range(0, 5):
            
            h = horaireProf()
            h.prof = p
            h.jdelaSemaine = ii
            h.hminApresMidi = 5
            h.hmaxApresMidi = 8
            h.hminMatin = 1
            h.hmaxMatin = 3
            h.save()     
            
            
############################# modifi� ######################                   
def addCalendrier(typeCour,jour,semaineMin,semaineMax,hmin,hmax,salles):
    c = Cour()
    c.typeCour = typeCour
    c.jour = jour
    
    c.uploadDate = timezone.now()
    c.semaineMin = semaineMin
    c.semaineMax = semaineMax
    c.hmin = hmin
    c.hmax = hmax
    c.save()
    c.salles=salles
    
            
            
            
############################# fin modifi� ######################              
                     
############################# modifi� ######################        
def addGroupe(nomm, personnes=None, modules=None):
############################# fin modifi� ######################  
    c = models.Groupe()
    c.nom = nomm
    c.uploadDate = timezone.now()
    c.save()
    ############################# modifi� ######################   
    if (modules!=None):
        c.modules=modules
    ############################# fin modifi� ######################   
    
    
    if (personnes!=None):
        c.personnes=personnes
    
    return c.id
def addCour(nom, isExam=False):
   
    c = models.TypeCour()
    c.nom = nom
    c.isExam = isExam
    c.save()            
def addUV(nom):
   
    c = models.UV()
    c.nom = nom
    c.save()
    return c.id
def addModule(nom, uv=None):
   
    c = models.Module()
    c.nom = nom
    c.uv = uv
    c.save()
    ############################# modifi� ######################      
def addNote(note, personne, module, prof):
    
    c = models.Note()
    c.note = note
    c.personne = personne
    c.module = module
    c.uploadDate = timezone.now()
    c.prof=prof
    c.save()
    
    
############################# fin modifi� ######################      
    
    
def addSalle(nom, capacite=None, typee=None):
   
    c = models.Salle()
    c.nom = nom
    if typee != None:
        c.type = typee
    if capacite != None:
        c.capacite = capacite
    c.save()    
     
            
             
         
        
