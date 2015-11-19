'''
Created on 28 oct. 2015

@author: Moran
'''
from _functools import reduce
import operator

from django.db.models import Q


def select(table, plus=None, column=None, page=None, nbparpage=None, listFiltre=None):
    
    if listFiltre == None:
        n = table.objects.count()
        
        if plus == None or column == None:
            if page == None or nbparpage == None or n <= nbparpage:
                var = table.objects.all()
            else:
                var = table.objects.all()[((page - 1) * nbparpage):(page * nbparpage)]    
        else:    
            if page == None or nbparpage == None or n <= nbparpage:
                var = table.objects.all().order_by(plus + column)
            else:
                var = table.objects.all().order_by(plus + column)[((page - 1) * nbparpage):(page * nbparpage)] 
    else:
        objets_q = [Q(x) for x in listFiltre]
        n = table.objects.filter(reduce(operator.and_, objets_q)).count()
        if plus == None or column == None:
            if page == None or nbparpage == None or n <= nbparpage:
                var = table.objects.filter(reduce(operator.and_, objets_q))
            else:
                var = table.objects.filter(reduce(operator.and_, objets_q))[((page - 1) * nbparpage):(page * nbparpage)]    
        else:    
            if page == None or nbparpage == None or n <= nbparpage:
                var = table.objects.filter(reduce(operator.and_, objets_q)).order_by(plus + column)
            else:
                var = table.objects.filter(reduce(operator.and_, objets_q)).order_by(plus + column)[((page - 1) * nbparpage):(page * nbparpage)]   

    
    return [var, n]
    
