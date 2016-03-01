'''
Created on 30 oct. 2015

@author: mabadie_2
'''
from BDD import models
from django.utils import timezone
from BDD.choices import INCONNU_STATUT, MODIFIE


def modGroupe(idP, nom=None, personnes=None):
    c = models.Groupe.objects.filter(id=idP)[0]
    if nom != c.nom or (personnes != c.personnes and personnes != None):
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'GroupeChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = c.id
        mod.save()
        if nom != c.nom:
            cm1 = models.ChampsModifie()
            cm1.champs = mod
            cm1.nomchamp = 'nom changé depuis'
            cm1.valchamp = c.nom
            cm1.save()
            c.nom = nom
        if personnes != c.personnes and personnes != None:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'membres changés depuis'
            a = ''
            for p in c.personnes.all():
                a = a+str(p)
            cm2.valchamp = a
            cm2.save()
            c.personnes = personnes
        c.save()
        

def modModule(idP, nom, uv=None):
    c = models.Module.objects.filter(id=idP)[0]
    if nom != c.nom or uv != c.uv:
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'ModuleChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = c.id
        mod.save()
        if nom != c.nom:
            cm1 = models.ChampsModifie()
            cm1.champs = mod
            cm1.nomchamp = 'nom changé depuis'
            cm1.valchamp = c.nom
            cm1.save()
            c.nom = nom
        if uv != c.uv:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'UV changé depuis'
            cm2.valchamp = c.uv
            cm2.save()
            c.uv = uv
        c.save()
    
def modNote(idP, note=None, personne=None, module=None):
    c = models.Note.objects.filter(id=idP)[0]    
    if note != c.note or (personne != c.personne and personne != None) or (module != c.module and module != None):
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'NoteChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = c.id
        mod.save()
        if note != c.note:
            cm1 = models.ChampsModifie()
            cm1.champs = mod
            cm1.nomchamp = 'note changée depuis'
            cm1.valchamp = c.note
            cm1.save()
            c.note = note
        if personne != c.uv and personne != None:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'élève changé depuis'
            cm2.valchamp = c.personne
            cm2.save()
            c.personne = personne
        if module != c.module and module != None:
            cm3 = models.ChampsModifie()
            cm3.champs = mod
            cm3.nomchamp = 'module changé depuis'
            cm3.valchamp = c.module
            cm3.save()
            c.module = module
        c.save()
        
def modCour(idP, nom, isExam, groupes=None, profs=None):
    c = models.TypeCour.objects.filter(id=idP)[0]    
    if nom != c.nom or isExam != c.isExam or (groupes != None and groupes != c.groupe) or (profs != None and profs != c.profs):
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'CourChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = c.id
        mod.save()
        if nom != c.nom:
            cm1 = models.ChampsModifie()
            cm1.champs = mod
            cm1.nomchamp = 'nom changé depuis'
            cm1.valchamp = nom
            cm1.save()
            c.nom = nom
        if isExam != c.isExam:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'isExam changé depuis'
            cm2.valchamp = c.isExam
            cm2.save()
            c.isExam = isExam
        if groupes != None and groupes != c.groupe:
            cm9 = models.ChampsModifie()
            cm9.champs = mod
            cm9.nomchamp = 'groupes changés depuis'
            cm9.valchamp = c.groupe
            cm9.save()
            c.groupe = groupes
        if profs != None and profs != c.profs:
            cm9 = models.ChampsModifie()
            cm9.champs = mod
            cm9.nomchamp = 'profs changés depuis'
            cm9.valchamp = c.profs
            cm9.save()
            c.profs = profs
        c.save()
    
def modSalle(idP, nom, capacite=None, typ=None):
    c = models.Salle.objects.filter(id=idP)[0]
    if nom != c.nom or capacite != c.capacite or (typ != c.type and typ !='0') :
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'SalleChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = c.id
        mod.save()
        if nom != c.nom:
            cm1 = models.ChampsModifie()
            cm1.champs = mod
            cm1.nomchamp = 'nom changé depuis'
            cm1.valchamp = c.nom
            cm1.save()
            c.nom = nom
        if capacite != c.capacite:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'capacite changée depuis'
            cm2.valchamp = c.capacite
            cm2.save()
            c.capacite = capacite
        if typ != c.type and typ != '0':
            cm3 = models.ChampsModifie()
            cm3.champs = mod
            cm3.nomchamp = 'type changé depuis'
            cm3.valchamp = c.type
            cm3.save()
            c.type = typ
        c.save()
    
def modUV(idP, nom):
    c = models.UV.objects.filter(id=idP)[0]
    if nom != c.nom:
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'UVChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = c.id
        mod.save()
        cm = models.ChampsModifie()
        cm.champs = mod
        cm.nomchamp = 'nom changé depuis'
        cm.valchamp = c.nom
        cm.save()
        c.nom = nom
        c.save()
    
