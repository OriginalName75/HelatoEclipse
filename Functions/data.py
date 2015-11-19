'''
Created on 30 oct. 2015

@author: mabadie_2
'''
from BDD import forms
from BDD.choices import INCONNU_STATUT, INCONNU_STATUT_TYPE, \
    INCONNU_STATUT_SALLE
from BDD.forms import fitrerP, AjouterP, fitrerGroupe, addGroupe, addPersonne
from BDD.models import Personne, Cour, Groupe, UV, Module, Annee, Salle, Note


def ficheAfter(t):
    reponse=True
    if t==1:
        reponse=False
    return reponse
def mulipleajout(t):
    reponse=True
    if t==1:
        reponse=False
    return reponse

def quiry(t):
    l = []
    
    if t == 5:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['capacite', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'])
    elif t == 1:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
    elif t == 3:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['uv', "if (VAL) return true; else return false;"  , 'Choisissez un uv svp'])
    elif t == 0:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['prenom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['login', "if (VAL.length > 3 && VAL) return true; else return false;"  , 'Ce champ doit avoir au moins 4 caractères'])
        
        
        l.append(['numeroDeTel', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'])
        l.append(['promotion', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'])
        l.append(['mdp', "if (VAL.length > 5 && VAL) return true; else return false;"  , 'Au moins 6 caractere plz'])
        l.append(['mdp2', "if ((VAL == jQuery('#id_form-'+lolo+'-mdp').val()) && VAL) return true; else return false;"  , 'Les mots de passe sont différents'])
        l.append(['mail', "if (VAL.match(/^[^\\W][a-zA-Z0-9\\_\\-\\.]+([a-zA-Z0-9\\_\\-\\.]+)*\\@[a-zA-Z0-9_]+(\\.[a-zA-Z0-9_]+)*\\.[a-zA-Z]{2,4}$/)) return true; else return false;"  , 'Ce n\'est pas un mail valide'])
        l.append(['dateDeNaissance', "if (!isValidDate(parseInt(VAL.split('/')[2]), parseInt(VAL.split('/')[0]), parseInt(VAL.split('/')[1]))) return false; else return true;"  , 'Ce n\'est pas une date valide'])

    return l
def formsoustable(table, y=None, n=None):
    l = []
    if table == 1:
        l.append([forms.addPersonne, 'personnes', 1,'personnes',Personne,'personnes'])
    elif table == 2:
        l.append([0, 'Modules', 'module_set', 'nom'])
    elif table == 3:
        pass
    elif table == 4:
        pass
    elif table == 5:
        pass
    elif table == 6:
        pass
    elif table == 7:
        l.append([0, 'Groupes', 'groupe', 'nom'])
        l.append([0, 'Salle', 'salles', 'nom'])
        l.append([1, 'Profs', 'personnes', 'user', 'last_name'])
    elif table == 0:
        if y == None or n == None:
            li=addGroupe()
        else:
            if n == 1:
                li=addGroupe(y)
            else:
                li=addGroupe()
        l.append([li, 'id_groupes', 1,'groupes',Groupe,'groupe_set'])
    return l
def links(table):
    l=[]
    if table==0:
        l.append(['/watch/6/0','Lui ajouter des notes'])
        l.append(['/watch/7/0','Lui ajouter des cours'])
    return l  
def soustable(table):
    l = []
    if table == 1:
        l.append([1,0, 'Personnes', 'personnes'])
    elif table == 2:
        l.append([0, 'Modules', 'module_set', 'nom'])
    elif table == 3:
        pass
    elif table == 4:
        pass
    elif table == 5:
        pass
    elif table == 6:
        pass
    elif table == 7:
        l.append([0, 'Groupes', 'groupe', 'nom'])
        l.append([0, 'Salle', 'salles', 'nom'])
        l.append([1, 'Profs', 'personnes'])
    elif table == 0:
        
        l.append([0, 1,'Groupes', 'groupe_set', 'nom'])
        
    
    return l
def listinside(t):
    listeliste = []
    if t == 1:
        listeliste.append([0, 'nom'])
        listeliste.append([0, 'uploadDate'])
    elif t == 2:
        listeliste.append([0, 'nom'])
    elif t == 3:
        listeliste.append([0, 'nom'])
        listeliste.append([1, 'uv', 'nom'])
    elif t == 4:
        listeliste.append([0, 'annee'])
    elif t == 6:
        listeliste.append([0, 'note'])
        listeliste.append([0, 'personne'])
        listeliste.append([1, 'module', 'nom'])
        listeliste.append([0, 'uploadDate'])
    elif t == 7:
        listeliste.append([0, 'nom'])
        listeliste.append([0, 'isExam'])
        listeliste.append([0, 'uploadDate'])
        
    elif t == 5:
        listeliste.append([0, 'nom'])
        listeliste.append([0, 'capacite'])
        listeliste.append([2, 'get_type_display'])
    elif t == 0:
        listeliste.append([1, 'user', 'last_name'])
        listeliste.append([1, 'user', 'first_name'])
        listeliste.append([2, 'get_sexe_display'])
        listeliste.append([0, 'promotion'])
        listeliste.append([2, 'get_type_display'])
        listeliste.append([0, 'dateDeNaissance'])
        listeliste.append([0, 'lieuDeNaissance'])
        listeliste.append([0, 'numeroDeTel'])
        listeliste.append([1, 'user', 'email'])
        listeliste.append([1, 'user', 'username'])
        listeliste.append([0, 'adresse'])
        listeliste.append([0, 'uploadDate'])
    
    return listeliste

def listTable(t):
    l = []
    if t == 1:
        l.append(['Nom', 1])
        l.append(['Ajout', 2])
    elif t == 2:
        l.append(['Nom', 1])
    elif t == 4:
        l.append(['Année', 1])
    elif t == 3:
        l.append(['Nom', 1])
        l.append(['UV', 2])
    elif t == 5:
        l.append(['Nom', 1])
        l.append(['Capacite', 2])
        l.append(['Type', 3])
    elif t == 6:
        l.append(['Note', 1])
        l.append(['Eleve', 2])
        l.append(['Module', 3])
        l.append(['Ajout', 4])
    elif t == 7:
        l.append(['Nom', 1])
        l.append(['Exam', 2])
        l.append(['Ajout', 3])
    elif t == 0:
        l.append(['Nom', 1])
        l.append(['Prenom', 2])
        l.append(['Sexe', 3])
        l.append(['Promotion', 4])
        
        l.append(['Statut', 5])
        l.append(['Date Naissance', 6])
        l.append(['Lieu Naissance', 7])
        l.append(['Tel', 8])
        l.append(['Email', 9])
        l.append(['Login', 10])
        
        l.append(['Adresse', 11])
        l.append(['Ajout', 12])
        
      
        
    return l
def table(t):
    if t == 1:
        return Groupe
    elif t == 2:
        return UV
    elif t == 3:
        return Module
    elif t == 4:
        return Annee
    elif t == 5:
        return Salle
    elif t == 6:
        return Note
    elif t == 7:
        return Cour
    else:
        return Personne
def changecond(table, cond, conditions, obj):
    if table == 1:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
    elif table == 2:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
    elif table == 4:
        cond.append(('annee', 0))
        conditions.append(obj.annee)
    elif table == 6:
        cond.append(('note', 0))
        conditions.append(obj.note)
        cond.append(('personne', 0))
        conditions.append(obj.personne)
        cond.append(('module', 0))
        conditions.append(obj.module)
        cond.append(('uploadDate', 0))
        conditions.append(obj.uploadDate)
    elif table == 7:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
        cond.append(('isExam', 0))
        conditions.append(obj.isExam)
        cond.append(('uploadDate', 0))
        conditions.append(obj.uploadDate)
    elif table == 5:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
        if obj.capacite != None:
            cond.append(('capacite', 0))
            conditions.append(obj.capacite)
        if int(obj.type) != INCONNU_STATUT_SALLE:
            conditions.append(obj.sexe)
            cond.append(('type', 0))
    elif table == 3:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
        cond.append(('uv', 0))
        conditions.append(obj.uv)
        cond.append(('uv', 0))
        conditions.append(obj.uv)
    elif table == 0:
        cond.append(('nom', 0))
        conditions.append(obj.user.last_name)
        cond.append(('prenom', 0))
        conditions.append(obj.user.first_name)
        cond.append(('login', 0))
        conditions.append(obj.user.username)
        if obj.user.email != None:
            conditions.append(obj.user.email)
            cond.append(('mail', 0)) 
        if int(obj.sexe) != INCONNU_STATUT:
            conditions.append(obj.sexe)
            cond.append(('sexe', 0))
        if obj.adresse != None:
            conditions.append(obj.adresse)
            cond.append(('adresse', 0))
        if obj.promotion != None:
            conditions.append(obj.promotion)
            cond.append(('promotion', 0))
        if int(obj.type) != INCONNU_STATUT_TYPE:
            conditions.append(obj.type)
            cond.append(('typeP', 0))
        if obj.dateDeNaissance != None:
            conditions.append(obj.dateDeNaissance)
            cond.append(('dateDeNaissance', 1))
        if obj.lieuDeNaissance != None:
            conditions.append(obj.lieuDeNaissance)
            cond.append(('lieuDeNaissance', 0))
        if obj.numeroDeTel != None:
            conditions.append(obj.numeroDeTel)
            cond.append(('numeroDeTel', 0)) 
def classer(t, nomClasser):
    if t == 1:
        if nomClasser == 1:
            column = 'nom'
        else:
            column = 'uploadDate'
    elif t == 2:
        column = 'nom'
    elif t == 4:
        column = 'annee'
    elif t == 5:
        if nomClasser == 1:
            column = 'nom'
        elif nomClasser == 2:
            column = 'capacite'
        else:
            column = 'type'
    elif t == 6:
        if nomClasser == 1:
            column = 'note'
        elif nomClasser == 2:
            column = 'personne'
        elif nomClasser == 3:
            column = 'module'
        else:
            column = 'uploadDate'
    elif t == 3:
        if nomClasser == 1:
            column = 'nom'
        else:
            column = 'uv__nom'
    elif t == 7:
        if nomClasser == 1:
            column = 'nom'
        elif nomClasser == 2:
            column = 'isExam'
        else:
            column = 'uploadDate'
    elif t == 0:
        if nomClasser == 1:
            column = 'user__last_name'
        elif nomClasser == 2:
            column = 'user__first_name'
        elif nomClasser == 4:
            column = 'promotion'
        elif nomClasser == 5:
            column = 'type'
        elif nomClasser == 3:
            column = 'sexe'
        elif nomClasser == 11:
            column = 'adresse'
        elif nomClasser == 6:
            column = 'dateDeNaissance'
        elif nomClasser == 7:
            column = 'lieuDeNaissance'
        elif nomClasser == 8:
            column = 'numeroDeTel'
        elif nomClasser == 9:
            column = 'user__email'
        elif nomClasser == 10:
            column = 'user__username'
        else:
            column = 'uploadDate'
    
    return column
def filtre(t):
    l = []
    if t == 1:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
    elif t == 2:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
    elif t == 4:
        l.append(['annee', 'annee', "", 'annee', 0])
    elif t == 3:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
        l.append(['uv', 'uv', "", 'uv__nom__icontains', 0])
    elif t == 6:
        l.append(['note', 'note', "", 'note', 0])
        l.append(['personne', 'personne', "", 'personne__user__last_name__icontains', 0])
        l.append(['module', 'module', "", 'module__nom__icontains', 0])
    elif t == 7:
        l.append(['nom', 'nom', "", 'nom', 0])
        l.append(['isExam', 'isExam', "", 'isExam', 0])
    elif t == 5:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
        l.append(['capacite', 'capacite', "", 'capacite', 0])
        l.append(['type', 'type', INCONNU_STATUT_SALLE, 'type', 1])
    elif t == 0:    
        
        l.append(['nom', 'nom', "", 'user__last_name__icontains', 0])
        l.append(['prenom', 'prenom', "", 'user__first_name__icontains', 0])
        l.append(['login', 'login', "", 'user__username__icontains', 0])
        l.append(['mail', 'mail', "", 'user__email', 0])
        l.append(['sexe', 'sexe', INCONNU_STATUT, 'sexe', 1])
        l.append(['adresse', 'adresse', "", 'adresse__icontains', 0])
        l.append(['promotion', 'promotion', None, 'promotion', 0])
        l.append(['typeP', 'type', INCONNU_STATUT_TYPE, 'type', 1])
        l.append(['dateDeNaissance', 'dateDeNaissance', None, 'dateDeNaissance', 2])
        l.append(['lieuDeNaissance', 'lieuDeNaissance', "", 'lieuDeNaissance__icontains', 0])
        l.append(['numeroDeTel', 'numeroDeTel', "", 'numeroDeTel', 0])
        
    return l
def form(t, n, post=None):
    if t == 1:
        if n == 0:
            if post == None:
                return fitrerGroupe()
            else:
                return fitrerGroupe(post)
        else:
            if post == None:
                return forms.AjouterGroupe
            else:
                return forms.AjouterGroupe(post)
    elif t == 2:
        if n == 0:
            if post == None:
                return forms.fitrerUV()
            else:
                return forms.fitrerUV(post)
        else:
            if post == None:
                return forms.AjouterUV
            else:
                return forms.AjouterUV(post)
    elif t == 3:
        if n == 0:
            if post == None:
                return forms.fitrerModule()
            else:
                return forms.fitrerModule(post)
        else:
            if post == None: 
                return forms.AjouterModule
            else:
                return forms.AjouterModule(post)
    elif t == 4:
        if n == 0:
            if post == None:
                return forms.fitrerAnnee()
            else:
                return forms.fitrerAnnee(post)
        else:
            if post == None: 
                return forms.AjouterAnnee
            else:
                return forms.AjouterAnnee(post) 
    elif t == 6:
        if n == 0:
            if post == None:
                return forms.fitrerNote()
            else:
                return forms.fitrerNote(post)
        else:
            if post == None: 
                return forms.AjouterNote
            else:
                return forms.AjouterNote(post) 
    elif t == 5:
        if n == 0:
            if post == None:
                return forms.fitrerSalle()
            else:
                return forms.fitrerSalle(post)
        else:
            if post == None: 
                return forms.AjouterSalle
            else:
                return forms.AjouterSalle(post)
    elif t == 7:
        if n == 0:
            if post == None:
                return forms.fitrerCour()
            else:
                return forms.fitrerCour(post)
        else:
            if post == None: 
                return forms.AjouterCour
            else:
                return forms.AjouterCour(post)
    else:
        if n == 0:
            if post == None:
                return fitrerP()
            else:
                return fitrerP(post)
        else:
            if post == None:
                return AjouterP
            else:
                return AjouterP(post)
