"""
    The ''modiData'' module
    ======================
    
    It define the functions to modify objects in the database.
    It takes care of news and saves (for ctrl-z) 
    
    
    :Exemple:
    
    >> modGroupe(3, request.user.personne, "MPSI 2"):
    modify the name's group which id is 3
    
    
@author: IWIMBDSL
"""
from django.utils import timezone

from BDD import models
from BDD.choices import SALLESTATUT, \
    MODIFIER, SALLES, PERSONNESTATUT, TYPE, findchoice, SEXE, GROUPESTATUT, \
    UVSTATUT, SEMAINE, CALENDRIERSTATUT, NOTESTATUT
from Functions.news import manytomany


def modCourLive(idP, pers, salles=None, typeCour=None, jour=None, semaineMin=None, semaineMax=None, hmin=None, hmax=None):
    """
        Modify an lesson
        
    :param idP: id of the lesson
    :type idP: int
    :param pers: the user who wants to modify the object
    :type pers: Personne
    :param salles: the lesson classroom(s)
    :type salles: List of Salle
    :param typeCour: which type of lesson
    :type typeCour: typeCour
    :param jour: Day of the lesson
    :type jour: list of Tuple
    :param semaineMin: first week of the lesson
    :type semaineMin: int
    :param semaineMax: last week of the lesson
    :type semaineMax: int
    :param hmin: first hour of the lesson
    :type hmin: int 
    :param hmax: last hour of the lesson
    :type hmax: int
    
    :exemple:
    
    >> from BDD.choices import MARDI
    >> modCourLive(3, request.user.personne, jour=MARDI)
    change the day of the lesson which id=3 
    
    """
    
    c = models.Cour.objects.get(id=idP)
    if typeCour != None and c.typeCour.id != typeCour.id :
       
        txt = "Vous avez modifié un cour de " + c.typeCour.nom + " en un cour de " + typeCour.nom + ". "
        c.typeCour = typeCour
        
    else:
        txt = "Vous avez modifié un cour de " + c.typeCour.nom + ". "
    if salles != None and c.salles != salles:
        txt = manytomany(salles, txt, c, models.Salle, "salles", "salle", "la", False)
        c.salles = salles
    
    if jour != None and c.jour != jour:
        txt = txt + "Vous avez modifié son jour de " + c.get_jour_display() + " à " + str(findchoice(int(jour), SEMAINE))
        c.jour = jour
    if semaineMin != None and c.semaineMin != semaineMin:
        txt = txt + "Vous avez modifié sa première semaine de " + str(c.semaineMin) + " à " + str(semaineMin)
        c.semaineMin = semaineMin
    if semaineMax != None and c.semaineMax != semaineMax:
        txt = txt + "Vous avez modifié sa dernière semaine de " + str(c.semaineMax) + " à " + str(semaineMax)
        c.semaineMax = semaineMax
    if hmin != None and c.hmin != hmin:
        txt = txt + "Vous avez modifié sa première heure de " + str(c.hmin) + " à " + str(hmin)
        c.hmin = hmin
    if hmax != None and c.hmax != hmax:
        txt = txt + "Vous avez modifié sa dernière heure de " + str(c.hmax) + " à " + str(hmax)
        c.hmax = hmax
    c.save()
    
    
    n = models.News()
    n.txt = txt
    n.typeG = MODIFIER
    n.type = CALENDRIERSTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers)

def modGroupe(idP, p, nom=None, personnes=None, modules=None):
    """
        modify a group in the database
    
    :param idP: id of the group to modify
    :type idP: int
    :param p: the user who wants to modify the group
    :type p: Personne
    :param nom: name of the group
    :type nom: string
    :param personnes: persons in the group
    :type personnes: list of Personne
    :param modules:  which module the group is marked
    :type modules: list of Module
    
    :exemples:
    
    >> modGroupe(3, request.user.personne, nom="MP")
    change the name of the group which id = 3
    
    >> m = Module.objects.filter(id=1) # it must be a list that is why it is a filter and not a get
    >> modGroupe(3, request.user.personne, modules=m)
    change the group in the database whit new modules
    
    """
    c = models.Groupe.objects.get(id=idP)
    txt = "Vous avez modifié le groupe " + c.nom
    if nom != None and c.nom != nom:
        txt = txt + " à " + " "
        c.nom = nom
    else:
        txt = txt + ". "
    ######################## mod ,""""""""""""""""""""""
    if modules != None and c.modules != modules:
        txt = manytomany(modules, txt, c, models.Module, "modules", "module", "le", False, attrafiche="nom")
        c.modules = modules
    ########################finmod ,""""""""""""""""""""""
    
    if personnes != None and c.personnes != personnes:
        txt = manytomany(personnes, txt, c, models.Personne, "personnes", "personne", "la", False, STATUT=GROUPESTATUT)
        c.personnes = personnes
    c.save()
    n = models.News()
    n.txt = txt
    n.typeG = MODIFIER
    n.type = GROUPESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)
    

