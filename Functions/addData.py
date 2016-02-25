'''
Created on 25 oct. 2015

@author: Moran
'''
from django.contrib.auth.models import User
from django.utils import timezone

from BDD import models
from BDD.choices import PROF_STATUT, ADMINISTRATEUR_STATUT, SALLESTATUT, AJOUT, \
    SEXE, TYPE, PERSONNESTATUT, GROUPESTATUT, UVSTATUT, MODULESTATUT,\
    CALENDRIERSTATUT
from BDD.models import Personne, horaireProf, Cour, UV
from Functions.news import manytomany


def checkNaddPersonne(nom, prenom, login, mdp, sexe, typeP, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None, errors=None):
    if User.objects.filter(username=login).exists():
        errors[0] = "Login exixtse dja"
    else :
        addPersonne(nom, prenom, login, mdp, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, email)
   
def addPersonne(pers, nom, prenom, login, mdp, sexe, typeP, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None):
    txt="Vous avez ajouté " + prenom + " " + nom + " de login " + login + ", qui est " + str(SEXE[int(sexe)][1]) + " et qui est " + str(TYPE[int(typeP)][1]) +"."
    user = User.objects.create_user(username=login , password=mdp)
    user.first_name = prenom
    user.last_name = nom
    if email != "" and email!=None:
        txt= txt + " Son mail est " + str(email)
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
   
    if adresse != "" and adresse != None:
        p.adresse = adresse
        txt= txt + " Son adresse est " + adresse
    if promotion != None:
        p.promotion = promotion
        txt= txt + " Sa promotion est " + str(promotion)
    if dateDeNaissance != "" and dateDeNaissance != None:
        txt= txt + " Il/Elle est né(e) le " + str(dateDeNaissance)
        p.dateDeNaissance = dateDeNaissance
        
    if lieuDeNaissance != "" and lieuDeNaissance != None:
        txt= txt + " Il/Elle est né(e) à " + str(lieuDeNaissance)
        p.lieuDeNaissance = lieuDeNaissance
    if numeroDeTel != "" and numeroDeTel != None:
        txt= txt + " Son noméro est le " + str(numeroDeTel)
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
            
    n=models.News()
    n.txt=txt
    n.typeG=AJOUT
    n.type=PERSONNESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers)      
############################# modifi� ######################                   
def addCalendrier(pers, typeCour,jour,semaineMin,semaineMax,hmin,hmax,salles):
    
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
    
    n=models.News()
    n.txt="Vous avez ajouté un cour de " + typeCour.nom + "" #besion de lalgo de quentin
    n.typeG=AJOUT
    n.type=CALENDRIERSTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers) 
            
            
############################# fin modifi� ######################              
                     
############################# modifi� ######################        
def addGroupe(pers, nomm, personnes=None, modules=None):
############################# fin modifi� ######################  
    txt="Vous avez ajouté le groupe " + nomm + ". "
    c = models.Groupe()
    c.nom = nomm
    c.uploadDate = timezone.now()
    c.save()
    ############################# modifi� ######################   
    if (modules!=None):
        txt =manytomany(modules, txt, c, models.Module, "modules", "module", "au", False, attrafiche="nom")
        c.modules=modules
    ############################# fin modifi� ######################   
    
    
    if (personnes!=None):
        txt =manytomany(personnes, txt, c, models.Personne, "personnes", "personne", "à la", False, STATUT=GROUPESTATUT)
        c.personnes=personnes
    
    n=models.News()
    n.txt=txt
    n.typeG=AJOUT
    n.type=GROUPESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers) 
    
    
    
    return c.id
def addCour(nom, isExam=False):
   
    c = models.TypeCour()
    c.nom = nom
    c.isExam = isExam
    c.save()            
def addUV(pers, nom):
   
    c = models.UV()
    c.nom = nom
    c.save()
    n=models.News()
    n.txt="Vous avez ajouté l\'UV " + c.nom
    n.typeG=AJOUT
    n.type=UVSTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers) 
    return c.id
def addModule(pers, nom, uv=None):
    txt="Vous avez ajouté le module " + nom
    c = models.Module()
    c.nom = nom
    if uv!=None:
        
        txt=txt+ " dans l\'UV " + uv.nom
        c.uv = uv
    c.save()
    n=models.News()
    n.txt=txt
    n.typeG=AJOUT
    n.type=MODULESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers) 
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
    
### m ###   
def addSalle(pers, nom, capacite=None, typee=None):
### fm ###    
    c = models.Salle()
    c.nom = nom
    if typee != None:
        c.type = typee
    if capacite != None:
        c.capacite = capacite
    c.save()
    ### m ###     
    n=models.News()
    txt="Vous avez ajouté la salle " + nom
    
    if typee != None and int(typee)!=0:
        txt = txt + " de type " + str(c.get_type_display())
        if capacite != None:
            txt=txt+ " et"
    if capacite != None:
        txt=txt+ " de " + str(capacite) + " places"   
    n.txt=txt
    n.typeG=AJOUT
    n.type=SALLESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers)
    ### fm ###   
    
     
            
             
         
        
