
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from model_mommy import mommy

from BDD.choices import FEMME_STATUT, PROF_STATUT, ELEVE_STATUT, Choix, \
    findchoice, TYPE, HOMME_STATUT
from BDD.forms import changeModule
from BDD.lookups import UVLookup
from BDD.models import UV, Personne, Module, Groupe, Salle, Note


class SimpleFormTestCase(TestCase):
    
      
    def test_changeCour(self):
       
        uv = mommy.make(UV)
        data = {'nom': "8.8", 'uv': uv.id,}
        form = changeModule(data=data)
        self.assertTrue(form.is_valid())  
      
        
        
    def test_changeModule(self):
        "Submit valid data."
        uv = mommy.make(UV)
        data = {'nom': "8.8", 'uv': uv.id,}
        form = changeModule(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        "Thing is required but missing."
        data = {
            'changeModule_0': 'Foo',
            'changeModule_1': '',
        }
        form = changeModule(data=data)
        self.assertFalse(form.is_valid())
class ThingLookupTestCase(TestCase):
 
    def setUp(self):
        self.factory = RequestFactory()
        self.uv = UV.objects.create(nom='8.8')
        self.uv2 = UV.objects.create(nom='8.88')
        self.uv3 = UV.objects.create(nom='7.88')
        self.lookup = UVLookup()
         
 
    def test_results(self):
        "Test full response."
        request = self.factory.get("/", {'term': '8.8'})
        response = self.lookup.get_query('8.8', request)
        
        self.assertEqual(2, len(response))
        
 
    



class ChoiceTest(TestCase):
    def test_findchoice(self):
        self.assertNotEqual(findchoice(PROF_STATUT,TYPE),"" )
        for c in Choix:
            for a in c:
                
                self.assertNotEqual(findchoice(a[0],c),"" )
    
    
# models test
class UVTestMommy(TestCase):
    
    def test_UV_creation_mommy(self):
        what = mommy.make(UV)
        self.assertTrue(isinstance(what, UV))
        self.assertEqual(what.__str__(), what.nom)
    
    def test_Personnes_creation_mommy(self):
        user=User(first_name = "Nom", last_name = "Prenom", username ="AbdelKuvin", password="KuvinAbdel679")
        self.assertTrue(isinstance(user,User))
        user.save()
        p= Personne()
        p.sexe=FEMME_STATUT
        p.type=PROF_STATUT
        p.user=user
        self.assertTrue(isinstance(p,Personne))
        p.save()                
        self.assertEqual(p.__str__(), p.filter)
        
    def test_Module_creation_mommy(self):
        uv=UV(nom="4.9")
        self.assertTrue(isinstance(uv,UV))
        uv.save()
        m=Module(nom="Jean Edmond, le module des champions", uv=uv)
        self.assertTrue(isinstance(m,Module))
        m.save()
        self.assertEqual(m.__str__(), "%s - %s" % (m.nom, m.uv.nom))
               
    def test_Salle_creation_mommy(self):
        s=Salle(nom="32")
        self.assertTrue(s,Salle)
        self.assertEqual(s.__str__(),s.nom)
    
        s2=Salle(nom="45",capacite="99")
        self.assertTrue(s2,Salle)
        self.assertEqual(s2.__str__(),s2.nom)
        
    def test_Groupe_creation_mommy(self):
        grp = Groupe()
        grp.nom = "Nom2Groupe"
        self.assertTrue(isinstance(grp,Groupe))
        self.assertEqual(grp.__str__(),grp.nom)
        grp2 = Groupe()
        grp2.nom = "Nom3Groupe"
        user=User(first_name = "Nom2Mec", last_name = "Nom3Mec", username ="AbdulKevin", password="KevinAbdul")
        self.assertTrue(isinstance(user,User))
        user.save()
        p= Personne()
        p.sexe=HOMME_STATUT
        p.type=ELEVE_STATUT
        p.user=user
        self.assertTrue(isinstance(p,Personne))
        p.save()
        grp2.save()
        self.assertTrue(isinstance(grp2,Groupe))
        grp2.personnes.add(p)
        
        self.assertEqual(grp2.__str__(),grp2.nom)   
        
    def test_Model_creation_mommy(self):
        uv = mommy.make(UV)
        module = mommy.make(Module)
        self.assertTrue(isinstance(uv, UV))
        self.assertTrue(isinstance(module, Module))
        self.assertEqual(uv.__str__(), uv.nom)
        self.assertEqual(module.__str__(), ("%s - %s" % (module.nom, module.uv.nom)))
        
    def test_Notes_creation_mommy(self):
        user=User(first_name = "Nom2Mec", last_name = "Nom3Mec", username ="AbdulKevin", password="KevinAbdul")
        self.assertTrue(isinstance(user,User))
        user.save()
        p1= Personne()
        p1.sexe=HOMME_STATUT
        p1.type=ELEVE_STATUT
        p1.user=user
        self.assertTrue(isinstance(p1,Personne))
        p1.save()
        
        uv=UV(nom="4.9")
        self.assertTrue(isinstance(uv,UV))
        uv.save()
        m=Module(nom="Jean Edmond, le module des champions", uv=uv)
        self.assertTrue(isinstance(m,Module))
        m.save()
        
        user=User(first_name = "Nom2Prof", last_name = "Nom3Prof", username ="Prof", password="Purofu")
        self.assertTrue(isinstance(user,User))
        user.save()
        p2= Personne()
        p2.sexe=HOMME_STATUT
        p2.type=ELEVE_STATUT
        p2.user=user
        self.assertTrue(isinstance(p2,Personne))
        p2.save()
        
        note = Note(note=0, personne=p1, module=m, prof=p2)
        note.save()
