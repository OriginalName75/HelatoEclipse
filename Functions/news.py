"""
    The ''news'' module
    ======================
    
    It define functions which are related to the news system
    
    
@author: IWIMBDSL
"""
from datetime import timedelta
import datetime
from math import floor

from django.utils import timezone

from BDD import models
from BDD.choices import AJOUT, MODIFIER, SALLESTATUT, SUPRIMER, GROUPESTATUT, \
    UVSTATUT, MODULESTATUT, CALENDRIERSTATUT, COURTYPESTATUT


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
        txt = txt + "Vous avez ajoute "
    elif obj.typeG == MODIFIER:
        txt = txt + "Vous avez modifie "
    else:
        txt = txt + "Vous avez suprime "
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
    elif  obj.type == COURTYPESTATUT:
        txt = txt + str(nb) + " type de cours"
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
                n.txt = "Vous avez ete ajoute a " + str(obj)
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
                n.txt = "Vous avez ete enleve de " + str(obj)
                n.typeG = SUPRIMER
                n.type = STATUT
                n.uploadDate = timezone.now()   
                n.save()
                n.personne.add(g) 
    if len(l) > 2:
        if sens:
            txt = txt + ". Vous l\'avez ajoute a " + str(len(l)) + " " + nom + "s. "    
        else:
            txt = txt + ". Vous y avez ajoute " + str(len(l)) + " " + nom + "s. "  
            
        if txt2 != None:
                txt2 = txt2 + ". Vous avez ete ajoute a " + str(len(l)) + " " + nom + "s. "        
    elif len(l) > 0:
        if sens:
            txt = txt + " Vous l\'avez ajoute "
        else:
            txt = txt + " Vous y avez ajoute "
        if txt2 != None:
            txt2 = txt2 + " Vous avez ete ajoute "
        first = True
        for ggg in l:
            if not first:
                txt = txt + " et " 
                if txt2 != None:
                    txt2 = txt2 + " et " 
            if attrafiche != None:
                if not (ggg is int) or not (ggg is str):
                    ggg=ggg.id
                att = getattr(model.objects.get(id=int(ggg)), attrafiche)
            else:
                if not (ggg is int) or not (ggg is str):
                    ggg=ggg.id
                att = str(model.objects.get(id=int(ggg)))
            
            txt = txt + " " + auoala + " " + nom + " " + att + " "
            if txt2 != None:
                txt2 = txt2 + " " + auoala + " " + nom + " " + att + " "
            first = False
    if len(l2) > 2:
        if sens:
            txt = txt + ". Vous l\'avez enleve a " + str(len(l)) + " " + nom + ". "   
        else:
            txt = txt + ". Vous y avez enleve " + str(len(l)) + " " + nom + ". "   
        if txt2 != None:
            txt2 = txt2 + ". Vous avez ete enleve a " + str(len(l)) + " " + nom + "s. " 
    elif len(l2) > 0:
        if sens:
            txt = txt + " Vous l\'avez enleve "
        else:
            txt = txt + " Vous y avez enleve "
        if txt2 != None:
            txt2 = txt2 + " Vous avez ete enleve "
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

def day(year):
    """
        Find the doomsday of the year
        
    :param year: year > 2000 and < 2099
    :type year: int
    :return: doomsday
    :rtype: int
    
    :exemple:
    
    >> day(2O00)
    3 
    >> from BDD.choices import findchoice, SEMAINE
    >> findchoice(day(2O00), SEMAINE)
    Jeudi
    
    
    """
    
    f = floor(year / 1000)
    year = year - f * 1000
    d = floor(year / 100)
    year = year - d * 100
    t = floor(year / 10)
    q = year - f * 10
    
    twolastdigit = t * 10 + q
    
    q = twolastdigit // 12
    r = twolastdigit % 12
    
    t = r // 4
    
    f = q + r + t + 2
    
    doomsday = f % 7
    
    # on met avec nos convention lundi = 0
    doomsday = (doomsday - 1) % 7
    
    return doomsday
    
 
def day2(year, week, d):
    """
        return the date
        
    :param year: year > 2000 and < 2099
    :type year: int
    :param week: the week (number between 0 and 53)
    :type week: int 
    :param d: day between 0 and 6
    :type d: int
    :return: date
    :rtype: datetime
    """
    
    
    doomsday = day(year)
    if doomsday == 0:
        w = 1
    else:    
        w = 7 - doomsday
    re = datetime.date(int(year), 1, int(w)) + timedelta(days=(int(week) - 1) * 7 + int(d))
    return re