def modModule(idP, p, nom=None, uv=None, groupes=None):
    """
        modify a module in he database
        
    :param idP: id of the module to modify
    :type idP: int   
    :param p: the user who wants to modify the object
    :type p: Personne
    :param nom: name of the module
    :type nom: string
    :param uv: uv of the module
    :type uv: UV
    :param groupes: groups related to the module
    :type groupes: list of Groupe
    
    :exemple:
    
    >> uv= UV.objects.get(id=3)
    >> modModule(3, request.user.personne, uv=uv)
    modify a module's UV in the database
    
    """

    c = models.Module.objects.get(id=idP)
    txt = " Vous avez modifié le module " + c.nom
    if nom != None and c.nom != nom:
        txt = txt + " en " + nom + ". "
        c.nom = nom
    else:
        txt = txt + ". "
    ####################### modifi� module #############################
    if uv != None and c.uv != uv:
        txt = txt + " Le module n\'est plus dans " + c.uv.nom + " mais dans " + uv.nom + ". "
        c.uv = uv
    if groupes != None:
        txt = manytomany(groupes, txt, c, models.Groupe, "groupe_set", "groupe", "au", True)
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
def modNote(idP, p, note=None, personne=None, module=None, prof=None):
    """
        modify a mark in the database
        
    :param idP: id of the mark to modify
    :type idP: int
    :param p: the user who wants to modify the object
    :type p: Personne
    :param note: the mark
    :type note: int
    :param personne: person which is marked
    :type personne: Personne
    :param module: module which ithe person is marked
    :type module: Module
    :param prof: teacher who has marked the person
    :type prof: Personne
    
    :exemple:
    
    >> p= Personne.objects.get(id=1)
    >> modNote(3, request.user.personne, prof=p)
    modify a mark in the database
    
    """
    c = models.Note.objects.get(id=idP)
    txt = "Vous avez modifié une note"
    txt3 = None
    if personne != None and c.personne != personne:
        txt = txt + " qui n\'est plus celle de" + c.personne.filter + " mais celle de " + personne.filter + ". "
        txt2 = ""
        txt3 = c.personne
        c.personne = personne
        
    else:
        txt2 = "Une de votre note a été modifié."
        txt = txt + " de " + personne.filter + ". "
    if note != None and c.note != note:
        stri = "La note n\'est plus de " + str(c.note) + " mais de " + str(note) + ". "
        txt = txt + stri
        txt2 = txt2 + stri
        c.note = note
    
    if module != None and c.module != module:
        stri="Le module noté n\'est plus celui de " + str(c.module) + " mais de " + str(module) + ". "
        txt2 = txt2 + stri
        txt = txt + stri
        c.module = module
    if prof != None and c.prof != prof:
        stri = "Le prof qui note n\'est plus " + str(c.prof) + " mais " + str(prof) + ". "
        txt = txt + stri
        txt2 = txt2 + stri
        c.prof = prof
    c.save()
    
    n = models.News()
    
    n.txt = txt
    n.typeG = MODIFIER
    n.type = NOTESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)
    if txt3==None:
        n2 = models.News()
        n2.txt = txt2
        n2.typeG = MODIFIER
        n2.type = SALLESTATUT
        n2.uploadDate = timezone.now()   
        n2.save()
        n2.personne.add(personne)
    else:
        n2 = models.News()
        n2.txt = "Une de vos note a été suprimmé"
        n2.typeG = MODIFIER
        n2.type = SALLESTATUT
        n2.uploadDate = timezone.now()   
        n2.save()
        n2.personne.add(txt3)
        
        n3 = models.News()
        n3.txt = "Vous avez une nouvelle note : " + str(c.note) + " au module " + str(c.module)
        n3.typeG = MODIFIER
        n3.type = SALLESTATUT
        n3.uploadDate = timezone.now()   
        n3.save()
        n3.personne.add(personne)
        
        
    
