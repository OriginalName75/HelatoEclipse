'''
Created on 26 oct. 2015

@author: Moran
'''
from datetime import date
import random

from django.utils import timezone

from BDD.choices import SALLES, PROF_STATUT
from BDD.models import Personne, Groupe, UV, Module, Salle, TypeCour
from Functions import addData
import random as r
FIRST = ['Théorie', "Entropologie", "Théorème", "Supercherie", "Science", "Modélisation", "Formation", "Innutilisté", "Problème", "Problème non résolu", "Solution", "Complexe", "Paradoxe"]
DEUZE = ['de Gauss', 'de Gauss-Wei[..]ass', 'de Pythagore', 'd\'Al Kachi', 'de Thalès', 'des éléments fini', "des elements infini", " de rien", "de tout", "de l'impossible", "du n'importe quoi", " de Hearthstone"]
    

def courType(n, clear=False):
    if (clear):
        for p in TypeCour.objects.all():
            p.delete()
    profs = Personne.objects.filter(type=PROF_STATUT)
    groupes = Groupe.objects.all()
    for i in range(0, n):
        c = TypeCour()
        c.isExam = False
        f = r.choice(FIRST)
        d = r.choice(DEUZE)
        nom = f + ' ' + d
        c.nom = nom
        c.save()
        rand = r.choice(range(0, 7))
        if rand == 0:
            nbprof = 4
        elif rand == 1:
            nbprof = 2
        else:
            nbprof = 1
        for i in range(0, nbprof):
            c.profs.add(r.choice(profs))
            
        c.groupe.add(r.choice(groupes))
        

def salles(n, m, clear=False):
    lets = 'ABCDEFGHIJKLMN'
    if (clear):
        for p in Salle.objects.all():
            p.delete()
    for i in lets:
        for j in range(0, n):
            for k in range(0, m):
                sal = Salle()
                nom = i + str(j * 100 + k)
                sal.nom = nom
                sal.capacite = r.choice(range(20, 50))
                sal.type = r.choice(SALLES)[0]
                sal.save()
        
def module(n, clear=False):
   
    if (clear):
        for p in Module.objects.all():
            p.delete()
            
    uvs = UV.objects.all()
    for u in uvs:
        for i in range(0, n):
            mod = Module()
            f = r.choice(FIRST)
            d = r.choice(DEUZE)
            nom = f + ' ' + d
            mod.nom = nom
            mod.uv = u
            mod.save()
            
            
def uvs(n , m , clear=False):
    if (clear):
        for p in UV.objects.all():
            p.delete()
    for i in range(1, n + 1):
        for j in range(1, 1 + m):
            uv = UV()
            uv.nom = str(i) + "." + str(j)
            uv.save()
def groupe(n, clear=False):
    if (clear):
        for p in Groupe.objects.all():
            p.delete()
    lets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pers = Personne.objects.all()
    grps = []
    for i in range(0, n):
        grp = Groupe()
        nom = ''
        n = r.choice(range(3, 10))
        for ii in range(0, n):
            nom += r.choice(lets)
        grp.nom = nom
        grp.uploadDate = timezone.now()
        grp.save()
        grps.append(grp)
    
    grptiers1 = Groupe()
    grptiers1.nom = 'tier 1'
    grptiers1.uploadDate = timezone.now()
    grptiers1.save()
    grptiers2 = Groupe()
    grptiers2.nom = 'tier 2'
    grptiers2.uploadDate = timezone.now()
    grptiers2.save()
    grptiers3 = Groupe()
    grptiers3.nom = 'tier 3'
    grptiers3.uploadDate = timezone.now()
    grptiers3.save()
    grptous = Groupe()
    grptous.nom = 'tous'
    grptous.uploadDate = timezone.now()
    grptous.save()
    for p in pers:
        ra = r.choice(range(0, 3))
        if ra == 1:
            grptiers1.personnes.add(p)
        elif ra == 0:
            grptiers2.personnes.add(p)
        else:
            grptiers3.personnes.add(p)
        grptous.personnes.add(p)
        g = r.choice(grps)
        g.personnes.add(p)
        
def telgene():
    stri = str(0) + str(1)
    i = 0
    while i < 8:
        stri = stri + str(random.randint(0, 9))
        i = i + 1
        
        
    return stri
def personnes(n, clear=False):
    prenoms = ['Tyrion', 'Cersei', 'Jon', 'Sensae', 'Arya', 'Jorah', 'Jaime', 'Samwell', 'Petyr', 'Theon', 'Tywin', 'Sandor', 'Jofrey']
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
