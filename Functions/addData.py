"""
    The ''addData'' module
    ======================
    
    It define the functions to add objects in the database.
    It takes care of news and saves ( for ctrl-z) 
    
    :Exemple:
    >> addGroupe(request.user.personne, "MPSI 1")
    add the group MPSI 1 in the database.
    The user who added the data (request.user.personne) must be specified
     
@author: IWIMBDSL
"""

from _ast import Module
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from BDD import models
from BDD.choices import PROF_STATUT, ADMINISTRATEUR_STATUT, SALLESTATUT, AJOUT, \
    SEXE, TYPE, PERSONNESTATUT, GROUPESTATUT, UVSTATUT, MODULESTATUT, \
    CALENDRIERSTATUT, COURTYPESTATUT, NOTESTATUT
from BDD.models import Personne, horaireProf, Cour, Groupe, TypeCour, UV, Salle
from Functions.news import manytomany, day2


def addPersonne(pers, nom, prenom, login, mdp, sexe, typeP, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None):
    """
        Add a person in the database
        
        :param pers: the user who wants to add the object
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
        
        :example:
        >> from BDD.choices import HOMME_STATUT, ELEVE_STATUT
        >> addPersonne(request.user.personne, "Davis", "Miles", "godofjazz", "123456", HOMME_STATUT, ELEVE_STATUT)
        save a person in the database
    """
    
    txt = "Vous avez ajouté " + prenom + " " + nom + " de login " + login + ", qui est " + str(SEXE[int(sexe)][1]) + " et qui est " + str(TYPE[int(typeP)][1]) + "."
    
    user = User.objects.create_user(username=login , password=mdp)
    user.first_name = prenom
    user.last_name = nom
    if email != "" and email != None:
        txt = txt + " Son mail est " + str(email)
        user.email = email
        user.has_perm("BDD.add_note")
        user.has_perm("BDD.change_note")
        user.has_perm("BDD.delete_note")
        user.is_staff = True
    if typeP == ADMINISTRATEUR_STATUT:
        user.is_superuser = True
    user.save()
    
    p = models.Personne()
    p.user = user
    p.type = typeP
    p.sexe = sexe
    if adresse != "" and adresse != None:
        p.adresse = adresse
        txt = txt + " Son adresse est " + adresse
    if promotion != None:
        p.promotion = promotion
        txt = txt + " Sa promotion est " + str(promotion)
    if dateDeNaissance != "" and dateDeNaissance != None:
        txt = txt + " Il/Elle est né(e) le " + str(dateDeNaissance)
        p.dateDeNaissance = dateDeNaissance
    if lieuDeNaissance != "" and lieuDeNaissance != None:
        txt = txt + " Il/Elle est né(e) à " + str(lieuDeNaissance)
        p.lieuDeNaissance = lieuDeNaissance
    if numeroDeTel != "" and numeroDeTel != None:
        txt = txt + " Son noméro est le " + str(numeroDeTel)
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
    
    mod = models.Modification()
    mod.datemodif = timezone.now()
    mod.typetable = 'Personne'
    mod.typemod = AJOUT
    mod.ipmod = p.id
    mod.save()
    cm1 = models.ChampsModifie()
    cm1.champs = mod
    cm1.nomchamp = 'Identité'
    cm1.valchamp = nom+' '+prenom
    cm1.save()
    cm2 = models.ChampsModifie()
    cm2.champs = mod
    cm2.nomchamp = 'Date d\'upload'
    cm2.valchamp = p.uploadDate
    cm2.save()
    
    n = models.News()
    n.txt = txt
    n.typeG = AJOUT
    n.type = PERSONNESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers)      
                 
