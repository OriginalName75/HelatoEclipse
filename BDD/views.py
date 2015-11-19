# -*- coding: utf-8 -*-


# ta mère

from datetime import datetime

from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models.query_utils import Q
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

from BDD.forms import nbAjout
from BDD.models import Personne
from Functions import  data
from Functions import generator
from Functions.selectData import select


@login_required(login_url='/connexion')
def index(request):
    return render(request, 'BDD/index.html')    

@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def administration(request):
    return render(request, 'BDD/ADMIN/admin.html')    


@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def fiche(request, table, idP, filtre, page, nbparpage, nomClasser, plusOuMoins):
    table = int(table)
    TABBLE = data.table(table)
    obj = TABBLE.objects.get(id=int(idP))
    listeliste = data.listinside(table)
    listetab = data.listTable(table)
    links = data.links(table)
    entier = 0
    soustable = data.soustable(table)
    titrest = []
    for st in soustable:
    
        if st[0] == 0:
            titrest.append([st[0], st[2], getattr(obj, st[3]).all(), st[4]])
        else:
            titrest.append([st[0], st[2], getattr(obj, st[3]).all()])
    
    return render(request, 'BDD/ADMIN/fiche.html', locals())    



@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def ajouter(request, table, nbajout, filtre, page, nbparpage, nomClasser, plusOuMoins, first=True):
    
    nbajout = int(nbajout)
    table = int(table)
    ficheAfter = data.ficheAfter(table)
    if nbajout > 0:
        
        listeform = range(0, nbajout)
        lquery = data.quiry(table)
        table = int(table)
        envoi = False
        Formset = formset_factory(data.form(table, 1), extra=nbajout)
        if request.method == 'POST' and first:
            
            formset = Formset(request.POST, request.FILES)
            if formset.is_valid():
                nbajout = 0  
                envoi = True
                
                for form in formset:
                    
                    idP = form.save()
                
                if not ficheAfter:
                    
                    return change(request, table, idP, 0, filtre, page, nbparpage, nomClasser, plusOuMoins, 0, False)
            form = nbAjout()
                       
        else:
            formset = Formset() 
            
            
    else:
        if request.method == 'POST':
            
            form = nbAjout(request.POST)  
            if form.is_valid():
                nb = form.cleaned_data['nb']
                
                return ajouter(request, table, nb, filtre, page, nbparpage, nomClasser, plusOuMoins, False)

        else:
            
            form = nbAjout() 
            
    return render(request, 'BDD/ADMIN/ajouter.html', locals())


