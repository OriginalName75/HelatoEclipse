# -*- coding: utf-8 -*-
"""
    The ''views'' module
    ======================
    
    It defines the variables used in the templates. It is the link between the URL and the templates.
    Templates are html codes mixed with Django code.   
    
   Users must be connected to their account in all the pages (but connection of course). 
   If not they will be redirected.
    
    :Exemple:
    
    >> index() 
    returns an http response of the template index.html
    
    .. seealso:: urls.py to know the urls which link to the wiews
    
    
@author: IWIMBDSL
"""
from datetime import datetime

from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render

from BDD import forms
from BDD.choices import PROF_STATUT
from BDD.forms import nbAjout
from BDD.models import Personne, News
from Eleve.views import menu
from Functions import  data
from Functions import generator
from Functions.Ctrlz import Ctrlz
from Functions.delete import supr_salles
from Functions.news import addN
from Functions.selectData import select
from language import connexion


@login_required(login_url='/connexion')
def index(request, plus=0):
   
   
        
        if request.user.is_superuser or int(request.user.personne.type) == PROF_STATUT :
            return administration(request, plus)
        else :
            return menu(request, plus)
        
        

@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def administration(request, plus=0):
    """
        Define what is in the admin and teacher index page of the template admin.html.
        Links are define in this template to the data of the website.
        
        
    :param request: Class that give many information like POST, GET and user data.
    :type request: Request
    :param plus: For the news. If plus>0, the plusth news will be clarified.
    :type plus: int
    :return: What the user is going to view on his screen 
    :rtype: HttpResponse
    
    """
    print(plus)
    PR = PROF_STATUT
    isProf= request.user.personne.type==PROF_STATUT
    plus = int(plus)
    new = News.objects.filter(personne__id__icontains=request.user.personne.id).order_by('-id')
    maxx = new.count()
    ajou = 0
    news = []
    l = 0
    i = 0
    fff = 0
    plus2 = 0
    nb = 1
    first = True
    #===========================================================================
    #                                 NEWS                                     
    #===========================================================================
    
    if maxx > 0:
        while l < 10 and i < maxx:
            obj = new[i]
            t = obj.type * 100 + obj.typeG
            if i < maxx - 1:
                obj2 = new[i + 1]
                tapres = obj2.type * 100 + obj2.typeG
            else:
                tapres = -2
            if t == tapres:
                nb = nb + 1
                
                txt = addN(obj, nb, not plus == plus2 + 1, plus2 + 1)
                if first:
                    fff = ajou
                    news.append(txt)
                    ajou = ajou + 1
                    
                else:
                    
                    news[fff] = txt
              
                first = False
                if plus == plus2 + 1:
                    
                    news.append(obj.txt)
                    ajou = ajou + 1
            else:
                l = l + 1   
                if nb == 1 or plus == plus2 + 1:
                    news.append(obj.txt)
                    ajou = ajou + 1
                plus2 = plus2 + 1
                nbbbb = 1
                nb = 1
                first = True
            i = i + 1 
            tavant = t
            
    
    
    text=[]
        
        
    if request.method == 'POST':
        form = forms.langage(request.POST)  
        if form.is_valid(): 
            strr = form.cleaned_data['txt']
            if strr!="clear":
                
                reponse = connexion.connect(strr, request.user.personne.id)
                strr = ">>> " + strr
                if not 'argg' in request.session or not request.session['argg']:
                    request.session['argg'] = [strr]
                else:
                    saved_list = request.session['argg']
                    saved_list.append(strr)
                    request.session['argg'] = saved_list
                
                if not 'resp' in request.session or not request.session['resp']:
                    request.session['resp'] = [reponse]
                else:
                    
                    saved_list = request.session['resp']
                    saved_list.append(reponse)
                    request.session['resp'] = saved_list   
            else:
                request.session['argg'] = []
                request.session['resp'] = []
    ii=0
    if not 'argg' in request.session or not request.session['argg']:  
        request.session['argg'] = []
                
        request.session['resp'] =[]     
    for x in request.session['argg']:
        text.append([x,request.session['resp'][ii]])
        ii=ii+1
    text=reversed(text)    
    
    
    form = forms.langage()    
     
    return render(request, 'BDD/ADMIN/admin.html', locals())    


