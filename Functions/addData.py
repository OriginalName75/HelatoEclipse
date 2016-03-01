'''
Created on 25 oct. 2015

@author: Moran
'''
from django.contrib.auth.models import User
from django.utils import timezone

from BDD import models
from BDD.choices import PROF_STATUT, AJOUT
from BDD.models import Personne, horaireProf, Groupe, TypeCour, UV, Module, \
    Salle


def checkNaddPersonne(nom, prenom, login, mdp, sexe, typeP, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None, errors=None):
    if User.objects.filter(username=login).exists():
        errors[0] = "Login existe deja"
    else :
        addPersonne(nom, prenom, login, mdp, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, email)
   
   
#a modifier
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
        
def addGroupe(nomm, personnes=None):
    i=Groupe.objects.filter(nom=nomm).count()
    if i==0:
        c = models.Groupe()
        c.nom = nomm
        c.uploadDate = timezone.now()
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
        if (personnes!=None):
            c.personnes=personnes
        cm3 = models.ChampsModifie()
        cm3.champs = mod
        cm3.nomchamp = 'ID des personnes du groupe'
        a = ''
        for p in c.personnes.all():
            a = a+str(p)+' '
        cm3.valchamp = a
        cm3.save()
        return c.id
    
def addCour(nom, isExam=False):
    i=TypeCour.objects.filter(nom=nom).count()
    if i==0:
        c = models.TypeCour()
        c.nom = nom
        c.isExam = isExam
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
        
def addUV(nom):
    i=UV.objects.filter(nom=nom).count()
    if i==0:
        c = models.UV()
        c.nom = nom
        c.save()
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'UV'
        mod.typemod = AJOUT
        mod.ipmod = c.id
        mod.save()
        cm = models.ChampsModifie()
        cm.champs = mod
        cm.nomchamp = 'nom'
        cm.valchamp = nom
        cm.save()
        
def addModule(nom, uv):
    i=Module.objects.filter(nom=nom).count()
    if i==0:
        c = models.Module()
        c.nom = nom
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
        cm2 = models.ChampsModifie()
        cm2.champs = mod
        cm2.nomchamp = 'dans l\'uv'
        cm2.valchamp = str(uv)
        cm2.save()

def addNote(note, personne, module):
    c = models.Note()
    c.note = note
    c.personne = personne
    c.module = module
    c.uploadDate = timezone.now()
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
    
def addSalle(nom, capacite=None, typ=None):
    i=Salle.objects.filter(nom=nom).count()
    if i==0:
        c = models.Salle()
        c.nom = nom
        if typ != None:
            c.type = typ
        if capacite != None:
            c.capacite = capacite
        c.save()
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'Salle'
        mod.typemod = AJOUT
        mod.ipmod = c.id
        mod.save()
        cm1 = models.ChampsModifie()
        cm1.champs = mod
        cm1.nomchamp = 'Numero de salle'
        cm1.valchamp = nom
        cm1.save()
        if capacite != None:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'Capacite de la salle'
            cm2.valchamp = str(capacite)+' personnes'
            cm2.save()
        if str(type) != '0':
            cm3 = models.ChampsModifie()
            cm3.champs = mod
            cm3.nomchamp = 'Type de salle'
            if str(type)=='1':
                cm3.valchamp = 'Classe'
            elif str(type)=='2':
                cm3.valchamp = 'Labo'
            elif str(type)=='3':
                cm3.valchamp = 'Info'
            cm3.save()