def addCalendrier(pers, typeCour, jour, semaineMin, semaineMax, hmin, hmax, salles):
    """
        add a lesson in the database
        
        :param pers: the user who wants to add the object
        :type pers: Personne
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
        :param salles: the lesson classroom(s)
        :type salles: List of Salle
        
        :example:
        >> from BDD.choices import MARDI
        >> t = TypeCour.objects.get(id=2)
        >> s = SALLE.objects.filter(id=1) # it must be a list that is why it is a filter and not a get
        >> addCalendrier(request.user.personne, t, MARDI,0,1,0,A, s)
        save a lesson in the database
    """
    
    c = Cour()
    c.typeCour = typeCour
    c.jour = jour
    c.uploadDate = timezone.now()
    c.semaineMin = semaineMin
    c.semaineMax = semaineMax
    c.hmin = hmin
    c.hmax = hmax
    c.salles = salles
    c.save()
    
    mod = models.Modification()
    mod.datemodif = timezone.now()
    mod.typetable = 'TypeCour'
    mod.typemod = AJOUT
    mod.ipmod = c.id
    mod.save()
    cm1 = models.ChampsModifie()
    cm1.champs = mod
    cm1.nomchamp = 'Jour'
    cm1.valchamp = jour
    cm1.save()
    cm2 = models.ChampsModifie()
    cm2.champs = mod
    cm2.nomchamp = 'Date d\'upload'
    cm2.valchamp = c.uploadDate
    cm2.save()
    cm3 = models.ChampsModifie()
    cm3.champs = mod
    cm3.nomchamp = 'Semaines'
    cm3.valchamp = 'De la semaine '+str(semaineMin)+' à la semaine '+str(semaineMax)
    cm3.save()
    cm4 = models.ChampsModifie()
    cm4.champs = mod
    cm4.nomchamp = 'Heures'
    cm4.valchamp = 'De l\H'+hmin+' à l\H'+hmax
    cm4.save()
    cm5 = models.ChampsModifie()
    cm5.champs = mod
    cm5.nomchamp = 'Salles du cour '
    a = ''
    for p in c.salles.all():
        a = a+str(p)+' '
    cm5.valchamp = a
    cm5.save()
    cm6 = models.ChampsModifie()
    cm6.champs = mod
    cm6.nomchamp = 'Type de cour'
    cm6.valchamp = typeCour
    cm6.save()
    
    d=datetime.datetime.now()
    n = models.News()
    if semaineMin < semaineMax:
        n.txt = "Vous avez ajouté un cour de " + typeCour.nom + " du " + day2(d.year,semaineMin,jour).strftime('%d/%m/%Y') + " au " + day2(d.year,semaineMax,jour).strftime('%d/%m/%Y') + " de l\'heure " + str(hmin) + " jusqu\'a " + str(hmax)  
    else:
        n.txt = "Vous avez ajouté un cour de " + typeCour.nom + " le " + day2(d.year,semaineMin,jour).strftime('%d/%m/%Y') + " de l\'heure " + str(hmin) + " jusqu\'a " + str(hmax)  
    n.typeG = AJOUT
    n.type = CALENDRIERSTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers) 

def addGroupe(pers, nomm, personnes=None, modules=None):
    """
        Add a group in the database
        
        :param pers: the user who wants to add the object
        :type pers: Personne
        :param nomm: name of the group
        :type nomm: string
        :param personnes: persons in the group
        :type personnes: list of Personne
        :param modules:  which module the group is marked
        :type modules: list of Module
        
        :examples:
        >> addGroupe(request.user.personne, "MP")
        save a group in the database
        
        >> m = Module.objects.filter(id=1) # it must be a list that is why it is a filter and not a get
        >> addGroupe(request.user.personne, "MP", modules=m)
        save a group in the database whit modules
    """
    
    i=Groupe.objects.filter(nom=nomm).count()
    if i==0:
        txt = "Vous avez ajouté le groupe " + nomm + ". "
        c = models.Groupe()
        c.nom = nomm
        c.uploadDate = timezone.now()
        if (modules != None):
            txt = manytomany(modules, txt, c, models.Module, "modules", "module", "au", False, attrafiche="nom")
            c.modules = modules
        if (personnes != None):
            txt = manytomany(personnes, txt, c, models.Personne, "personnes", "personne", "à la", False, STATUT=GROUPESTATUT)
            c.personnes = personnes
        c.save()
        
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'Groupe'
        mod.typemod = AJOUT
        mod.ipmod = c.id
        mod.save()
        cm1 = models.ChampsModifie()
        cm1.champs = mod
        cm1.nomchamp = 'nom'
        cm1.valchamp = nomm
        cm1.save()
        cm2 = models.ChampsModifie()
        cm2.champs = mod
        cm2.nomchamp = 'Date d\'upload'
        cm2.valchamp = c.uploadDate
        cm2.save()
        if (personnes != None):
            cm3 = models.ChampsModifie()
            cm3.champs = mod
            cm3.nomchamp = 'Personnes du groupe '
            a = ''
            for p in c.personnes.all():
                a = a+str(p)+' '
            cm3.valchamp = a
            cm3.save()
        if (modules != None):
            cm4 = models.ChampsModifie()
            cm4.champs = mod
            cm4.nomchamp = 'Modules du groupe '
            m = ''
            for p in c.modules.all():
                m = m+str(p)+' '
            cm4.valchamp = m
            cm4.save()
        
        n = models.News()
        n.txt = txt
        n.typeG = AJOUT
        n.type = GROUPESTATUT
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(pers) 
        
        return c.id

