"""
    The ''delete'' module
    ======================
    
    It define the functions to delete objects in the database.
    It takes care of news ( for ctrl-z) 
    
    :Exemple:
    
    >> supr_salles(1, 3, request.user.personne)
    it delete the group (because table=1, the first argument) which the id = 3.
     
    
@author: IWIMBDSL
"""
from django.utils import timezone

from BDD import models
from BDD.choices import SUPRIMER, SALLESTATUT, GROUPESTATUT, PERSONNESTATUT, \
    UVSTATUT, MODULESTATUT, CALENDRIERSTATUT, NOTESTATUT, COURTYPESTATUT
from Functions import data


def supr_salles(table, idP, p):
    """
        Delete objects in the database
        
    :param table: it represent which kind of data it is (exemple: a groupe)
    :type table: int 
    :param idP: id of the object to delete
    :type idP: int
    :param p: user who deletes the object
    :type p: Personne
    
    :Exemple:
    
    >> supr_salles(1, 3, request.user.personne)
    it delete the group (because table=1, the first argument) which the id = 3.
    
    """
    
    txt = "vous avez supprimé "
    obj = data.table(table).objects.filter(id=int(idP))
    if len(obj)>0:
        obj=obj[0]
        obj.isvisible=False
        obj.save()
        if table == 5:
            ST = SALLESTATUT
            txt = txt + "la salle " + obj.nom
        elif table == 0:
            ST = PERSONNESTATUT
            txt = txt + "la personne " + obj.user.first_name + " " + obj.user.last_name
        elif table == 1:
            ST = GROUPESTATUT
            txt = txt + "le groupe " + obj.nom
            for p in obj.personnes.all():
                n = models.News()
                n.txt = "Votre groupe " + obj.nom + " a ete supprimé"
                n.typeG = SUPRIMER
                n.type = GROUPESTATUT
                n.uploadDate = timezone.now()   
                n.save()
                n.personne.add(p)   
        elif table == 2:
            ST = UVSTATUT
            txt = txt + "l\'UV " + obj.nom
        elif table == 3:
            ST = MODULESTATUT
            txt = txt + "le module " + obj.nom
        elif table == 4:
            ST = CALENDRIERSTATUT
            txt = txt + "un cour de " + obj.typeCour.nom
        elif table == 6:
            ST = NOTESTATUT
            txt = txt + "une note de " + obj.personne.filter
        else :
            ST = COURTYPESTATUT
            txt = txt + "un cour de " + obj.nom
        n = models.News()
        n.txt = txt
        n.typeG = SUPRIMER
        n.type = ST
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(p)  