def modCour(idP, p, nom=None, isExam=None, groupes=None, profs=None):
    """
       Modify a type of lesson in the database
    
    :param idP: id of the type of lesson to modify
    :type idP: int
    :param p: the user who wants to modify the object
    :type p: Personne
    :param nom: name of the type of lesson
    :type nom: string
    :param isExam: is it aan exam ?
    :type isExam: boolean
    :param profs: the teacher(s) of the type of lesson
    :type profs: List of Personne
    :param groupes: the groupe(s) in the type of lesson
    :type groupes: List of groups
    
    :exemple:
    
    >> modCour(3, request.user.personne, nom="Sport")
    change a type of lesson in the database
    
    
    """
    
    c = models.TypeCour.objects.filter(id=idP)[0]
    txt = "Vous avez modifié le type de cour " + c.nom
    if nom != None and c.nom != nom:
        txt = txt + " en " + nom 
        c.nom = nom
    txt = txt + ". "
    if isExam != None and c.isExam != isExam:
        if c.isExam:
            txt = txt + "Ce n\'est plus un exam. "
        else:
            txt = txt + "C\'est maintenant un exam. "
        c.isExam = isExam
    if groupes != None and c.groupe != groupes:
        txt = manytomany(groupes, txt, c, models.Groupe, "groupe", "groupe", "au", False)
        c.groupe = groupes
    if profs != None and c.profs != profs:
        txt = manytomany(profs, txt, c, models.Personne, "profs", "prof", "le", False)
        c.profs = profs
    c.save()
    n = models.News()
    
    n.txt = txt
    n.typeG = MODIFIER
    n.type = SALLESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)
    