def addCour(pers, nom, isExam=False, profs=None):
    """
       Add a type of lesson in the database
        
        :param pers: the user who wants to add the object
        :type pers: Personne
        :param nom: name of the type of lesson
        :type nom: string
        :param isExam: is it aan exam ?
        :type isExam: boolean
        :param profs: the teacher(s) of the type of lesson
        :type profs: List of Personne
        
        :examples:
        >> addCour(request.user.personne, "Connaissance de soi")
        save a type of lesson in the database
        
        >> addCour(request.user.personne, "Surprise !", True)
        save exam in the database 
    """
    
    i=TypeCour.objects.filter(nom=nom).count()
    if i==0:
        txt = "Vous avez ajouté le type de cour " + nom
        if isExam:
            txt = txt + " qui est un exam"
        txt = txt + ". "
        c = models.TypeCour()
        c.nom = nom
        c.uploadDate = timezone.now()
        c.isExam = isExam
        if profs != None:
            txt = manytomany(profs, txt, c, models.Personne, "profs", "prof", "le", False)
            c.profs=profs        
        c.save() 
        
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'Cour'
        mod.typemod = AJOUT
        mod.ipmod = c.id
        mod.save()
        cm1 = models.ChampsModifie()
        cm1.champs = mod
        cm1.nomchamp = 'Nom'
        cm1.valchamp = nom
        cm1.save()
        cm2 = models.ChampsModifie()
        cm2.champs = mod
        cm2.nomchamp = 'C\'est un Exam ?'
        if isExam:
            cm2.valchamp = 'oui'
        else:
            cm2.valchamp = 'non'
        cm2.save()
        cm3 = models.ChampsModifie()
        cm3.champs = mod
        cm3.nomchamp = 'Date d\'upload'
        cm3.valchamp = c.uploadDate
        cm3.save()
        cm4 = models.ChampsModifie()
        cm4.champs = mod
        cm4.nomchamp = 'Profs'
        a = ''
        for s in c.profs.all():
            a = a+str(s)
        cm4.valchamp = a
        cm4.save()
        cm5 = models.ChampsModifie()
        cm5.champs = mod
        cm5.nomchamp = 'Groupes'
        g = ''
        for t in c.groupe.all():
            g = g+str(t)
        cm5.valchamp = g
        cm5.save()
        
        n = models.News()
        n.txt = txt
        n.typeG = AJOUT
        n.type = COURTYPESTATUT
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(pers)

def addUV(pers, nom):
    """
        Add an UV in the database
        
        :param pers: the user who wants to add the object
        :type pers: Personne
        :param nom: name of the UV
        :type nom: string
        
        :examples:
        >> addUV(request.user.personne, "2.9")
        save an UV in the database
    """
    
    i=UV.objects.filter(nom=nom).count()
    if i==0:
        c = models.UV()
        c.nom = nom
        c.uploadDate = timezone.now()
        c.save()
        
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'UV'
        mod.typemod = AJOUT
        mod.ipmod = c.id
        mod.save()
        cm1 = models.ChampsModifie()
        cm1.champs = mod
        cm1.nomchamp = 'nom'
        cm1.valchamp = nom
        cm1.save()
        cm2 = models.ChampsModifie()
        cm2.champs = mod
        cm2.nomchamp = 'Date d\'upload'
        cm2.valchamp = c.uploadDate
        cm2.save()
        
        n = models.News()
        n.txt = "Vous avez ajouté l\'UV " + c.nom
        n.typeG = AJOUT
        n.type = UVSTATUT
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(pers)
        
        return c.i

def addModule(pers, nom, uv=None):
    """
        Add a module in the database
            
        :param pers: the user who wants to add the object
        :type pers: Personne
        :param nom: name of the module
        :type nom: string
        :param uv: uv of the module
        :type uv: UV
        
        :example:
        >> uv= UV.objects.get(id=5)
        >> addModule(request.user.personne, "Géopolitique de Brest", uv)
        save a module in the database
    """
    
    i=Module.objects.filter(nom=nom).count()
    if i==0:
        txt = "Vous avez ajouté le module " + nom
        c = models.Module()
        c.uploadDate = timezone.now()
        c.nom = nom
        if uv != None:
            txt = txt + " dans l\'UV " + uv.nom
            c.uv = uv
        c.save()
        
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'Module'
        mod.typemod = AJOUT
        mod.ipmod = c.id
        mod.save()
        cm1 = models.ChampsModifie()
        cm1.champs = mod
        cm1.nomchamp = 'nom'
        cm1.valchamp = nom
        cm1.save()
        if uv != None:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'dans l\'uv'
            cm2.valchamp = str(uv)
            cm2.save()
        cm3 = models.ChampsModifie()
        cm3.champs = mod
        cm3.nomchamp = 'Date d\'upload'
        cm3.valchamp = c.uploadDate
        cm3.save()
        
        n = models.News()
        n.txt = txt
        n.typeG = AJOUT
        n.type = MODULESTATUT
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(pers)

