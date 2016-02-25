'''
Created on 23 févr. 2016

@author: mabadie_2
'''
from django.utils import timezone

from BDD import models
from BDD.choices import AJOUT, MODIFIER, SALLESTATUT, SUPRIMER, GROUPESTATUT,\
    UVSTATUT, MODULESTATUT, CALENDRIERSTATUT


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
    elif  obj.type == GROUPESTATUT:
        txt= txt+ str(nb) + " groupes"
    elif  obj.type == MODULESTATUT:
        txt= txt+ str(nb) + " modules"
    elif  obj.type == UVSTATUT:
        txt= txt+ str(nb) + " UV"
    elif  obj.type == CALENDRIERSTATUT:
        txt= txt+ str(nb) + " cours"
    else :
        txt= txt+ str(nb) + " personnes"  
    return txt

def manytomany(newtable, txt, obj, model, many, nom, auoala, sens, attrafiche=None, txt2=None, STATUT=None):
    l=[]
    for g in newtable:
        found=False
        for u in getattr(obj, many).all():
            if u.id==int(g):
                found=True
                
                break
        if not found:
            l.append(g)
            if STATUT!=None:
                n=models.News()
                n.txt="Vous avez été ajouté à " + str(obj)
                n.typeG=AJOUT
                n.type=STATUT
                n.uploadDate = timezone.now()   
                n.save()
                n.personne.add(g) 
    l2=[]
    for g in getattr(obj, many).all():
        found=False
        for u in newtable:
            if g.id==int(u):
                found=True
                
                break
        if not found:
            
            l2.append(g)
            if STATUT!=None:
                n=models.News()
                n.txt="Vous avez été enlevé de " + str(obj)
                n.typeG=SUPRIMER
                n.type=STATUT
                n.uploadDate = timezone.now()   
                n.save()
                n.personne.add(g) 
    if len(l)>2:
        if sens:
            txt= txt + ". Vous l\'avez ajouté à " + str(len(l)) + " "+nom+"s. "    
        else:
            txt= txt + ". Vous y avez ajouté " + str(len(l)) + " "+nom+"s. "  
            
        if txt2!=None:
                txt2= txt2 + ". Vous avez été ajouté à " + str(len(l)) + " "+nom+"s. "        
    elif len(l)>0:
        if sens:
            txt = txt + " Vous l\'avez ajouté "
        else:
            txt = txt + " Vous y avez ajouté "
        if txt2!=None:
            txt2 = txt2 + " Vous avez été ajouté "
        first=True
        for ggg in l:
            if not first:
                txt = txt + " et " 
                if txt2!=None:
                    txt2 = txt2 + " et " 
            if attrafiche!=None:
                att=getattr(model.objects.get(id=int(ggg)), attrafiche)
            else:
                att=str(model.objects.get(id=int(ggg)))
            
            txt= txt + " "+auoala+" "+nom+" " + att + " "
            if txt2!=None:
                txt2= txt2 + " "+auoala+" "+nom+" " + att + " "
            first=False
    if len(l2)>2:
        if sens:
            txt= txt + ". Vous l\'avez enlevé à " + str(len(l)) + " "+nom+". "   
        else:
            txt= txt + ". Vous y avez enlevé " + str(len(l)) + " "+nom+". "   
        if txt2!=None:
            txt2= txt2 + ". Vous avez été enlevé à " + str(len(l)) + " "+nom+"s. " 
    elif len(l2)>0:
        if sens:
            txt = txt + " Vous l\'avez enlevé "
        else:
            txt = txt + " Vous y avez enlevé "
        if txt2!=None:
            txt2 = txt2 + " Vous avez été enlevé "
        first=True
        for ggg in l2:
            if not first:
                txt = txt + " et " 
                if txt2!=None:
                    txt2 = txt2 + " et " 
            if attrafiche!=None:
                att=getattr(ggg, attrafiche)
            else:
                att=str(ggg)
            txt= txt + " "+auoala+" "+nom+" " + att + ". "
            if txt2!=None:
                txt2= txt2 + " "+auoala+" "+nom+" " + att + ". "
            first=False    
    if txt2==None:
        return txt
    else:
        return txt, txt2