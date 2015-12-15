'''
Created on 30 oct. 2015

@author: mabadie_2
'''
from BDD import models
from BDD.choices import INCONNU_STATUT, INCONNU_STATUT_SALLE

######################## mod ,""""""""""""""""""""""
def modGroupe(idP, nom=None, personnes=None, modules=None):
    ######################## fin mod ,""""""""""""""""""""""
    c = models.Groupe.objects.filter(id=idP)[0]
    ######################## mod ,""""""""""""""""""""""
    if modules != None:
        c.modules = modules
    ########################finmod ,""""""""""""""""""""""
    if nom != None:
        c.nom = nom
    if personnes != None:
        c.personnes = personnes
    c.save()
####################### modifié module #############################
def modModule(idP, nom=None, uv=None, groupes=None):
####################### modifié module #############################
    c = models.Module.objects.filter(id=idP)[0]
    if nom != None:
        c.nom = nom
    ####################### modifié module #############################
    if uv != None:
        c.uv = uv
    if groupes != None:
        
        c.groupe_set = groupes
    ####################### modifié module #############################    
    c.save()
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
def modSalle(idP, nom=None, capacite=None, typee=None):
    c = models.Salle.objects.filter(id=idP)[0]
    if nom != None:
        c.nom = nom
    if capacite != None:
        c.capacite = capacite
    if typee != INCONNU_STATUT_SALLE:
        
        c.type = typee
    c.save()
def modUV(idP, nom=None):
    c = models.UV.objects.filter(id=idP)[0]
    if nom != None:
        c.nom = nom
    c.save()
def modPersonne(idP, nom=None, prenom=None, login=None, mdp=None, sexe=None, typeP=None, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None, groupes=None):
    p = models.Personne.objects.filter(id=idP)[0]
    if groupes != None:
        p.groupe_set = groupes
    if login != None:
        p.user.username = login
    if mdp != None:
        p.user.password = login
    if prenom != None:
        p.user.first_name = prenom
    if nom != None:
        p.user.last_name = nom
    p.filter = "{0} {1}".format(p.user.last_name, p.user.first_name)
    if email != None:
        p.user.email = email
    p.user.save()    
    if typeP != None:
        if int(typeP) == 3:
            p.user.is_superuser = True
            
        p.type = typeP
    if sexe != None:
        if sexe != INCONNU_STATUT:
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
    
    p.save()
    
