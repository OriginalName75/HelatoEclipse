from collections.__main__ import p
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render

from BDD import forms
from BDD.choices import LUNDI, MARDI, JEUDI, VENDREDI, MECREDI
from BDD.models import Personne, Note, Module, UV, Groupe, TypeCour, Cour, Salle


# Create your views here.
@login_required(login_url='/connexion')
def menu(request):
    return render(request, 'Eleve/menu.html', locals())  
    
    
@login_required(login_url='/connexion')
def note(request):
    p=request.user.personne
    uvs = UV.objects.all().order_by('nom')
    g=p.groupe_set.all()
    modules = Module.objects.filter(groupe__in=g).order_by('uv')
    
   
    notes=p.note_set.all()
    #modules=uvs.module_set.all()  filter(groupe__in=g).order_by('uv')
    l2=[]
    for m in modules:
        note=notes.filter(module=m)
        if note.count()>0:
            note=note[0]
        l2.append([m,note])
    
    return render(request, 'Eleve/note.html', locals())  
    

@login_required(login_url='/connexion')
def emploi(request, semaine=None):
    if request.method == 'POST' :
        formul=forms.semaine(request.POST)
        if formul.is_valid() :       
            semaine=formul.cleaned_data['nb']
    else :
        formul=forms.semaine()
    
    
    import datetime
    time = datetime.datetime.now()-datetime.datetime(2016, 1, 4)
    sem = int(time.days/7)+1
    timenow = datetime.datetime.now()
    
    
    if semaine==None:
        semaine=sem

    pre=int(semaine)-1
    suiv=int(semaine)+1
    
    pre5=int(semaine)-5
    suiv5=int(semaine)+5
    
    pre10=int(semaine)-10
    suiv10=int(semaine)+10
     
    dlundi=datetime.date(2016,1,4) + timedelta(days=(int(semaine)-1)*7)
    dmardi=datetime.date(2016,1,4) + timedelta(days=(int(semaine)-1)*7+1)
    dmercredi=datetime.date(2016,1,4) + timedelta(days=(int(semaine)-1)*7+2)
    djeudi=datetime.date(2016,1,4) + timedelta(days=(int(semaine)-1)*7+3)
    dvendredi=datetime.date(2016,1,4) + timedelta(days=(int(semaine)-1)*7+4)
    
    
    p=request.user.personne
    g=p.groupe_set.all()
    cours = TypeCour.objects.filter(groupe__in=g)
    c=Cour.objects.filter(Q(typeCour__in=cours),Q(semaineMin__lte=semaine),Q(semaineMax__gte=semaine))
  
    llundi=[[],[],[],[],[],[]]
    lmardi=[[],[],[],[],[],[]]
    lmercredi=[[],[],[],[],[],[]]
    ljeudi=[[],[],[],[],[],[]]
    lvendredi=[[],[],[],[],[],[]]
    

    
    for cour in c :
        for k in range(1,6) :
            if cour.jour == LUNDI and cour.hmin<=k and cour.hmax>=k :
                llundi[k-1].append(cour)
                
        for k in range(1,6) :
            if cour.jour == MARDI and cour.hmin<=k and cour.hmax>=k :
                lmardi[k-1].append(cour)
                      
        for k in range(1,6) :
            if cour.jour == MECREDI and cour.hmin<=k and cour.hmax>=k :
                lmercredi[k-1].append(cour)
                
        for k in range(1,6) :
            if cour.jour == JEUDI and cour.hmin<=k and cour.hmax>=k :
                ljeudi[k-1].append(cour)
                
        for k in range(1,6) :
            if cour.jour == VENDREDI and cour.hmin<=k and cour.hmax>=k :
                lvendredi[k-1].append(cour)     
    
    ljour=[llundi,lmardi,lmercredi,ljeudi,lvendredi]
    l5=range(6)
    
    return render(request, 'Eleve/emploi.html', locals())  
    
    
@login_required(login_url='/connexion')
def donnees(request):
    p=request.user.personne
    g=p.groupe_set.all()
    lg=[]
    q=0
    for i in g :
        lg.append([i])
        q=q+1
    l6=range(q)    
        
        
    return render(request, 'Eleve/donnees.html', locals())  