def modPersonne(idP, nom=None, prenom=None, login=None, mdp=None, sexe=None, typeP=None, adresse=None, promotion=None, dateDeNaissance=None, lieuDeNaissance=None, numeroDeTel=None, email=None, groupes=None):
    p = models.Personne.objects.filter(id=idP)[0]
    if (prenom != None and nom != p.user.last_name) or (nom != None and prenom != p.user.first_name) or (login != None and login  != p.user.username) or (email != None and email  != p.user.email):
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'UserChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = p.user.id_
        mod.save()
        if prenom != None and prenom != p.user.first_name:
            cm1 = models.ChampsModifie()
            cm1.champs = mod
            cm1.nomchamp = 'prenom changé depuis'
            cm1.valchamp = p.user.first_name
            cm1.save()
            p.user.first_name = prenom
        if nom != None and nom != p.user.last_name:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'nom changé depuis'
            cm2.valchamp = p.user.last_name
            cm2.save()
            p.user.last_name = nom
        p.filter = "{0} {1}".format(p.user.last_name, p.user.first_name)
        if login != None and login  != p.user.username:
            cm3 = models.ChampsModifie()
            cm3.champs = mod
            cm3.nomchamp = 'login changé depuis'
            cm3.valchamp = p.user.username
            cm3.save()
            p.user.username = login
        if email != None and email  != p.user.email:
            cm4 = models.ChampsModifie()
            cm4.champs = mod
            cm4.nomchamp = 'email changé depuis'
            cm4.valchamp = p.user.email
            cm4.save()
            p.user.email = email
        p.user.save() 
    
    if (adresse != None and adresse != p.adresse) or (promotion != None and promotion != p.promotion) or (dateDeNaissance != None and dateDeNaissance != p.dateDeNaissance) or (lieuDeNaissance != None and lieuDeNaissance != p.lieuDeNaissance) or (numeroDeTel != None and numeroDeTel != p.numeroDeTel) or (sexe != None and int(sexe) != int(p.sexe) and sexe != INCONNU_STATUT) or (typeP != None and int(typeP) != int(p.type)) or (groupes != None and groupes != p.groupe_set):
        mod = models.Modification()
        mod.datemodif = timezone.now()
        mod.typetable = 'PersonneChanged : '
        mod.typemod = MODIFIE
        mod.ipmod = p.id
        mod.save()
        if adresse != None and adresse != p.adresse:
            cm1 = models.ChampsModifie()
            cm1.champs = mod
            cm1.nomchamp = 'adresse changé depuis'
            cm1.valchamp = p.adresse
            cm1.save()
            p.adresse = adresse
        if promotion != None and promotion != p.promotion:
            cm2 = models.ChampsModifie()
            cm2.champs = mod
            cm2.nomchamp = 'promotion changé depuis'
            cm2.valchamp = p.promotion
            cm2.save()
            p.promotion = promotion
        if dateDeNaissance != None and dateDeNaissance != p.dateDeNaissance:
            cm3 = models.ChampsModifie()
            cm3.champs = mod
            cm3.nomchamp = 'dateDeNaissance changé depuis'
            cm3.valchamp = p.dateDeNaissance
            cm3.save()
            p.dateDeNaissance = dateDeNaissance
        if lieuDeNaissance != None and lieuDeNaissance != p.lieuDeNaissance:
            cm4 = models.ChampsModifie()
            cm4.champs = mod
            cm4.nomchamp = 'lieuDeNaissance changé depuis'
            cm4.valchamp = p.lieuDeNaissance
            cm4.save()
            p.lieuDeNaissance = lieuDeNaissance
        if numeroDeTel != None and numeroDeTel != p.numeroDeTel:
            cm5 = models.ChampsModifie()
            cm5.champs = mod
            cm5.nomchamp = 'numeroDeTel changé depuis'
            cm5.valchamp = p.numeroDeTel
            cm5.save()
            p.numeroDeTel = numeroDeTel
        if sexe != None and int(sexe) != int(p.sexe) and sexe != INCONNU_STATUT:
            cm6 = models.ChampsModifie()
            cm6.champs = mod
            cm6.nomchamp = 'sexe changé depuis'
            cm6.valchamp = p.sexe
            cm6.save()
            p.sexe = sexe
        if typeP != None and int(typeP) != int(p.type):
            cm7 = models.ChampsModifie()
            cm7.champs = mod
            cm7.nomchamp = 'type changé depuis'
            cm7.valchamp = p.type
            cm7.save()
            p.type = typeP
            if int(typeP) == 3:
                cm8 = models.ChampsModifie()
                cm8.champs = mod
                cm8.nomchamp = 'superuser changé depuis'
                cm8.valchamp = False
                cm8.save()
                p.user.is_superuser = True
        if groupes != None and groupes != p.groupe_set:
            cm9 = models.ChampsModifie()
            cm9.champs = mod
            cm9.nomchamp = 'groupe changé depuis'
            cm9.valchamp = p.groupe_set
            cm9.save()
            p.groupe_set = groupes
        p.save()
    
