"""
    The ''news'' module
    ======================
    
    It define functions which are related to the news system
    
    
@author: IWIMBDSL
"""
from django.utils import timezone

from BDD import models
from BDD.choices import AJOUT, MODIFIER, SALLESTATUT, SUPRIMER, GROUPESTATUT, \
    UVSTATUT, MODULESTATUT, CALENDRIERSTATUT


def addN(obj, nb, plus, n):
    """
        return the text in function of the paramters when many news of the same kind
        are printed
    
    :param obj: the news
    :type obj: Model object
    :param nb: how many news of the same kind
    :type nb: int
    :param plus: if the news is clarified or not
    :type plus: boolean
    :param n: the position of the news in the template
    :type n: int
    :return: text printed of the news in html code
    :rtype: string
    
    :exemple:
    >> obj = News.objects.get(id=4)
    >> addN(obj, 1, True, 1)
    html code of the news, it will start with <a href=\"/f/"1"\">+</a>
    
    """
    if plus:
        txt = "<a href=\"/f/" + str(n) + "\">+</a> "
    else:
        txt = "<a href=\"/f/0\">-</a> "
    
    if obj.typeG == AJOUT:
        txt = txt + "Vous avez ajouté "
    elif obj.typeG == MODIFIER:
        txt = txt + "Vous avez modifié "
    else:
        txt = txt + "Vous avez suprimé "
    if obj.type == SALLESTATUT:
        txt = txt + str(nb) + " salles"
    elif  obj.type == GROUPESTATUT:
        txt = txt + str(nb) + " groupes"
    elif  obj.type == MODULESTATUT:
        txt = txt + str(nb) + " modules"
    elif  obj.type == UVSTATUT:
        txt = txt + str(nb) + " UV"
    elif  obj.type == CALENDRIERSTATUT:
        txt = txt + str(nb) + " cours"
    else :
        txt = txt + str(nb) + " personnes"  
    return txt

def manytomany(newtable, txt, obj, model, many, nom, auoala, sens, attrafiche=None, txt2=None, STATUT=None):
    """
        text printed for many to many relations news
        
    :param newtable: list of objects added/modified or deleted in a many to many relation
    :type newtable: list of Model
    :param txt: text to add for the user
    :type txt: string
    :param obj: object added/modified or deleted 
    :type obj: Model obecj
    :param model: Which model
    :type model: Model
    :param many: the manytomany name of the object added/modified or deleted 
    :type many: string
    :param nom: name of the manytomany relation printed in the news
    :type nom: string
    :param auoala: if it is 'la' or 'le' etc..
    :type auoala: string
    :param sens: in which sense the sentence is written (psive form or bot)
    :type sens: boolean
    :param attrafiche: if None take the __str__ value of the objects int the manytomany, if not take the attrafiche value
    :type attrafiche: string
    :param txt2: if not only the user will have a news
    :type txt2: string
    :param STATUT: if every object of th lanytomany are person send the news
    :type STATUT: list of tuples
    :return: if txt2=None return the new text else the two news text txt and txt2
    :rtype: string or tuple of string
    
    
    """
    l = []
    for g in newtable:
        found = False
        for u in getattr(obj, many).all():
            if u.id == int(g):
                found = True
                
                break
        if not found:
            l.append(g)
            if STATUT != None:
                n = models.News()
                n.txt = "Vous avez été ajouté à " + str(obj)
                n.typeG = AJOUT
                n.type = STATUT
                n.uploadDate = timezone.now()   
                n.save()
                n.personne.add(g) 
    l2 = []
    for g in getattr(obj, many).all():
        found = False
        for u in newtable:
            if g.id == int(u):
                found = True
                
                break
        if not found:
            
            l2.append(g)
            if STATUT != None:
                n = models.News()
                n.txt = "Vous avez été enlevé de " + str(obj)
                n.typeG = SUPRIMER
                n.type = STATUT
                n.uploadDate = timezone.now()   
                n.save()
                n.personne.add(g) 
    if len(l) > 2:
        if sens:
            txt = txt + ". Vous l\'avez ajouté à " + str(len(l)) + " " + nom + "s. "    
        else:
            txt = txt + ". Vous y avez ajouté " + str(len(l)) + " " + nom + "s. "  
            
        if txt2 != None:
                txt2 = txt2 + ". Vous avez été ajouté à " + str(len(l)) + " " + nom + "s. "        
    elif len(l) > 0:
        if sens:
            txt = txt + " Vous l\'avez ajouté "
        else:
            txt = txt + " Vous y avez ajouté "
        if txt2 != None:
            txt2 = txt2 + " Vous avez été ajouté "
        first = True
        for ggg in l:
            if not first:
                txt = txt + " et " 
                if txt2 != None:
                    txt2 = txt2 + " et " 
            if attrafiche != None:
                att = getattr(model.objects.get(id=int(ggg)), attrafiche)
            else:
                att = str(model.objects.get(id=int(ggg)))
            
            txt = txt + " " + auoala + " " + nom + " " + att + " "
            if txt2 != None:
                txt2 = txt2 + " " + auoala + " " + nom + " " + att + " "
            first = False
    if len(l2) > 2:
        if sens:
            txt = txt + ". Vous l\'avez enlevé à " + str(len(l)) + " " + nom + ". "   
        else:
            txt = txt + ". Vous y avez enlevé " + str(len(l)) + " " + nom + ". "   
        if txt2 != None:
            txt2 = txt2 + ". Vous avez été enlevé à " + str(len(l)) + " " + nom + "s. " 
    elif len(l2) > 0:
        if sens:
            txt = txt + " Vous l\'avez enlevé "
        else:
            txt = txt + " Vous y avez enlevé "
        if txt2 != None:
            txt2 = txt2 + " Vous avez été enlevé "
        first = True
        for ggg in l2:
            if not first:
                txt = txt + " et " 
                if txt2 != None:
                    txt2 = txt2 + " et " 
            if attrafiche != None:
                att = getattr(ggg, attrafiche)
            else:
                att = str(ggg)
            txt = txt + " " + auoala + " " + nom + " " + att + ". "
            if txt2 != None:
                txt2 = txt2 + " " + auoala + " " + nom + " " + att + ". "
            first = False    
    if txt2 == None:
        return txt
    else:
        return txt, txt2
