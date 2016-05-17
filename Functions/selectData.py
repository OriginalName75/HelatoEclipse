"""
    The ''selectData'' module
    ======================
    
    Functions to select data
    
    
    
@author: IWIMBDSL
"""
from _functools import reduce
import operator

from django.db.models import Q


def select(table, plus=None, column=None, page=None, nbparpage=None, listFiltre=None):
    """
        Select data depends if it is filtered or not, sorted or not etc..
        
    :param table: define in which model the object is.
    :type table: int   
    :param plus: if equals to '-', sort by descending order; if '' in the ascending order
    :type plus: string
    :param column: which column to sort
    :type column: string
    :param page: defines which page is printed. 
    :type page: int
    :param nbparpage: defines how many object are printed every pages. if None it is all in 1 page             
    :type nbparpage: int 
    :param listFiltre:  lists of filter conditions
    :type listFiltre: list of string
    :return: the list of objects and the total nmber of ibjetc in the database
    :rtype: list Model, int
    
    """
    if page != None and int(page)<1:
        page=1
    if listFiltre == None:
        n = table.objects.filter(isvisible=True).count()
        
        if plus == None or column == None or column=="error":
            if page == None or nbparpage == None or n <= nbparpage:
                var = table.objects.filter(isvisible=True)
            else:
                var = table.objects.filter(isvisible=True)[((page - 1) * nbparpage):(page * nbparpage)]    
        else:    
            if page == None or nbparpage == None or n <= nbparpage:
                var = table.objects.filter(isvisible=True).order_by(plus + column)
            else:
                var = table.objects.filter(isvisible=True).order_by(plus + column)[((page - 1) * nbparpage):(page * nbparpage)] 
    else:
        objets_q = [Q(x) for x in listFiltre]
        n = table.objects.filter(isvisible=True and reduce(operator.and_, objets_q)).count()
        if plus == None or column == None or column=="error":
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
    

