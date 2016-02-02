# -*- coding: utf-8 -*-

from datetime import datetime

from ajax_select.fields import autoselect_fields_check_can_add
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render

from BDD.choices import PROF_STATUT
from BDD.forms import nbAjout
from BDD.models import Personne, Note
from Functions import  data
from Functions import generator
from Functions.selectData import select


@login_required(login_url='/connexion')
def index(request):
    PR = PROF_STATUT
    return render(request, 'BDD/index.html', locals())    

@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def administration(request):
    return render(request, 'BDD/ADMIN/admin.html')    


@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def fiche(request, table, idP, filtre=None, page=None, nbparpage=None, nomClasser=None, plusOuMoins=None):
    table = int(table)
    allllll = 'all'
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
            titrest.append([st[0], st[2], getattr(obj, st[3][0]).all(), st[3][1], st[4]])
        elif st[0] == 1:
            titrest.append([st[0], st[2], getattr(obj, st[3][0]).all(), st[4]])
    
    return render(request, 'BDD/ADMIN/fiche.html', locals())    



@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser or u.personne.type == PROF_STATUT)
def ajouter(request, table, nbajout, filtre, page, nbparpage, nomClasser, plusOuMoins, first=True):
    
    nbajout = int(nbajout)
    table = int(table)
    if not request.user.is_superuser and table != 6:
        return index(request)
    ajj = data.ajouterA(table)
    ficheAfter = data.ficheAfter(table)
    if nbajout > 0 and nbajout != 100:
        
        listeform = range(0, nbajout)
        lquery = data.quiry(table)
        table = int(table)
        envoi = False
        if nbajout < 100:
            
            if data.form(table, 3) == None:
                Formset = formset_factory(data.form(table, 1), extra=nbajout)
            else:
                
                Formset = formset_factory(data.form(table, 1), extra=nbajout, formset=data.form(table, 3))
            if request.method == 'POST' and first:
                print("1")
                formset = Formset(request.POST, request.FILES)
                if formset.is_valid():
                    
                    nbajout = 0  
                    envoi = True
                    
                    
                    for form in formset:
                        if table == 6:
                            idP = form.save(request.user.personne)
                            
                        else:
                            idP = form.save()
                    
                    if not ficheAfter:
                        
                        return change(request, table, idP, 0, filtre, page, nbparpage, nomClasser, plusOuMoins, False)
                form = nbAjout()
                           
            else:
                formset = Formset() 
        else:
            stock = request.session['stock']
            solo = []
            multi = []
            i = 0
            
            
            for x in ajj[1]:
                if x[1] == 0:
                    kwargs = {
                        x[3]: stock[i]
                        
                    }
                    a = x[2].objects.filter(**kwargs)
                    nb = a.count()
                    Formset = formset_factory(x[4], extra=nb, formset=x[5])
                    
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
                    solo.append(x[2].objects.get(id=stock[i]))
                i += 1
            if request.method == 'POST' and first:
                if formset.is_valid():
                    jj = 0
                    for f in formset:
                        if table == 6:
                            f.save(solo, [x[jj] for x in multi],request.user.personne)
                        else:
                            f.save(solo, [x[jj] for x in multi])
                        jj += 1
                    nbajout = 0  
                    return http.HttpResponseRedirect('/watch/' + str(table) + '/' + str(filtre))
                
    
                
            
            
    else:
        if request.method == 'POST':
            if ajj == None or nbajout < 100:
                
                form = nbAjout(request.POST)
                
                if form.is_valid():
                    nb = form.cleaned_data['nb']
                    
                    return ajouter(request, table, nb, filtre, page, nbparpage, nomClasser, plusOuMoins, False)
                else:
                    if ajj != None:
                        formAjj = ajj[0]()
            else:
                formAjj = ajj[0](request.POST)
                stock = []
                if formAjj.is_valid():
                    for x in ajj[1]:
                        if x[1] == 0:
                            stock.append(formAjj.cleaned_data[x[0]])
                        else:
                            stock.append(formAjj.cleaned_data[x[0]].id)
                
                    request.session['stock'] = stock
                    return ajouter(request, table, 101, filtre, page, nbparpage, nomClasser, plusOuMoins, False)
        else:
            if ajj != None:
                formAjj = ajj[0]()
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
    
        
    
    generator.personnes(300, True)
    if not hasattr(request.user, 'personne'):
        p = Personne()
        p.user = request.user
        p.filter="Superadmin"
        p.save()
        request.user.first_name = "Dieu"
        request.user.last_name = "Tout puissan"
        request.user.save()
       
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
        return change(request, table, idP, 0, filtre, page, nbparpage, nomClasser, plusOuMoins, 0)
    
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def change(request, table, idP, what, filtre, page, nbparpage, nomClasser, plusOuMoins, first=True):
    table = int(table)
    soustable = data.soustable(table)
    TABBLE = data.table(table)
    obj = TABBLE.objects.get(id=int(idP))
    links = data.links(table)
    titrest = []
    formseti = None
    ii = 0
    changed = False
    stforms = data.formsoustable(table)
    if (first and request.method == 'POST' and int(what) > 0):
        for frm in stforms:
            instance = TABBLE.objects.get(id=int(idP))
            frm[0] = frm[0](request.POST, instance=instance)
        j = 1  
        for frm in stforms:
            
            if j == int(what) and frm[0].is_valid():
                frm[0].savePerso(int(idP))
                changed = True
            j += 1
        return http.HttpResponseRedirect('')
    else:
        
        stforms = data.formsoustable(table)
    
        for frm in stforms:
            instance = TABBLE.objects.get(id=int(idP))
            frm[0] = frm[0](instance=instance)
            
            
            
    if (first and request.method == 'POST' and int(what) == 0):
        
        form = data.form(table, 2, request.POST) 
        if form.is_valid():
            form.modif(idP)    
            changed = True
            
            
    else:
       
        cond = []
        conditions = []
        
        form = data.form(table, 2)
        
        data.changecond(table, cond, conditions, obj)
         
        entier = 0
        for l in conditions:
            if cond[entier][1] == 1:
                form.fields[cond[entier][0]].initial = l.strftime('%d/%m/%Y')
            else:   
                form.fields[cond[entier][0]].initial = l
            entier = entier + 1 
    taille = len(stforms)
    print(taille)
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
def watch(request, table, filtre, page=None, nbparpage=None, nomClasser=None, plusOuMoins=None):
    table = int(table)
    if not request.user.is_superuser and table != 6:
        return index(request)
    FILTRE = data.filtre(table)
    filtre = int(filtre)
    listAffich = data.listTable(table)
    listeliste = data.listinside(table)
    print (listeliste)
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
            form = data.form(table, 0)
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
