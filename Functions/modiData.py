'''
Created on 30 oct. 2015

@author: mabadie_2
'''
from django.utils import timezone

from BDD import models
from BDD.choices import INCONNU_STATUT, INCONNU_STATUT_SALLE, SALLESTATUT, \
    MODIFIER, SALLES, PERSONNESTATUT, TYPE, findchoice, SEXE


####################### AJOUT #################
def modCourLive(idP, salles=None, typeCour=None, jour=None, semaineMin=None, semaineMax=None, hmin=None, hmax=None):
    c = models.Cour.objects.filter(id=idP)[0]
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
####################### modifi� module #############################
def modModule(idP, nom=None, uv=None, groupes=None):
####################### modifi� module #############################
    c = models.Module.objects.filter(id=idP)[0]
    if nom != None:
        c.nom = nom
    ####################### modifi� module #############################
    if uv != None:
        c.uv = uv
    if groupes != None:
        
        c.groupe_set = groupes
    ####################### modifi� module #############################    
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
def modUV(idP, nom=None):
    c = models.UV.objects.filter(id=idP)[0]
    if nom != None:
        c.nom = nom
    c.save()
def modPersonne(perso, idP, nom=None, prenom=None, login=None, mdp=None, sexe=None, typeP=None, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None, groupes=None):
    
    p = models.Personne.objects.filter(id=idP)[0]
    su=0
    txt="Vous avez changé " + p.user.first_name + " " + p.user.last_name
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
        l=[]
        for g in groupes:
            found=False
            for u in p.groupe_set.all():
                if u.id==int(g):
                    found=True
                    
                    break
            if not found:
                l.append(g)
        l2=[]
        for g in p.groupe_set.all():
            found=False
            for u in groupes:
                if g.id==int(u):
                    found=True
                    
                    break
            if not found:
                l2.append(g)
        if len(l)>2:
            txt= txt + ". Vous l\'avez ajouté à " + str(len(l)) + " groupes. " 
            txt2= txt2 + ". Vous avez été ajouté à " + str(len(l)) + " groupes. "     
        elif len(l)>0:
            txt = txt + " Vous l\'avez ajouté "
            txt2 = txt2 + " Vous avez été ajouté "
            first=True
            for ggg in l:
                if not first:
                    txt = txt + " et " 
                    txt2 = txt2 + " et " 
                txt= txt + " au groupe " + models.Groupe.objects.get(id=int(ggg)).nom + " "
                txt2= txt2 + " au groupe " + models.Groupe.objects.get(id=int(ggg)).nom + " "
                first=False
        if len(l2)>2:
            txt= txt + ". Vous l\'avez enlevé à " + str(len(l)) + " groupes. "   
            txt2= txt2 + ". Vous avez été enlevé à " + str(len(l)) + " groupes. " 
        elif len(l2)>0:
            txt = txt + " Vous l\'avez enlevé "
            txt2 = txt2 + " Vous avez été enlevé "
            first=True
            for ggg in l2:
                if not first:
                    txt = txt + " et " 
                    txt2 = txt2 + " et " 
                txt= txt + " au groupe " + ggg.nom + " "
                txt2= txt2 + " au groupe " + ggg.nom + " "
                first=False    
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

