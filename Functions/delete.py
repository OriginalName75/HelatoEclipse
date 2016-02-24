'''
Created on 23 févr. 2016

@author: mabadie_2
'''
from django.utils import timezone

from BDD import models
from BDD.choices import SUPRIMER, SALLESTATUT
from Functions import data


def supr_salles(table, idP,p):
    
    txt="vous avez suprimé "
    obj = data.table(table).objects.get(id=int(idP))
    
    if table==5:
        txt=txt+"la salle " + obj.nom
    elif table==0:
        txt=txt+"la personne " + obj.user.first_name + " " + obj.user.last_name
    n = models.News()
    n.txt = txt
    n.typeG = SUPRIMER
    n.type = SALLESTATUT
    n.uploadDate = timezone.now()   
    n.save()
    n.personne.add(p)   