def addNote(pers, note, personne, module, prof):
    """
        Add a mark in the database
        
        :param pers: the user who wants to add the object
        :type pers: Personne    
        :param note: the mark
        :type note: int
        :param personne: person which is marked
        :type personne: Personne
        :param module: module which ithe person is marked
        :type module: Module
        :param prof: teacher who has marked the person
        :type prof: Personne
        
        :example:
        >> p= Personne.objects.get(id=1)
        >> prof= Personne.objects.get(id=3)
        >> m= Module.objects.get(id=3)
        >> addNote(request.user.personne, 0, p, m, prof)
        save a mark in the database
    """
    
    c = models.Note()
    c.note = note
    c.personne = personne
    c.module = module
    c.uploadDate = timezone.now()
    c.prof = prof
    c.save()
    
    mod = models.Modification()
    mod.datemodif = timezone.now()
    mod.typetable = 'Note'
    mod.typemod = AJOUT
    mod.ipmod = c.id
    mod.save()
    cm1 = models.ChampsModifie()
    cm1.champs = mod
    cm1.nomchamp = 'Elève'
    cm1.valchamp = personne
    cm1.save()
    cm2= models.ChampsModifie()
    cm2.champs = mod
    cm2.nomchamp = 'Note'
    cm2.valchamp = note
    cm2.save()
    cm3 = models.ChampsModifie()
    cm3.champs = mod
    cm3.nomchamp = 'Module'
    cm3.valchamp = module
    cm3.save()
    cm4 = models.ChampsModifie()
    cm4.champs = mod
    cm4.nomchamp = 'Noté par'
    cm4.valchamp = prof
    cm4.save()
    cm5 = models.ChampsModifie()
    cm5.champs = mod
    cm5.nomchamp = 'Date d\'upload'
    cm5.valchamp = c.uploadDate
    cm5.save()
    
    n = models.News()
    n.txt = "Vous avez ajouté la note " + str(c.note) + " à la personne " + c.personne.filter + " au module " + c.module.nom  
    n.typeG = AJOUT
    n.type = NOTESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(pers)
    
    n2 = models.News()
    n2.txt = "Vous avez eu " + str(c.note) + " au module " + c.module.nom  +" (noté par " + prof.filter +")"
    n2.typeG = AJOUT
    n2.type = NOTESTATUT
    n2.uploadDate = timezone.now()   
    n2.save()
    n2.personne.add(c.personne)

def addSalle(pers, nom, capacite=None, typee=None):
    """
        Add a classroom in the database
            
        :param pers: the user who wants to add the object
        :type pers: Personne
        :param nom: name of the classroom
        :type nom: string
        :param capacite: capacity of the classroom
        :type capacite: int
        :param typee: which type of classroom (labo etc...)
        :type typee: list of tuple
        
        :example:
        >> from BDD.choices import INFO_STATUT
        >> addSalle(request.user.personne, "404", capacite=30, typee=INFO_STATUT)
        save a classroom in the database
    """
    
    i=Salle.objects.filter(nom=nom).count()
    if i==0:
        c = models.Salle()
        c.nom = nom
        if typee != None:
            c.type = typee
        if capacite != None:
            c.capacite = capacite
        c.uploadDate = timezone.now()
        c.save()
        
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'Salle'
        mod.typemod = AJOUT
        mod.ipmod = c.id
        mod.save()
        cm1 = models.ChampsModifie()
        cm1.champs = mod
        cm1.nomchamp = 'Salle '
        cm1.valchamp = nom
        cm1.save()
        if capacite != None:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'Capacite de la salle'
            cm2.valchamp = str(capacite)+' personnes'
            cm2.save()
        if str(typee) != '0' and typee != None:
            cm3 = models.ChampsModifie()
            cm3.champs = mod
            cm3.nomchamp = 'Type de salle'
            if str(type)=='1':
                cm3.valchamp = 'Classe'
            elif str(type)=='2':
                cm3.valchamp = 'Labo'
            elif str(type)=='3':
                cm3.valchamp = 'Info'
            else:
                cm3.valchamp = 'Inconnu' 
            cm3.save()
            cm4 = models.ChampsModifie()
            cm4.champs = mod
            cm4.nomchamp = 'Date d\'upload'
            cm4.valchamp = c.uploadDate
            cm4.save()
    
        n = models.News()
        txt = "Vous avez ajouté la salle " + nom
        if typee != None and int(typee) != 0:
            txt = txt + " de type " + str(c.get_type_display())
            if capacite != None:
                txt = txt + " et"
        if capacite != None:
            txt = txt + " de " + str(capacite) + " places"   
        n.txt = txt
        n.typeG = AJOUT
        n.type = SALLESTATUT
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(pers)