'''
Created on 23 févr. 2016

@author: mabadie_2
'''
from BDD.choices import AJOUT, MODIFIER, SALLESTATUT


def addN(obj, nb, plus, n):
    if plus:
        txt="<a href=\"/f/"+ str(n) +"\">+</a> "
    else:
        txt="<a href=\"/f/0\">-</a> "
    
    if obj.typeG == AJOUT:
        txt= txt + "Vous avez ajouté "
    elif obj.typeG == MODIFIER:
        txt= txt + "Vous avez modifié "
    else:
        txt= txt + "Vous avez suprimé "
    if obj.type == SALLESTATUT:
        txt= txt+ str(nb) + " salles"
    else :
        txt= txt+ str(nb) + " personnes"  
    return txt