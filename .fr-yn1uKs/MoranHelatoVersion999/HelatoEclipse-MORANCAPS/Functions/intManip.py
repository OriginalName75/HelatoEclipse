'''
Created on 26 oct. 2015

@author: Moran
'''
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False