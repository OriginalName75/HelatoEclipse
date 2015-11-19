'''
Created on 30 oct. 2015

@author: mabadie_2
'''
from django import template

register = template.Library()
@register.filter(is_safe=True)
def getS(model,arg):
    return getattr(model, arg)
@register.filter(is_safe=True)
def getSD(model,arg):
    return getattr(model, arg)()
    