def modSalle(idP, p, nom=None, capacite=None, typee=None):
    """
        modify a classroom in the database
    
    :param idP: id of the classroom to modify
    :type idP: int    
    :param pers: the user who wants to modify the object
    :type pers: Personne
    :param nom: name of the classroom
    :type nom: string
    :param capacite: capacity of the classroom
    :type capacite: int
    :param typee: which type of classroom (labo etc...)
    :type typee: list of tuple
    
    :exemple:
    
    >> from BDD.choices import INFO_STATUT
    >> modSalle(3, request.user.personne, typee=INFO_STATUT)
    modify a classroom in the database
    
    """
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
            txt = txt + "la "
            
        if c.capacite != None:
            txt = txt + "capacité de " + str(c.capacite) + " à " + str(capacite)
        else:
            txt = txt + "capacité à " + str(capacite)
        if i == 0:
            txt = txt + " de la salle " + c.nom      
        c.capacite = capacite
        i = 1
    if typee != None and int(typee) != int(c.type):
        if i == 1:
            txt = txt + " et son "
        else:
            txt = txt + "le ";
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
    """
        Modify an UV in the database
    
    :param idP: id of the UV to modify
    :type idP: int   
    :param p: the user who wants to modify the object
    :type p: Personne
    :param nom: name of the UV
    :type nom: string
    
    :exemples:
    
    >> modUV(3, request.user.personne, nom="2.9")
    modify an UV in the database
    
    """
    c = models.UV.objects.get(id=idP)
    txt = "Vous avez modifié le nom de l\'UV " + c.nom + " en " + nom
    
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
    """
        Modify a person in the database
    
    :param idP: id of the person to modify
    :type idP: int      
    :param pers: the user who wants to modify the object
    :type pers: Personne
    :param nom: last name of the person
    :type nom: string
    :param prenom: first name of the person
    :type prenom: string
    :param login: username of the person
    :type login: string
    :param mdp: password of the person
    :type mdp: string
    :param sexe: sex of the person
    :type sexe: list of tuple
    :param typeP: if the person is a student, a teacher etc...
    :type typeP: list of tuple
    :param adresse: the address of the person
    :type adresse: string
    :param promotion: year of the person promotion
    :type promotion: int
    :param dateDeNaissance: date of birth
    :type dateDeNaissance: python date
    :param lieuDeNaissance: place of birth
    :type lieuDeNaissance: string
    :param numeroDeTel: phone number
    :type numeroDeTel: string
    :param email: email of the person
    :type email: Django email or string
    
    :exemple:
    
    >> from BDD.choices import HOMME_STATUT, ELEVE_STATUT
    >> modPersonne(request.user.personne, sexe=HOMME_STATUT, typeP=ELEVE_STATUT)
    modify a person in the database
    
    """
    p = models.Personne.objects.filter(id=idP)[0]
    su = 0
    txt = "Vous avez changé la personne " + p.user.first_name + " " + p.user.last_name
    txt2 = "Votre profil à été changé :"
    if prenom != None and prenom != "" and prenom != p.user.first_name:
        su = 1
        
        p.user.first_name = prenom
    if nom != None and nom != ""  and nom != p.user.last_name:
        su = 1
        p.user.last_name = nom
    if su == 1:
        txt2 = txt2 + " vous etes maintenant : " + prenom + " " + nom + ". "
        txt = txt + " en " + prenom + " " + nom
    txt = txt + ". "
    if groupes != None:
        txt, txt2 = manytomany(groupes, txt, p, models.Groupe, "groupe_set", "groupe", "au", True, attrafiche="nom", txt2=txt2)
        p.groupe_set = groupes
    if login != None and login != "" and login != p.user.username:
        txt = txt + " Son login a changé de " + p.user.username + " à " + login
        txt2 = txt2 + " Votre login a été changé de " + p.user.username + " à " + login
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
    if typeP != None and int(typeP) != int(p.type):   
        txt = txt + " Son statut a changé de " + str(p.get_type_display()) + " à " + findchoice(typeP, TYPE) + ". "
        txt2 = txt2 + " Votre statut a été changé de " + str(p.get_type_display()) + " à " + findchoice(typeP, TYPE) + ". "
        
        if int(typeP) == 3:
            p.user.is_superuser = True
        else:
            p.user.is_superuser = False    
        p.type = typeP
        
    if sexe != None and int(sexe) != int(p.sexe):
        
        txt = txt + " Vous avez changé son sexe de " + str(p.get_sexe_display()) + " à " + findchoice(sexe, SEXE) + ". "
        txt2 = txt2 + " Vous sexe a été changé (sur le site) de " + str(p.get_sexe_display()) + " à " + findchoice(sexe, SEXE) + ". "
        
        p.sexe = sexe
   
    if adresse != None and adresse != "" and p.adresse != adresse:
        txt = txt + " Vous avez changé son adresse de " + p.adresse + " à " + adresse + ". "
        txt2 = txt2 + " Votre adresse a été changé de " + p.adresse + " à " + adresse + ". "
        
        p.adresse = adresse 
    if promotion != None and p.promotion != promotion:
        txt = txt + " Vous avez changé sa promotion de " + str(p.promotion) + " à " + str(promotion) + ". "
        txt2 = txt2 + " Votre promotion a changé de " + str(p.promotion) + " à " + str(promotion) + ". "
      
       
        p.promotion = promotion
    if dateDeNaissance != None and p.dateDeNaissance != dateDeNaissance:
        txt = txt + " Vous avez changé sa date de naissance de " + str(p.dateDeNaissance) + " à " + str(dateDeNaissance) + ". "
        txt2 = txt2 + " Votre date de naissance a été changé de " + str(p.dateDeNaissance) + " à " + str(dateDeNaissance) + ". "
        
        p.dateDeNaissance = dateDeNaissance
    if lieuDeNaissance != None and  p.lieuDeNaissance != lieuDeNaissance:
        txt = txt + " Vous avez changé son lieu de naissance de " + str(p.lieuDeNaissance) + " à " + str(lieuDeNaissance) + ". "
        txt2 = txt2 + " Votre lieu de naissance a été changé de " + str(p.lieuDeNaissance) + " à " + str(lieuDeNaissance) + ". "
        
        p.lieuDeNaissance = lieuDeNaissance
    if numeroDeTel != None and p.numeroDeTel != numeroDeTel:
        txt = txt + " Vous avez changé son numéro de " + str(p.numeroDeTel) + " à " + str(numeroDeTel) + ". "
        txt2 = txt2 + " Votre numéro a changé de " + str(p.numeroDeTel) + " à " + str(numeroDeTel) + ". "
 
        p.numeroDeTel = numeroDeTel
    
    p.save()
    if p != perso:
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

