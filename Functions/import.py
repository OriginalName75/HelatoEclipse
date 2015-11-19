'''
Created on 29 oct. 2015

@author: mabadie_2
'''
def importPersonne(upload):
    with open(upload) as f:
        content = f.readlines()
        