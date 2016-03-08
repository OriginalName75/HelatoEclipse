from random import choice
from django.conf import settings
from django.utils.importlib import import_module


from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.test.client import Client
from django.test.testcases import TestCase
from django.utils import timezone
from django.utils.datetime_safe import datetime


from BDD.choices import SEXE, TYPE, TYPENEWS, TYPENEWSG, GROUPESTATUT, \
    HOMME_STATUT, ELEVE_STATUT, LUNDI, SALLES, SEMAINE, ADMINISTRATEUR_STATUT, \
    PROF_STATUT, AJOUT, PERSONNESTATUT, MODIFIER, SUPRIMER
from BDD.models import Personne, News, UV, Groupe
from Functions.addData import addPersonne, addCalendrier, addUV, addModule, \
    addCour, addSalle, addNote, addGroupe
from Functions.data import table
from Functions.generator import salles
from Functions.news import addN, manytomany


# models test
class test_add_data(TestCase):
    

    
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        
        self.alll = True
        self.client = Client()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser=True
        self.user.save()        
        self.puser = Personne()
        self.puser.type=ADMINISTRATEUR_STATUT
        self.puser.user = self.user
        self.puser.save()
        
        self.userteacher = User.objects.create_user('john3', 'lennon3@thebeatles.com', 'john3password')
        self.puserteacher = Personne()
        self.puserteacher.type=PROF_STATUT
        self.puserteacher.user = self.userteacher
        self.puserteacher.save()
        
        self.userteStudent = User.objects.create_user('john4', 'lennon3@thebeatles.com', 'john4password')
        self.puserStudent = Personne()
        self.puserStudent.type=ELEVE_STATUT
        self.puserStudent.user = self.userteStudent
        self.puserStudent.save()
        
        
    def createnews(self, sTATU=PERSONNESTATUT, g=AJOUT):
        n = News()
        n.txt = "txt"
        n.typeG = g
        n.type = sTATU
        n.uploadDate = timezone.now()   
        n.save()
        n.personne.add(self.puser)     
    def test_index(self):
        
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('BDD.views.index'))
        
        self.assertEqual(response.status_code, 200)
        
        
        self.createnews()
        
        
        response = self.client.get(reverse('BDD.views.index'))
        
        self.assertEqual(response.status_code, 200)
        
        self.createnews()
        self.createnews()
        
        
        response = self.client.get(reverse('BDD.views.index'))
        
        self.assertEqual(response.status_code, 200)
        
        
        response = self.client.get(reverse('BDD.views.index', args=[1]))
        
        self.assertEqual(response.status_code, 200)
        self.createnews(g=MODIFIER)
        self.createnews(g=MODIFIER)
        self.createnews(g=SUPRIMER)
        self.createnews(g=SUPRIMER)
        response = self.client.get(reverse('BDD.views.index', args=[0]))
        
        self.assertEqual(response.status_code, 200)
        for Staut in TYPENEWS:
            self.createnews(Staut[0])
            self.createnews(Staut[0])
        response = self.client.get(reverse('BDD.views.index', args=[0]))
        
        self.assertEqual(response.status_code, 200)
    def watch(self):    
        allll=self.alll
        
        
        self.client.login(username='john3', password='john3password')
        response = self.client.get(reverse('BDD.views.watch',args=[1,2]))
        self.assertEqual(response.status_code, 200) 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('BDD.views.watch',args=[1,2]))
        self.assertEqual(response.status_code, 200) 
        
        
        response = self.client.post(reverse('BDD.views.watch',args=[0,1]),{'nom': 'a', 'prenom':'', 'login':'', 'mail':'', 'sexe':'0', 'adresse':'', 'typeP':'0', 'dateDeNaissance':'03/03/2000', 'lieuDeNaissance':'', 'numeroDeTel': ''})
        self.assertEqual(response.status_code, 200) 
        
        response = self.client.post(reverse('BDD.views.watch',args=[3,1]),{'nom': 'a', 'uv':'1'}) 
        self.assertEqual(response.status_code, 200)        
        
        response = self.client.post(reverse('BDD.views.watch',args=[4,1]),{'typeCour': 'a', 'salles':'1', 'jour':'1', 'semaineMin':'1', 'semaineMax':'1', 'hmin':'1', 'hmax':'1'}) 
        self.assertEqual(response.status_code, 200)  
        
        
        
        if allll:
            tables=range(0,9)
            filtres=range(0,5)
            page=[x for x in range(0,3)]
            #page.append(None)
            nbparpage=[3, 40, 10000]
            nomClasser=[x for x in range(0,3)]
            #nomClasser.append(None)
            nomClasser.append(100)
            plusoumoi=[1,0]
            for t in tables:
                for f in filtres:
                    for p in page:
                        for n in nbparpage:
                            for nc in nomClasser:
                                for pm in plusoumoi:
                                    response = self.client.get(reverse('BDD.views.watch',args=[t,f,p,n,nc,pm]))
                                    self.assertEqual(response.status_code, 200) 
                                
            
        
        
        
    def test_admin(self):    
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('BDD.views.administration'))
        
        self.assertEqual(response.status_code, 200)
        self.client.login(username='john3', password='john3password')
        response = self.client.get(reverse('BDD.views.administration'))
        
        self.assertEqual(response.status_code, 200)
        self.client.login(username='john4', password='john4password')
        response = self.client.get(reverse('BDD.views.administration'))
        
        self.assertNotEqual(response.status_code, 200)
    def test_all(self):
        print()
        
        self.personne(self.alll)
        self.UV()
        self.module()
        self.typeCour()
        self.salle()
        self.Calendrier()
        self.Note()
        self.Groupe()
        self.watch()
        
    def personne(self, alll=False):
        self.listpers = []
        login = "l"
        if alll:
            ADRR = [None, "klqekljsqdjlqksjdq"]
            LIEU = [None, "lqsdkjqsdkj"]
            DATE = [None, datetime.now()]
            PROM = [None, 2012]
            n = 121212121
            NUMB = [None, n]
            EMAILl = [None, "lol@cieux.ci"]
            
            for adresse in ADRR:
                for lieuDeNaissance in LIEU:
                    for dateDeNaissance in DATE:
                        for promotion in PROM:
                            for numeroDeTel in NUMB:
                                for email in EMAILl:
                                    for sexe in SEXE:
                                        for typeP in TYPE:
                                            nom = "mdr"
                                            prenom = "mdr2"
                                            login = login + "l"
                                            mdp = "smdkqsmldkqslmdkqmlsdk"
                                            repo = addPersonne(self.puser, nom, prenom, login, mdp, sexe[0], typeP[0], adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, email)
                                            self.assertFalse(type(repo) is str)
                                            self.listpers.append(repo)
                                            
        else:
            self.listpers.append(addPersonne(self.puser, "jean", "jean", login, "1234567", SEXE[1][0], TYPE[1][0]))
        deux=addPersonne(self.puser, "jean", "jean", login, "1234567", SEXE[1][0], TYPE[1][0])                             
        self.assertTrue(type(deux) is str)
    def UV(self):
        idd = addUV(self.puser, "jean")
        self.assertFalse(type(idd) is str)
        
        self.uvs = [UV.objects.get(id=idd)]
        idd2 = addUV(self.puser, "jean")
        self.assertTrue(type(idd2) is str)
        
        
    def module(self):
        repo = addModule(self.puser, "uv", choice(self.uvs))
        self.assertFalse(type(repo) is str)
        self.modules = [repo]
        repo3 = addModule(self.puser, "uv", choice(self.uvs))
        self.assertTrue(type(repo3) is str)
        
        
    def typeCour(self):
        EXAM = [None, True, False]
       
        PROF = [None, [self.puser], [self.puser, choice(self.listpers)]]
        noms = "a"
        self.typecours = []
        for exa in EXAM:
            for prof in PROF:
                repo = addCour(self.puser, noms, isExam=exa, profs=prof)
                self.assertFalse(type(repo) is str)
                self.typecours.append(repo)
                noms = noms + "a"
        repo = addCour(self.puser, "a")
        
        self.assertTrue(type(repo) is str)
    def salle(self):
        self.salles=[]
        CAPACITE=[100, None]
        if self.alll:
            TYPE=[x[0] for x in SALLES]
        else:
            TYPE=[SALLES[1][0]]
        TYPE.append(None)
        nom="1"
        for typee in TYPE:
            for capa in CAPACITE:
                
                repo=addSalle(self.puser, nom, capacite=capa, typee=typee)
                nom=nom+"1"
                self.assertFalse(type(repo) is str)
                self.salles.append(repo)
        repo=addSalle(self.puser, "1")
        self.assertTrue(type(repo) is str)
    
    def Calendrier(self):
        self.lessons=[]
        if self.alll:
            SEM=[x[0] for x in SEMAINE]
        else:
            SEM=[LUNDI]
        
        for typeC in self.typecours:
            for day in SEM:
                for sem in range(0,2):
                    repo=addCalendrier(self.puser, typeC, day, sem, 1, 0, 1, self.salles)
                    self.assertFalse(type(repo) is str)
                    self.lessons.append(repo)
        repo=addCalendrier(self.puser, self.typecours[0], LUNDI, 2, 1, 0, 1, self.salles)
        self.assertTrue(type(repo) is str)     
        repo=addCalendrier(self.puser, self.typecours[0], LUNDI, 0, 1, 2, 1, self.salles)
        self.assertTrue(type(repo) is str)   
    
    def Note(self):
        self.notes=[]
        if self.alll:
            PERSONNES=self.listpers
        else:
            PERSONNES=[self.listpers[0]]
        for mod in self.modules:
            for p in PERSONNES:
                repo=addNote(self.puser,3,p,mod, self.puser)
                self.assertFalse(type(repo) is str)
                self.notes.append(repo)
    def Groupe(self):
        self.groupes=[]
        nom="a"
        PERS=[None, self.listpers]
        Mod=[None, self.modules]
        for mod in Mod:
            for pers in PERS:
                
                repo=addGroupe(self.puser,nom, personnes=pers, modules=mod)
                self.assertFalse(type(repo) is str)   
                self.groupes.append(repo)
                nom=nom+"a"
        repo=addGroupe(self.puser,"a")
        self.assertTrue(type(repo) is str)           
        
        
    
    