@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def fiche(request, table, idP, filtre=None, page=None, nbparpage=None, nomClasser=None, plusOuMoins=None):
    """
        It defines the variables used in the template fiche.html, which show specifications of an object in the database.
    
    :param request: Class that give many information like POST, GET and user data.
    :type request: Request    
    :param table: define in which model the object is.
    :type table: int
    :param idP: Id of the object
    :type idP: int
            
            the variable bellow are there so when the user press the buttom back
            he has the same specification as before in the view watch.
            
    :param filtre: if = 1, filter forms are printed. if =2, filter forms are printed
                    and the user has filtered the data. Else, forms no printed, no filters.
    :type filtre: int
    :param page: defines which page is printed. If None, it is the first page.
    :type page: int
    :param nbparpage: defines how many object are printed every pages. if None it is 40. 
                      If 10000 its all of them in one page
    :type nbparpage: int 
    :param nomClasser: Which column is sorted. if None or = 100, nothing is sorted.
    :type nomClasser: int
    :param plusOuMoins:  if None or 0, data is sorted in ascending order, else in descending order.
    :type plusOuMoins: int 
    :return: What the user is going to view on his screen 
    :rtype: HttpResponse
    
    :Exemple:
    
    >> fiche(request, 1, 3)
    Will return the http response of the page that show specificatin of the object which the id = 3 
    and is in the group database (table = 1 represents group database)
    
    .. warnings:: the id is in the url but the user is an admin or a teacher.
    
    
    """
    table = int(table)
    allllll = 'all'
    isProf= request.user.personne.type==PROF_STATUT
    TABBLE = data.table(table)
    if not TABBLE.objects.filter(id=int(idP)).count() > 0:
        return http.HttpResponseRedirect('/')
    if not request.user.is_superuser and table != 6:
        return http.HttpResponseRedirect('/')
    
    obj = TABBLE.objects.get(id=int(idP))
    if not request.user.is_superuser and table == 6:
        if obj.prof.id!=request.user.personne.id:
            return http.HttpResponseRedirect('/')
    listeliste = data.listinside(table)
    listetab = data.listTable(table)
    MODEL=data.table(table)()
    if hasattr(MODEL,'links'):
        links = MODEL.links()
    else:
        links=[]
    entier = 0
    soustable = data.soustable(table)
    titrest = []
    
    #===========================================================================
    #                      Many to many obects
    #===========================================================================
    for st in soustable:
    
        if st[0] == 0:
            titrest.append([st[0], st[2], getattr(obj, st[3][0]).all(), st[3][1], st[4]])
        elif st[0] == 1:
            titrest.append([st[0], st[2], getattr(obj, st[3][0]).all(), st[4]])
    
    return render(request, 'BDD/ADMIN/fiche.html', locals())    



