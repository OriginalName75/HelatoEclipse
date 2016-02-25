'''
Created on 30 oct. 2015

@author: mabadie_2
'''
from django.utils import timezone

from BDD import models
from BDD.choices import SALLESTATUT, \
    MODIFIER, SALLES, PERSONNESTATUT, TYPE, findchoice, SEXE, GROUPESTATUT,\
    UVSTATUT
from Functions.news import manytomany
from BDD.models import Groupe


####################### AJOUT #################
def modCourLive(idP, salles=None, typeCour=None, jour=None, semaineMin=None, semaineMax=None, hmin=None, hmax=None):
    c = models.Cour.objects.get(id=idP)
    if salles != None:
        c.salles = salles
    if typeCour != None:
        c.typeCour = typeCour
    if jour != None:
        c.jour = jour
    if semaineMin != None:
        c.semaineMin = semaineMin
    if semaineMax != None:
        c.semaineMax = semaineMax
    if hmin != None:
        c.hmin = hmin
    if hmax != None:
        c.hmax = hmax
    c.save()


########################### FIN AJOUT #######################

######################## mod ,""""""""""""""""""""""
def modGroupe(idP, p, nom=None, personnes=None, modules=None):
    
    ######################## fin mod ,""""""""""""""""""""""
    c = models.Groupe.objects.get(id=idP)
    txt="Vous avez modifié le groupe " + c.nom
    if nom != None and c.nom != nom:
        txt=txt + " à " + " "
        c.nom = nom
    else:
        txt=txt+". "
    ######################## mod ,""""""""""""""""""""""
    if modules != None and c.modules != modules:
        txt =manytomany(modules, txt, c, models.Module, "modules", "module", "le", False, attrafiche="nom")
        c.modules = modules
    ########################finmod ,""""""""""""""""""""""
    
    if personnes != None and c.personnes != personnes:
        txt =manytomany(personnes, txt, c, models.Personne, "personnes", "personne", "la", False, STATUT=GROUPESTATUT)
        c.personnes = personnes
    c.save()
    n = models.News()
    n.txt = txt
    n.typeG = MODIFIER
    n.type = GROUPESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)
    
####################### modifi� module #############################
def modModule(idP,p,  nom=None, uv=None, groupes=None):
   
####################### modifi� module #############################
    c = models.Module.objects.get(id=idP)
    txt=" Vous avez modifié le module " + c.nom
    if nom != None and c.nom!=nom:
        txt=txt + " en " + nom + ". "
        c.nom = nom
    else:
        txt=txt+". "
    ####################### modifi� module #############################
    if uv != None and c.uv != uv:
        txt=txt + " Le module n\'est plus dans " + c.uv.nom + " mais dans " + uv.nom +". "
        c.uv = uv
    if groupes != None:
        txt =manytomany(groupes, txt, c, models.Groupe, "groupe_set", "groupe", "au", True)
        c.groupe_set = groupes
    ####################### modifi� module #############################    
    c.save()
    n = models.News()
    
    n.txt = txt
    n.typeG = MODIFIER
    n.type = SALLESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)
def modNote(idP, note=None, personne=None, module=None):
    c = models.Note.objects.filter(id=idP)[0]
    if note != None:
        c.note = note
    if personne != None:
        c.personne = personne
    if module != None:
        c.module = module
    c.save()
def modCour(idP, nom=None, isExam=None, groupes=None, profs=None):
    c = models.TypeCour.objects.filter(id=idP)[0]
    if nom != None:
        c.nom = nom
    if isExam != None:
        c.isExam = isExam
    if groupes != None:
        c.groupe = groupes
    if profs != None:
        c.profs = profs
    c.save()
def modSalle(idP, p, nom=None, capacite=None, typee=None):
    txt = "Vous avez modifié " 
    i = 0
    c = models.Salle.objects.filter(id=idP)[0]
    if nom != None and c.nom != nom:
        txt = txt + "le nom de la salle " + c.nom + " en " + nom
        i = 1
        c.nom = nom
    if capacite != None and capacite != c.capacite:
        if i == 1:
            txt = txt + " et ça "
        else:
            txt=txt+ "la "
            
        if c.capacite != None:
            txt = txt + "capacité de " + str(c.capacite) + " à " + str(capacite)
        else:
            txt = txt + "capacité à " + str(capacite)
        if i == 0:
            txt = txt + " de la salle " + c.nom      
        c.capacite = capacite
        i=1
    if typee != None and int(typee)!=int(c.type):
        if i == 1:
            txt = txt + " et son "
        else:
            txt=txt+ "le ";
        txt = txt + "type de salle de " + str(c.get_type_display()) + " à " + str(SALLES[int(typee)][1])
        c.type = typee
    c.save()
    n = models.News()
    
    n.txt = txt
    n.typeG = MODIFIER
    n.type = SALLESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)
def modUV(idP, p, nom=None):
    c = models.UV.objects.get(id=idP)
    txt="Vous avez modifié le nom de l\'UV " + c.nom+ " en " + nom
    
    if nom != None and c.nom != nom:
        c.nom = nom
    c.save()
    n = models.News()
    
    n.txt = txt
    n.typeG = MODIFIER
    n.type = UVSTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)
