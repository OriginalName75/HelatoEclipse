
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from model_mommy import mommy

from BDD.choices import FEMME_STATUT, PROF_STATUT, ELEVE_STATUT, Choix, \
    findchoice, TYPE
from BDD.forms import changeModule
from BDD.lookups import UVLookup
from BDD.models import UV, Personne, Module


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
        
        
        
    def test_Model_creation_mommy(self):
        uv = mommy.make(UV)
        module = mommy.make(Module)
        self.assertTrue(isinstance(uv, UV))
        self.assertTrue(isinstance(module, Module))
        self.assertEqual(uv.__str__(), uv.nom)
        self.assertEqual(module.__str__(), ("%s - %s" % (module.nom, module.uv.nom)))
        
    def test_Personne_creation_mommy(self):
        user = mommy.make(User)
        personne = mommy.make(Personne)
        self.assertTrue(isinstance(user, User))
        self.assertTrue(isinstance(personne, Personne))
        self.assertEqual(personne.__str__(), personne.filter)
    