@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def ajouter(request, table, nbajout, filtre, page, nbparpage, nomClasser, plusOuMoins, first=True):
    """
        It defines the variables used in the template ajouter.html, which print 
        forms to add one or mutltiple objects.
    
    :param request: Class that give many information like POST, GET and user data.
    :type request: Request    
    :param table: define in which model the object is.
    :type table: int
    :param first: Is it the first time ajouter() has been call ?
    :type first: boolean
    :param nbajout: if 0, print forms to know how many object the user want to add.
                    if 100, add object for a manyto many relation ex: notes for a group
                    if >100, the objcts are added in a session after =100
                    if not, it adds nbajout forms to add nbajout objects.
    :type nbajout: int
            
            the variable bellow are there so when the user press the buttom back
            he has the same specification as before in the view watch.
            
    :param filtre: if = 1, filter forms are printed. if =2, filter forms are printed
                    and the user has filtered the data. Else, forms no printed, no filters.
    :type filtre: int
    :param page: defines which page is printed. If None, it is the first page.
    :type page: int
    :param nbparpage: defines how many object are printed every pages. if None it is 40. 
                      If 10000 its all of them in one page
    :type nbparpage: int 
    :param nomClasser: Which column is sorted. if None or = 100, nothing is sorted.
    :type nomClasser: int
    :param plusOuMoins:  if None or 0, data is sorted in ascending order, else in descending order.
    :type plusOuMoins: int 
    :return: What the user is going to view on his screen 
    :rtype: HttpResponse
    
    :Exemple:
    
    >> ajouter(request, 1, 3, 0, 1, 12, 0, 0)
    Will return the http response of the page that print 3 forms to add 3
    groups in the database (table = 1 represents group database).
    All the other parameters (after 3) are the previous parameter of the view watch.
    
    .. warnings:: if the user play with nbajout in the url, he will be redirected to index.hmlt
    if he doesn't do it correctly (so no errors occurs)
    
    """
    
    isProf= request.user.personne.type==PROF_STATUT
    nbajout = int(nbajout)
    table = int(table)
    MODEL=data.table(table)()
    if hasattr(MODEL,'ajouterPlusieurs'):
       
       
        AJJ=MODEL.ajouterPlusieurs()
        
    else:
        AJJ=None
    if not request.user.is_superuser and table != 6:  # case of teacher
        return http.HttpResponseRedirect('/')
    #ajj = data.ajouterA(table)
    ficheAfter = False
    if nbajout > 0 and nbajout != 100:
        
        listeform = range(0, nbajout)
        if hasattr(MODEL,'quiery'):
            lquery = MODEL.quiery()
        else:
            lquery =[]
        table = int(table)
        envoi = False
        #===========================================================================
        #      Nb ajout normal. No many to many relations
        #===========================================================================
        if nbajout < 100:
            
            if data.form(request.user, table, 3) == None:
                Formset = formset_factory(data.form(request.user, table, 1), extra=nbajout)
            else:
                
                Formset = formset_factory(data.form(request.user, table, 1), extra=nbajout, formset=data.form(request.user, table, 3))
            if request.method == 'POST' and first:
             
                formset = Formset(request.POST, request.FILES)
                if formset.is_valid():
                    
                    nbajout = 0  
                    envoi = True
                    
                    
                    for form in formset:
                        
                        idP = form.save(request.user.personne)
                        
                    
                form = nbAjout()
                           
            else:
                formset = Formset() 
        #===========================================================================
        #      Many to many relations, the user has already write the forms
        #      to know which many to many relations exactly
        #===========================================================================
        else:
            if 'stock' not in request.session:
                return http.HttpResponseRedirect('/')
            stock = request.session['stock']
            solo = []
            multi = []
            i = 0
            
            if AJJ!=None:
                
                for x in AJJ.listFieldForm:
                    if i==0:
                        kwargs = {
                            AJJ.QCode: stock[i]
                        }
                        a = AJJ.listModel[i].objects.filter(**kwargs)
                        nb = a.count()
                        Formset = formset_factory(AJJ.form, extra=nb, formset=AJJ.baseForm)
                        
                        if request.method == 'POST' and first:
                           
                            formset = Formset(request.POST, request.FILES)
                        
                                
                        else:
                            formset = Formset()
                        b = []
                        ii = 0
                        for aa in a:
                            b.append([aa, formset[ii]])
                            ii += 1
                            
                        multi.append(b)
                        
                        
                    else:
                        solo.append(AJJ.listModel[i].objects.get(id=stock[i]))
                    i += 1
                    
            if request.method == 'POST' and first:
                if formset.is_valid():
                    jj = 0
                    for f in formset:
                        if table == 6:
                            f.save(request.user.personne, solo, [x[jj] for x in multi], request.user.personne)
                        else:
                            f.save(request.user.personne, solo, [x[jj] for x in multi])
                        jj += 1
                    nbajout = 0  
                    return http.HttpResponseRedirect('/watch/' + str(table) + '/' + str(filtre))
            
    else:
        if request.method == 'POST':
            #===========================================================================
            #      Normal nb ajout. no many to many relations. 
            #      print forms to know how much
            #===========================================================================
            if AJJ == None or nbajout < 100:
                
                form = nbAjout(request.POST)
                
                if form.is_valid():
                    nb = form.cleaned_data['nb']
                    
                    return ajouter(request, table, nb, filtre, page, nbparpage, nomClasser, plusOuMoins, False)
                else:
                    if AJJ != None:
                        formAjj = AJJ.formInit()
            #===========================================================================
            #      Many to many relations,print the forms
            #      to know which many to many relations 
            #===========================================================================
            else:
                formAjj = AJJ.formInit(request.POST)
                stock = []
                if formAjj.is_valid():
                    i=0
                    for x in AJJ.listFieldForm:
                        if i == 0:
                            stock.append(formAjj.cleaned_data[x])
                        else:
                            stock.append(formAjj.cleaned_data[x].id)
                        i=i+1
                    request.session['stock'] = stock
                    return ajouter(request, table, 101, filtre, page, nbparpage, nomClasser, plusOuMoins, False)
        else:
            if AJJ != None:
                
                formAjj = AJJ.formInit()
            form = nbAjout() 
            
            
    return render(request, 'BDD/ADMIN/ajouter.html', locals())


