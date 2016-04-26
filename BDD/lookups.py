"""
    The ''lookups'' module
    ======================
    
    To customize ajax_select


@author: IWIMBDSL
"""
from ajax_select import register, LookupChannel
from BDD.models import Personne, Groupe, Module, UV, Salle, TypeCour


@register('uv')
class UVLookup(LookupChannel):
    """
       It customize UV research in a field form 
    
    """
    model = UV
    
    def get_query(self, q, request):
        """
            search in the database what the user has written in the field. 
            
        :param q: what the user has written in the field
        :type q: string
        :param request: Django request
        :type request: request
        :return: all the UVs which the name contains what the user has written in the field
        :rtype: list of UVs
        
        """
        
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        """
            It define how the ajax_select prints the responses of a search
            
        :param item: 
        :type item:
        :return: what's going to be printed in the form field
        :rtype: string
        
        """
        return u"<span class='tag'>%s</span>" % item.nom


@register('personnes')
class PersonLookup(LookupChannel):
    """
       It customize persons research in a field form 
    
    """
    model = Personne
    
    def get_query(self, q, request):
        """
            search in the database what the user has written in the field. 
            
        :param q: what the user has written in the field
        :type q: string
        :param request: Django request
        :type request: request
        :return: all the persons which the first name and last name contains what the user has written in the field
        :rtype: list of Personne
        
        """
        
        return self.model.objects.filter(filter__icontains=q).order_by('filter')[:50]

    def format_item_display(self, item):
        """
            It define how the ajax_select prints the responses of a search
            
        :param item: 
        :type item:
        :return: what's going to be printed in the form field
        :rtype: string
        
        """
        return u"<span class='tag'>%s</span>" % item.filter
 
@register('typeCour')
class typeCourLookup(LookupChannel):
    """
       It customize types of lesson research in a field form 
    
    """
    model = TypeCour    
    def get_query(self, q, request):
        """
            search in the database what the user has written in the field. 
            
        :param q: what the user has written in the field
        :type q: string
        :param request: Django request
        :type request: request
        :return: all the types of lesson which the name contains what the user has written in the field
        :rtype: list of Cour
        
        """
        
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        """
            It define how the ajax_select prints the responses of a search
            
        :param item: 
        :type item:
        :return: what's going to be printed in the form field
        :rtype: string
        
        """
        return u"<span class='tag'>%s</span>" % item.nom   
    
@register('salles')
class SalleLookup(LookupChannel):
    """
       It customize classroom research in a field form 
    
    """
    model = Salle
    
    def get_query(self, q, request):
        """
            search in the database what the user has written in the field. 
            
        :param q: what the user has written in the field
        :type q: string
        :param request: Django request
        :type request: request
        :return: all the classrooms which the name contains what the user has written in the field
        :rtype: list of classrooms
        
        """
        
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        """
            It define how the ajax_select prints the responses of a search
            
        :param item: 
        :type item:
        :return: what's going to be printed in the form field
        :rtype: string
        
        """
        return u"<span class='tag'>%s</span>" % item.nom

@register('module')
class ModuleLookup(LookupChannel):
    """
       It customize module research in a field form 
    
    """
    model = Module
    
    def get_query(self, q, request):
        """
            search in the database what the user has written in the field. 
            
        :param q: what the user has written in the field
        :type q: string
        :param request: Django request
        :type request: request
        :return: all the modules which the name contains what the user has written in the field
        :rtype: list of modules
        
        """
        
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        """
            It define how the ajax_select prints the responses of a search
            
        :param item: 
        :type item:
        :return: what's going to be printed in the form field
        :rtype: string
        
        """
        stri= item.uv.nom + " - " + item.nom
        return u"<span class='tag'>%s</span>" % stri

@register('groupes')
class GroupeLookup(LookupChannel):
    """
       It customize group research in a field form 
    
    """

    model = Groupe

    def get_query(self, q, request):
        """
            search in the database what the user has written in the field. 
            
        :param q: what the user has written in the field
        :type q: string
        :param request: Django request
        :type request: request
        :return: all the groups which the name contains what the user has written in the field
        :rtype: list of groups
        
        """
        return self.model.objects.filter(nom__icontains=q).order_by('nom')[:50]

    def format_item_display(self, item):
        """
            It define how the ajax_select prints the responses of a search
            
        :param item: 
        :type item:
        :return: what's going to be printed in the form field
        :rtype: string
        
        """
        return u"<span class='tag'>%s</span>" % item.nom