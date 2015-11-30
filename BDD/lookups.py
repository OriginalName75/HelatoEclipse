'''
Created on 19 nov. 2015

@author: mabadie_2
'''
from ajax_select import register, LookupChannel
from django.db.models.query_utils import Q
from django.utils.html import escape

from BDD.models import Personne, Groupe, Module, UV


@register('uv')
class UVLookup(LookupChannel):
    model = UV
    
    def get_query(self, q, request):
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.nom


@register('personnes')
class PersonLookup(LookupChannel):
    model = Personne
    
    def get_query(self, q, request):
        return self.model.objects.filter(filter__icontains=q).order_by('filter')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.filter

@register('module')
class ModuleLookup(LookupChannel):
    model = Module
    
    def get_query(self, q, request):
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        stri= item.uv.nom + " - " + item.nom
        return u"<span class='tag'>%s</span>" % stri

@register('groupes')
class GroupeLookup(LookupChannel):

    model = Groupe

    def get_query(self, q, request):
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.nom