@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def delete(request, table, idP, filtre, page, nbparpage, nomClasser, plusOuMoins, supri):
    """
        It defines the variables used in the template delete.html, which print 
        forms to delete an objects.
    
    :param request: Class that give many information like POST, GET and user data.
    :type request: Request    
    :param table: define in which model the object is.
    :type table: int
    :param idP: Is it the id of the object to delete
    :type idP: int
    :param supri: if 1, the obeject has been deleted or delete it, else not
    :type supri: int
            
            the variable bellow are there so when the user press the buttom back
            he has the same specification as before in the view watch.
            
    :param filtre: if = 1, filter forms are printed. if =2, filter forms are printed
                    and the user has filtered the data. Else, forms no printed, no filters.
    :type filtre: int
    :param page: defines which page is printed. If None, it is the first page.
    :type page: int
    :param nbparpage: defines how many object are printed every pages. if None it is 40. 
                      If 10000 its all of them in one page
    :type nbparpage: int 
    :param nomClasser: Which column is sorted. if None or = 100, nothing is sorted.
    :type nomClasser: int
    :param plusOuMoins:  if None or 0, data is sorted in ascending order, else in descending order.
    :type plusOuMoins: int 
    :return: What the user is going to view on his screen 
    :rtype: HttpResponse
    
    :Exemple:
    
    >> delete(request, 1, 3, 0, 1, 1, 2, 0, 0)
    Will return the http response of the page that ask if the user is sure if he wants to delete
    the object that the id=3 and a group in the database (table = 1 represents group database).
    The last parameter is 0 that is why it is an 'are you sure' page.
    All the other parameters (after 3) but the last one are the previous parameter of the view watch.
    
    >> delete(request, 1, 3, 0, 1, 1, 2, 0, 1)
    On the other hand, it will return the http response of the page that print that the 
    the user has deleted the object successfully
    
    
    .. warnings:: the id is in the url but if the user is a teacher and not an admin, 
    he can delete only his own adds. Only an admin has to care about using urls.
    
    
    """

    isProf= request.user.personne.type==PROF_STATUT
    supr = False
    table = int(table)
    if not request.user.is_superuser and table != 6:
        return http.HttpResponseRedirect('/')
    if not data.table(table).objects.filter(id=int(idP)).count() > 0:
        return http.HttpResponseRedirect('/')
    p = data.table(table).objects.get(id=int(idP))
    #===========================================================================
    # if 1, delete
    #===========================================================================
    if int(supri) == 1:
        
        obj = data.table(table).objects.get(id=int(idP))
        if not request.user.is_superuser and table == 6:
            if request.user.personne.id != obj.personne.id:
                return http.HttpResponseRedirect('/')
        supr_salles(table, idP, request.user.personne)
        
        
       
        supr = True
    
    
    return render(request, 'BDD/ADMIN/delete.html', locals())
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def randomP(request):
    """
        Génération aléatoire.
        
    """
        
    
    
    if not hasattr(request.user, 'personne'):
        p = Personne()
        p.user = request.user
        p.filter = "Superadmin"
        p.save()
        request.user.first_name = "Dieu"
        request.user.last_name = "Tout puissant"
        request.user.save()
        
    generator.personnes(request.user.personne, 300, True)  
    generator.groupe(10, True)
    generator.courType(200, True)
    generator.salles(2, 10, True)
     
    generator.uvs(3, 12, True)
    generator.module(4, True)
    generator.generEmploiedutemp()
    
   
    
    text = """done"""
    return HttpResponse(text)
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def langage(request):
    Ctrlz(5)
    return render(request, 'BDD/ADMIN/lang.html', locals())
