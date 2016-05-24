
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render

from BDD import forms
from BDD.choices import LUNDI, MARDI, JEUDI, VENDREDI, MECREDI
from BDD.models import Personne, Note, Module, UV, Groupe, TypeCour, Cour, Salle, \
    News
from Functions.news import addN


# Create your views here.
@login_required(login_url='/connexion')
def menu(request, plus=0):
    new = News.objects.filter(personne__id__icontains=request.user.personne.id).order_by('-id')
    maxx = new.count()
    news = []
    plus=int(plus)
    l = 0
    i = 0
    nb=1
    ajou = 0
    plus2=0
    first = True
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
    return render(request, 'Eleve/index.html', locals()) 
 
    
    
@login_required(login_url='/connexion')
def note(request):
    p=request.user.personne
    uvs = UV.objects.all().order_by('nom')
    g=p.groupe_set.all()
    modules = Module.objects.filter(groupe__in=g).order_by('theuv')
    
   
    notes=p.note_set.all()
    #modules=uvs.module_set.all()  filter(groupe__in=g).order_by('uv')
    l2=[]
    for m in modules:
        note=notes.filter(themodule=m)
        if note.count()>0:
            note=note[0].lanote
        else:
            note=""
        l2.append([m,note])
        
    import datetime
    timenow = datetime.datetime.now()
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
  
    llundi=[[],[],[],[],[],[],[],[]]
    lmardi=[[],[],[],[],[],[],[],[]]
    lmercredi=[[],[],[],[],[],[],[],[]]
    ljeudi=[[],[],[],[],[],[],[],[]]
    lvendredi=[[],[],[],[],[],[],[],[]]
    

    
    for cour in c :
        for k in range(1,7) :
            if cour.jour == LUNDI and cour.hmin<=k and cour.hmax>=k and k<8:
                llundi[k-1].append(cour)
                
        for k in range(1,7) :
            if cour.jour == MARDI and cour.hmin<=k and cour.hmax>=k and k<8:
                lmardi[k-1].append(cour)
                      
        for k in range(1,7) :
            if cour.jour == MECREDI and cour.hmin<=k and cour.hmax>=k and k<8:
                lmercredi[k-1].append(cour)
                
        for k in range(1,7) :
            if cour.jour == JEUDI and cour.hmin<=k and cour.hmax>=k and k<8:
                ljeudi[k-1].append(cour)
                
        for k in range(1,7) :
            if cour.jour == VENDREDI and cour.hmin<=k and cour.hmax>=k and k<8:
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
    import datetime
    timenow = datetime.datetime.now()
   
        
    return render(request, 'Eleve/donnees.html', locals())  

