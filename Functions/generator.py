'''
Created on 26 oct. 2015

@author: Moran
'''
from datetime import date
import random

from BDD import models
from BDD.models import Personne
from Functions import addData


def telgene():
    stri = str(0) + str(1)
    i = 0
    while i < 8:
        stri = stri + str(random.randint(0, 9))
        i = i + 1
        
        
    return stri
def personnes(n, clear=False):
    prenoms =  ['Tyrion', 'Cersei', 'Jon', 'Sensae', 'Arya', 'Jorah', 'Jaime', 'Samwell', 'Petyr', 'Theon', 'Tywin', 'Sandor', 'Jofrey']
    noms = ['Lannister', 'Clarke', 'Harington', 'Snow', 'Slark', 'Turner', 'Williams', 'Glen', 'Bradley', 'Hill', 'Baratheon']
    villes = ['Paris', 'Brest', 'New York', 'Trouville', 'Pekin']
    i = 0
    if (clear):
        for p in Personne.objects.all():
            p.delete()
    while i < n:
        prenom = prenoms[random.randint(0, len(prenoms) - 1)]
        nom = noms[random.randint(0, len(noms) - 1)]
        login = prenom + nom + str(random.randint(0, 1000000))
        mdp = prenom + nom
        r = random.randint(1, 2)
        sexe = r
        
        r = random.randint(0, 100)
        typeP = 1
        if r < 10:
            r = random.randint(0, 1)
            if r == 0:
                typeP = 0
            else:
                typeP = 2      
        adresse = str(random.randint(0, 100)) + ' Avenue ' + prenoms[random.randint(0, len(prenoms) - 1)] + ' ' + villes[random.randint(0, len(villes) - 1)] 
        promotion = random.randint(2017, 2020)
        dateDeNaissance = date(random.randint(1980, 1995), random.randint(1, 12), random.randint(1, 28))
        lieuDeNaissance = villes[random.randint(0, len(villes) - 1)]
        numeroDeTel = telgene()
        mail = nom + prenom + '@enstabretagne.org'
        addData.addPersonne(nom, prenom, login, mdp, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, mail)
        i = i + 1