def modPersonne(perso, idP, nom=None, prenom=None, login=None, mdp=None, sexe=None, typeP=None, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None, groupes=None):
    
    p = models.Personne.objects.filter(id=idP)[0]
    su=0
    txt="Vous avez changé la personne " + p.user.first_name + " " + p.user.last_name
    txt2="Votre profil à été changé :"
    if prenom != None and prenom!= "" and prenom!=p.user.first_name:
        su=1
        
        p.user.first_name = prenom
    if nom != None and nom != ""  and nom !=p.user.last_name:
        su=1
        p.user.last_name = nom
    if su==1:
        txt2=txt2+ " vous etes maintenant : "  + prenom + " " + nom+ ". "
        txt=txt + " en " + prenom + " " + nom
    txt=txt + ". "
    if groupes != None:
        txt, txt2=manytomany(groupes, txt, p, models.Groupe, "groupe_set", "groupe", "au", True, attrafiche="nom", txt2=txt2)
        p.groupe_set = groupes
    if login != None and login!="" and login!=p.user.username:
        txt = txt + " Son login a changé de " + p.user.username + " à " + login
        txt2 = txt2+ " Votre login a été changé de " + p.user.username + " à " + login
        p.user.username = login
    if mdp != None and p.user.password != login:
        txt = txt + " Son mot de passe a été changé "
        txt2 = txt2 + " Votre mot de passe a été changé "
        p.user.password = mdp
    
    p.filter = "{0} {1}".format(p.user.last_name, p.user.first_name)
    if email != None and p.user.email != email: 
        txt = txt + " Son email a changé de " + p.user.email + " à " + email
        txt2 = txt2 + " Votre email a été changé de " + p.user.email + " à " + email
        p.user.email = email
    p.user.save()    
    if typeP != None and int(typeP)!=int(p.type):   
        txt = txt + " Son statut a changé de " + str(p.get_type_display())   +  " à " + findchoice(typeP, TYPE)+ ". "
        txt2 = txt2 + " Votre statut a été changé de " + str(p.get_type_display())   +  " à " + findchoice(typeP, TYPE)+ ". "
        
        if int(typeP) == 3:
            p.user.is_superuser = True
        else:
            p.user.is_superuser = False    
        p.type = typeP
        
    if sexe != None and int(sexe)!=int(p.sexe):
        
        txt = txt + " Vous avez changé son sexe de " + str(p.get_sexe_display())   +  " à " + findchoice(sexe, SEXE) + ". "
        txt2 = txt2 + " Vous sexe a été changé (sur le site) de " + str(p.get_sexe_display())   +  " à " + findchoice(sexe, SEXE) + ". "
        
        p.sexe = sexe
   
    if adresse != None and adresse != "" and p.adresse != adresse:
        txt = txt + " Vous avez changé son adresse de " + p.adresse   +  " à " + adresse + ". "
        txt2 = txt2 + " Votre adresse a été changé de " + p.adresse   +  " à " + adresse + ". "
        
        p.adresse = adresse 
    if promotion != None and p.promotion != promotion:
        txt = txt + " Vous avez changé sa promotion de " + str(p.promotion)   +  " à " + str(promotion) + ". "
        txt2 = txt2 + " Votre promotion a changé de " + str(p.promotion)   +  " à " + str(promotion) + ". "
      
       
        p.promotion = promotion
    if dateDeNaissance != None and p.dateDeNaissance != dateDeNaissance:
        txt = txt + " Vous avez changé sa date de naissance de " + str(p.dateDeNaissance)   +  " à " + str(dateDeNaissance) + ". "
        txt2 = txt2 + " Votre date de naissance a été changé de " + str(p.dateDeNaissance)   +  " à " + str(dateDeNaissance) + ". "
        
        p.dateDeNaissance = dateDeNaissance
    if lieuDeNaissance != None and  p.lieuDeNaissance != lieuDeNaissance:
        txt = txt + " Vous avez changé son lieu de naissance de " + str(p.lieuDeNaissance)   +  " à " + str(lieuDeNaissance) + ". "
        txt2 = txt2 + " Votre lieu de naissance a été changé de " + str(p.lieuDeNaissance)   +  " à " + str(lieuDeNaissance) + ". "
        
        p.lieuDeNaissance = lieuDeNaissance
    if numeroDeTel != None and p.numeroDeTel != numeroDeTel:
        txt = txt + " Vous avez changé son numéro de " + str(p.numeroDeTel)   +  " à " + str(numeroDeTel) + ". "
        txt2 = txt2 + " Votre numéro a changé de " + str(p.numeroDeTel)   +  " à " + str(numeroDeTel) + ". "
 
        p.numeroDeTel = numeroDeTel
    
    p.save()
    if p!=perso:
        n = models.News()
        
        n.txt = txt
        n.typeG = MODIFIER
        n.type = PERSONNESTATUT
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(perso)
        
    n2 = models.News()
    
    n2.txt = txt2
    n2.typeG = MODIFIER
    n2.type = PERSONNESTATUT
    n2.uploadDate = timezone.now()   
    n2.save()
    n2.personne.add(p)