@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def delete(request, table, idP, filtre, page, nbparpage, nomClasser, plusOuMoins, supri):
    supr = False
    table = int(table)
    p = data.table(table).objects.get(id=int(idP))
    if int(supri) == 1:
        obj = data.table(table).objects.filter(id=int(idP))
        obj.delete()
        supr = True
    
    
    return render(request, 'BDD/ADMIN/delete.html', locals())
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def randomP(request):
    
    generator.personnes(300)
    text = """done"""
    return HttpResponse(text)
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def areusure(request, table, idP, what, filtre, page, nbparpage, nomClasser, plusOuMoins, nor, which):
    table = int(table)
    
    if int(nor) == 0:
        return render(request, 'BDD/ADMIN/areusure.html', locals())  
    else:
        TABBLE = data.table(table)
        obj = TABBLE.objects.get(id=int(idP))
        l = data.soustable(table)
        for ll in l:
            gr = getattr(obj, ll[3]).get(id=int(what))
            getattr(obj, ll[3]).remove(gr)
        return change(request, table, idP, 0, filtre, page, nbparpage, nomClasser, plusOuMoins,0)
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def change(request, table, idP, what, filtre, page, nbparpage, nomClasser, plusOuMoins, nbajout, first=True):
    table = int(table)
    soustable = data.soustable(table)
    TABBLE = data.table(table)
    obj = TABBLE.objects.get(id=int(idP))
    links = data.links(table)
    titrest = []
    ii = 0
    changed = False
    if (first and request.method == 'POST'  and int(nbajout) == 0):
        
        nbajoutf = nbAjout(request.POST)
    
        if nbajoutf.is_valid():
            nbajout = int(nbajoutf.cleaned_data['nb'])
            first=False
            
            
            
    else:
        nbajoutf = nbAjout()
    
    if (first and request.method == 'POST' and int(what) > 0 and int(nbajout) > 0):
        
        stforms = data.formsoustable(table, request.POST, int(what))
        
        for frm in stforms:
            llll=[o.id for o in getattr(obj, frm[5]).all()]
            frm[0].fields[frm[3]].queryset = frm[4].objects.all().exclude(id__in=llll)
        for frm in stforms:
            
            if frm[0].is_valid():
                frm[0].save(obj)
                changed = True
                return http.HttpResponseRedirect('')
    else:
        
        stforms = data.formsoustable(table)
        
        
        for frm in stforms:
            llll=[o.id for o in getattr(obj, frm[5]).all()]
            frm[0].fields[frm[3]].queryset = frm[4].objects.all().exclude(id__in=llll)
            Formset = formset_factory(frm[0], int(nbajout))
            
    
    if (first and request.method == 'POST' and int(what) == 0 and int(nbajout) > 0):
        
        form = data.form(table, 0, request.POST) 
        if form.is_valid():
            form.modif(idP)    
            changed = True
            
            
    else:
       
        cond = []
        conditions = []
        
        form = data.form(table, 0)
        
        data.changecond(table, cond, conditions, obj)
         
        entier = 0
        for l in conditions:
            if cond[entier][1] == 1:
                form.fields[cond[entier][0]].initial = l.strftime('%d/%m/%Y')
            else:   
                form.fields[cond[entier][0]].initial = l
            entier = entier + 1 
    
    for st in soustable:
        
        if st[0] == 0:
            titrest.append([stforms[ii], st[0], st[2], [getattr(obj, st[3]).all(), st[4]], st[1]])
        else:
            titrest.append([stforms[ii], st[0], st[2], [getattr(obj, st[3], st[1]).all()], st[1]])
            
        ii = ii + 1  
    return render(request, 'BDD/ADMIN/change.html', locals())       
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def watch(request, table, filtre, page=None, nbparpage=None, nomClasser=None, plusOuMoins=None):
    table = int(table)  
    FILTRE = data.filtre(table)
    filtre = int(filtre)
    listAffich = data.listTable(table)
    listeliste = data.listinside(table)
    addmulti = data.mulipleajout(table)
    if page == None:
        page = 1
    else:
        page = int(page)
    if nomClasser == None:
        nomClasser = 100
    if plusOuMoins == None:
        plusOuMoins = 0   
    if nbparpage == None:
        nbparpage = 40
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
    if filtre > 0:
        if request.method == 'POST':
           
            form = data.form(table, 0, request.POST)
                
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
                        else:
                            cleanf = clean
                        
                        conditions.append((f[3], cleanf))
                        cond.append((f[1], 0))
                request.session['conditions'] = conditions
                request.session['cond'] = cond
                
        else:
            form = data.form(table, 0)
    if filtre == 2 and conditions == []:
        try:
            conditions = request.session['conditions']
            cond = request.session['cond']
            
            entier = 0
            for l in conditions:
                if cond[entier][1] == 1:
                    form.fields[cond[entier][0]].initial = (datetime.strptime(l[1], '%Y-%m-%d').date()).strftime('%d/%m/%Y')
                else:   
                    
                    form.fields[cond[entier][0]].initial = l[1]
                entier = entier + 1
        except:
            filtre = 0
    if nomClasser != 100:
        column = data.classer(table, nomClasser)
        if allP:
            if filtre == 2:
                rep = select(data.table(table), plus, column, listFiltre=conditions)
            else:
                rep = select(data.table(table), plus, column)   
        else:
            if filtre == 2:
                rep = select(data.table(table), plus, column, page, nbparpage, listFiltre=conditions)
            else:    
                rep = select(data.table(table), plus, column, page, nbparpage)
    else:    
        if allP:
            if filtre == 2:
                rep = select(data.table(table), listFiltre=conditions)
            else:
                rep = select(data.table(table))
        else :      
            if filtre == 2:     
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
