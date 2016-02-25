'''
Created on 23 févr. 2016

@author: mabadie_2
'''
from django.utils import timezone

from BDD import models
from BDD.choices import SUPRIMER, SALLESTATUT, GROUPESTATUT, PERSONNESTATUT, \
    UVSTATUT, MODULESTATUT
from Functions import data


def supr_salles(table, idP,p):
    
    txt="vous avez suprimé "
    obj = data.table(table).objects.get(id=int(idP))
    
    if table==5:
        ST=SALLESTATUT
        txt=txt+"la salle " + obj.nom
    elif table==0:
        ST=PERSONNESTATUT
        txt=txt+"la personne " + obj.user.first_name + " " + obj.user.last_name
    elif table==1:
        ST=GROUPESTATUT
        txt=txt+"le groupe " + obj.nom
        for p in obj.personnes.all():
            n = models.News()
            n.txt = "Votre groupe " + obj.nom +" a été suprimé"
            n.typeG = SUPRIMER
            n.type = GROUPESTATUT
            n.uploadDate = timezone.now()   
            n.save()
            n.personne.add(p)   
    elif table==2:
        ST=UVSTATUT
        txt=txt+"l\'UV " + obj.nom
    elif table==3:
        ST=MODULESTATUT
        txt=txt+"le module " + obj.nom
    n = models.News()
    n.txt = txt
    n.typeG = SUPRIMER
    n.type = ST
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)   