'''
Created on 2 févr. 2016

@author: Morgan
'''

from BDD import models
from BDD.choices import AJOUT, MODIFIE, SUPPRIME
from BDD.models import Modification, ChampsModifie, Personne, Groupe, Module, \
    Salle, Note, UV, TypeCour


def Ctrlz(d):
    i=models.Modification.objects.filter(models.Modification.datemodif<d)[0]
    a=i[0]
    for p in i:
        if p.datemodif > a.datemodif:
            a=p
    i=models.Personne.objects.filter(id=a.ipmod).count()
    if(i!=0):
        b = models.Personne.objects.filter(id=a.ipmod)[0]
    else:
        i=models.Groupe.objects.filter(id=a.ipmod).count()
        if(i!=0):
            b = models.Groupe.objects.filter(id=a.ipmod)[0]
        else:
            i=models.UV.objects.filter(id=a.ipmod).count()
            if(i!=0):
                b = models.UV.objects.filter(id=a.ipmod)[0]
            else:
                i=models.Module.objects.filter(id=a.ipmod).count()
                if(i!=0):
                    b = models.Module.objects.filter(id=a.ipmod)[0]
                else:
                    i=models.Salle.objects.filter(id=a.ipmod).count()
                    if(i!=0):
                        b = models.Salle.objects.filter(id=a.ipmod)[0]
                    else:
                        i=models.Note.objects.filter(id=a.ipmod).count()
                        if(i!=0):
                            b = models.Note.objects.filter(id=a.ipmod)[0]
                        else:
                            i=models.TypeCour.objects.filter(id=a.ipmod).count()
                            if(i!=0):
                                b = models.TypeCour.objects.filter(id=a.ipmod)[0]
                            else:
                                i=models.Cour.objects.filter(id=a.ipmod).count()
                                if(i!=0):
                                    b = models.Cour.objects.filter(id=a.ipmod)[0]
    if a.typemod == SUPPRIME:
        b.isvisible = True
    elif a.typemod == AJOUT:
        b.isvisible = False
    elif a.typemod == MODIFIE:
        for k in models.ChampsModifie.objects.filter(models.ChampsModifie.champs==a)[0]:
            if k.nomchamp == 'nom changé depuis':
                b.nom = k.valchamp
            if k.nomchamp == 'membres changés depuis' or a.nomchamp == 'élève changé depuis':
                b.personnes = k.valchamp
            if k.nomchamp == 'UV changé depuis':
                b.uv = a.valchamp
            if k.nomchamp == 'note changée depuis':
                b.note = k.valchamp
            if k.nomchamp == 'module changé depuis':
                b.module = k.valchamp
            if k.nomchamp == 'isExam changé depuis':
                b.isExam = k.valchamp
            if k.nomchamp == 'groupes changés depuis':
                b.groupe = k.valchamp
            if k.nomchamp == 'profs changés depuis':
                b.profs = k.valchamp
            if k.nomchamp == 'capacite changée depuis':
                b.capacite = k.valchamp
            if k.nomchamp == 'prenom changé depuis':
                b.user.first_name = k.valchamp
            if k.nomchamp == 'login changé depuis':
                b.user.username = k.valchamp
            if k.nomchamp == 'email changé depuis':
                b.user.email = k.valchamp
            if k.nomchamp == 'adresse changé depuis':
                b.adresse = k.valchamp
            if k.nomchamp == 'promotion changé depuis':
                b.promotion = k.valchamp
            if k.nomchamp == 'dateDeNaissance changé depuis':
                b.dateDeNaissance = k.valchamp
            if k.nomchamp == 'lieuDeNaissance changé depuis':
                b.lieuDeNaissance = k.valchamp
            if k.nomchamp == 'numeroDeTel changé depuis':
                b.numeroDeTel = k.valchamp
            if k.nomchamp == 'sexe changé depuis':
                b.sexe = k.valchamp
            if k.nomchamp == 'superuser changé depuis':
                b.user.is_superuser = k.valchamp            
    a.datemodif.replace(day=01, month=01)
    
def delet(dat):
    y = Modification.objects.all()
    for x in y:
        if x.datemodif < dat:
            x.delete()
    y = ChampsModifie.objects.all()
    for x in y:
        if x.champs.datemodif < dat:
            x.delete()
    y = Personne.objects.all()
    for x in y:
        if x.isvisible==False:
            x.delete()
    y = Groupe.objects.all()
    for x in y:
        if x.isvisible==False:
            x.delete()
    y = UV.objects.all()
    for x in y:
        if x.isvisible==False:
            x.delete()
    y = Module.objects.all()
    for x in y:
        if x.isvisible==False:
            x.delete()
    y = Salle.objects.all()
    for x in y:
        if x.isvisible==False:
            x.delete()
    y = Note.objects.all()
    for x in y:
        if x.isvisible==False:
            x.delete()
    y = TypeCour.objects.all()
    for x in y:
        if x.isvisible==False:
            x.delete()
    
    