# @login_required(login_url='/connexion')
# @user_passes_test(lambda u: u.is_superuser)
# def areusure(request, table, idP, what, filtre, page, nbparpage, nomClasser, plusOuMoins, nor, which):
#     """
#         Not used yet. Was used before.
#         Can be used later.
#     
#     """
#     table = int(table)
#     
#     if int(nor) == 0:
#         return render(request, 'BDD/ADMIN/areusure.html', locals())  
#     else:
#         TABBLE = data.table(table)
#         obj = TABBLE.objects.get(id=int(idP))
#         l = data.soustable(table)
#         for ll in l:
#             gr = getattr(obj, ll[3]).get(id=int(what))
#             getattr(obj, ll[3]).remove(gr)
#         return change(request, table, idP, 0, filtre, page, nbparpage, nomClasser, plusOuMoins, 0)
#     
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def change(request, table, idP, what, filtre, page, nbparpage, nomClasser, plusOuMoins, first=True):
    """
        It defines the variables used in the template change.html, which print 
        forms to change an object.
    
    :param request: Class that give many information like POST, GET and user data.
    :type request: Request    
    :param table: define in which model the object is.
    :type table: int
    :param idP: id of the object to change 
    :type idP: int
    :param what: if >0 the user want to change a manytomany relation.  
    :type what: int
    :param first: Is it the first time change() has been call ?
    :type first: boolean
            
            the variable bellow are there so when the user press the buttom back
            he has the same specification as before in the view watch.
            
    :param filtre: if = 1, filter forms are printed. if =2, filter forms are printed
                    and the user has filtered the data. Else, forms no printed, no filters.
    :type filtre: int
    :param page: defines which page is printed. If None, it is the first page.
    :type page: int
    :param nbparpage: defines how many object are printed every pages. if None it is 40. 
                      If 10000 its all of them in one page
    :type nbparpage: int 
    :param nomClasser: Which column is sorted. if None or = 100, nothing is sorted.
    :type nomClasser: int
    :param plusOuMoins:  if None or 0, data is sorted in ascending order, else in descending order.
    :type plusOuMoins: int 
    :return: What the user is going to view on his screen 
    :rtype: HttpResponse
    
    :Exemple:
    
    >> change(request, 1, 3, 0, 1, 0, 10, 1, 0)
    Will return the http response of the page that change the group (because table=1) and the id =3.
    what=0 so no many to many relations involved (yet).
    All the other parameters (after 3) are the previous parameter of the view watch.
    
    .. warnings:: admin or teacher in a specific view can change ids in the url.
    
    """
    isProf= request.user.personne.type==PROF_STATUT

    table = int(table)
    if not data.table(table).objects.filter(id=int(idP)).count() > 0 or table > 7:
        return http.HttpResponseRedirect('/')
    if not request.user.is_superuser and table != 6:
        return http.HttpResponseRedirect('/')
    soustable = data.soustable(table)
    TABBLE = data.table(table)
    obj = TABBLE.objects.get(id=int(idP))
    MODEL=data.table(table)()
    if hasattr(MODEL,'links'):
        links = MODEL.links()
    titrest = []
    formseti = None
    ii = 0
    changed = False
    stforms = data.formsoustable(table)
    #===========================================================================
    #  if user wants to change manytomany relations
    #===========================================================================
    if (first and request.method == 'POST' and int(what) > 0):
        for frm in stforms:
            instance = TABBLE.objects.get(id=int(idP))
            frm[0] = frm[0](request.POST, instance=instance)
        j = 1  
        for frm in stforms:
            
            if j == int(what) and frm[0].is_valid():
                frm[0].savePerso(int(idP), request.user.personne)
                changed = True
            j += 1
        return http.HttpResponseRedirect('')
    #===========================================================================
    # no post for manytyomany
    #===========================================================================
    else:
        
        stforms = data.formsoustable(table)
        for frm in stforms:
            instance = TABBLE.objects.get(id=int(idP))
            frm[0] = frm[0](instance=instance)
            
            
    #===========================================================================
    #  if user wants to change value
    #===========================================================================        
    if (first and request.method == 'POST' and int(what) == 0):
        
        form = data.form(request.user, table, 2, request.POST) 
        if form.is_valid():
            form.modif(idP, request.user.personne)    
            changed = True
    #===========================================================================
    #  No POST for value
    #===========================================================================          
    else:
       
        cond = []
        conditions = []
        
        form = data.form(request.user, table, 2)
        
        data.changecond(table, cond, conditions, obj)
         
        entier = 0
        for l in conditions:
            if cond[entier][1] == 1:
                form.fields[cond[entier][0]].initial = l.strftime('%d/%m/%Y')
            else:   
                form.fields[cond[entier][0]].initial = l
            entier = entier + 1 
    taille = len(stforms)
  
    for st in soustable:
        
        if ii < taille:
            
            if st[0] == 0:
                
                titrest.append([stforms[ii], st[0], st[2], [getattr(obj, st[3][0]).all(), st[3][1]], st[1]])
            else:
                
                titrest.append([stforms[ii], st[0], st[2], [getattr(obj, st[3][0], st[1]).all()], st[1]])
        else:
            break        
        ii = ii + 1  
    return render(request, 'BDD/ADMIN/change.html', locals())   
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def helpcustom(request):
    
    return render(request, 'BDD/ADMIN/help.html', locals())   
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def watch(request, table, filtre, page=None, nbparpage=None, nomClasser=None, plusOuMoins=None):
    """
        It defines the variables used in the template watch.html, which print 
        data. You can filter and sort data.
    
    :param request: Class that give many information like POST, GET and user data.
    :type request: Request    
    :param table: define in which model the object is.
    :type table: int   
    :param filtre: if = 1, filter forms are printed. if =2, filter forms are printed
              and the user has filtered the data. Else, forms no printed, no filters.
    :type filtre: int
    :param page: defines which page is printed. If None, it is the first page.
    :type page: int
    :param nbparpage: defines how many object are printed every pages. if None it is 40. 
                      If 10000 its all of them in one page
    :type nbparpage: int 
    :param nomClasser: Which column is sorted. if None or = 100, nothing is sorted.
    :type nomClasser: int
    :param plusOuMoins:  if None or 0, data is sorted in ascending order, else in descending order.
    :type plusOuMoins: int 
    :return: What the user is going to view on his screen 
    :rtype: HttpResponse
    
    :Exemple:
    
    >> watch(request, 1, 0, 1, 30, 1, 0)
    Will return the http response of the first page that print 30 groups per page (table=1),
    sorted by his first atribute (the name) in ascending order
    Filters forms wont be printed because filtre=0
    All the other parameters (after 3) are the previous parameter of the view watch.
    
    
    """
    isProf= request.user.personne.type==PROF_STATUT

    table = int(table)
    if not request.user.is_superuser and table != 6:
        return index(request)
    FILTRE = data.filtre(table)
    filtre = int(filtre)
    listAffich = data.listTable(table)
    listeliste = data.listinside(table)
    
    allllll = 'all'
    if page == None:
        page = 1
    else:
        page = int(page)
    if nomClasser == None:
        nomClasser = 100
    if plusOuMoins == None:
        plusOuMoins = 0   
    if nbparpage == None:
        nbparpage = 20
    else:
        nbparpage = int(nbparpage)       
    allP = False
    
    if nbparpage == 10000:
        allP = True 
    nomClasser = int(nomClasser)
    if int(plusOuMoins) == 0:
        plus = ''
    else:
        plus = '-'
    conditions = []
    cond = []
    #===========================================================================
    # if filters form are printed
    #===========================================================================
    if filtre > 0:
        #=======================================================================
        # if filter form has been validated
        #=======================================================================
        if request.method == 'POST':
           
            form = data.form(request.user, table, 0, request.POST)
                
            if form.is_valid():
                filtre = 2
                
                for f in FILTRE:
                    clean = form.cleaned_data[f[0]]
                    
                    if f[4] == 1:
                        cleancond = int(clean)
                    else:
                        cleancond = clean
                    if cleancond != f[2]:
                        
                        if f[4] == 2:
                            cleanf = clean.strftime('%Y-%m-%d')
                        elif f[4] == 3:
                            cleanf = str(clean)
                        elif f[4] == 4:
                            cleanf = clean.id
                        else:
                            cleanf = clean
                        
                        conditions.append((f[3], cleanf))
                        cond.append((f[1], 0))
                request.session['conditions'] = conditions
                request.session['cond'] = cond
                
        else:
            form = data.form(request.user, table, 0)
    #===========================================================================
    # filter forms are printed and the user has filtered the data
    #===========================================================================
    if filtre == 2 and conditions == []:
        try:
            conditions = request.session['conditions']
            
            cond = request.session['cond']
            if table == 6 and not request.user.is_superuser:
                    conditions.append(("prof", request.user.personne))
                    cond.append(("prof", 0))
            entier = 0
            for l in conditions:
                if cond[entier][1] == 1:
                    form.fields[cond[entier][0]].initial = (datetime.strptime(l[1], '%Y-%m-%d').date()).strftime('%d/%m/%Y')
                else:   
                    
                    form.fields[cond[entier][0]].initial = l[1]
                entier = entier + 1
        except:
            filtre = 0
    #===========================================================================
    # if nothing is sorted
    #===========================================================================
    if nomClasser != 100:
        column = data.classer(table, nomClasser)
        if allP:
            if filtre == 2 and conditions != []:
                rep = select(data.table(table), plus, column, listFiltre=conditions)
            else:
                if table == 6 and not request.user.is_superuser:
                    conditions = []
                    conditions.append(("prof", request.user.personne))
                    rep = select(data.table(table), plus, column, listFiltre=conditions)  
                else:
                    rep = select(data.table(table), plus, column)   
        else:
            if filtre == 2 and conditions != [] :
                rep = select(data.table(table), plus, column, page, nbparpage, listFiltre=conditions)
            else:    
                if table == 6 and not request.user.is_superuser:
                    conditions = []
                    conditions.append(("prof", request.user.personne))
                    rep = select(data.table(table), plus, column, page, nbparpage, listFiltre=conditions)   
                else:
                    rep = select(data.table(table), plus, column, page, nbparpage)
    #===========================================================================
    # something is sorted
    #===========================================================================
    else:    
        if allP:
            if filtre == 2 and conditions != []:
                rep = select(data.table(table), listFiltre=conditions)
            else:
                if table == 6 and not request.user.is_superuser:
                    conditions = []
                    conditions.append(("prof", request.user.personne))
                    rep = select(data.table(table), listFiltre=conditions) 
                else:
                    rep = select(data.table(table))
        else :      
            if filtre == 2 and conditions != []:     
                rep = select(data.table(table), page=page, nbparpage=nbparpage, listFiltre=conditions)
            else:
                if table == 6 and not request.user.is_superuser:
                    conditions = []
                    conditions.append(("prof", request.user.personne))
                    rep = select(data.table(table), page=page, nbparpage=nbparpage, listFiltre=conditions)
                else:
                    rep = select(data.table(table), page=page, nbparpage=nbparpage)
    reponserecherche = rep[0]
    n = rep[1]    
    pagemax = nbparpage * page >= n
    pagemoins = page - 1
    pageplus = page + 1
    i = 1
    pages = []
    while nbparpage * (i) < n:
        pages.append(i)
        i = i + 1
    pages.append(i)
    return render(request, 'BDD/ADMIN/watch.html', locals())    
