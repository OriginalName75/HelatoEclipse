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

@register.filter
def index(List,i):
    return List[int(i)]

@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.
    
    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """
    
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value
    
    
    
    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value
    
    # Cut the string
    value = value[:limit]
    
    # Break into words and remove the last
    words = value.split(' ')[:-1]
    
    # Join the words and return
    return ' '.join(words) + '...'

