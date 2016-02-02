'''
Created on 30 oct. 2015

@author: mabadie_2
'''
from BDD import forms
from BDD.choices import INCONNU_STATUT, INCONNU_STATUT_TYPE, \
    INCONNU_STATUT_SALLE, SEMAINEINCONNU
from BDD.forms import fitrerP, AjouterP, fitrerGroupe
from BDD.models import Personne, Cour, Groupe, UV, Module, Salle, Note, \
    horaireProf, TypeCour


def ajouterA(t):
    """ Pour un ajout par ManytoMany"""
    reponse = None
    if t == 6:
        reponse = [forms.chooseGroupe, [["groupes", 0, Personne, 'groupe__in', forms.notes, forms.BaseNoteFormSet], ["module", 1, Module]]]
    return reponse
def ficheAfter(t):
    """ Afficher une fiche après ajout """
    reponse = True
    
    
    return reponse
def quiry(t):
    """ gestion de correction automatique des forms """
    l = []
    
    if t == 5:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['capacite', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'])
    elif t == 1:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
    elif t == 2:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])    
    elif t == 3:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['uv', "if (VAL) return true; else return false;"  , 'Choisissez un uv svp'])
    elif t == 4:
        l.append(['jour', "if ((VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['semaineMin', "if (VAL && VAL>=0 && VAL<=52) return true; else return false;"  , 'Ce champ est obligatoire et >-1 et <53'])
        l.append(['semaineMax', "if (VAL && VAL>=0 && VAL<=52) return true; else return false;"  , 'Ce champ est obligatoire et >-1 et <53'])
        l.append(['hmin', "if (VAL && VAL>=0 && VAL<=10) return true; else return false;"  , 'Ce champ est obligatoireet >-1 et <11'])
        l.append(['hmax', "if (VAL && VAL>=0 && VAL<=52) return true; else return false;"  , 'Ce champ est obligatoireet >-1 et <11'])
      
        
    elif t == 7:
        l.append(['nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
    elif t == 6:
        l.append(['note', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['note', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'])
        l.append(['personne', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
        l.append(['module', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'])
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
def formsoustable(table):
    """ Pour les ManytoMany dans modifier"""
    l = []
    if table == 1:
        l.append([forms.addPersonne, 'personnes', 1, 'personnes', Personne, 'personnes'])
        l.append([forms.addModule, 'modules', 2, 'modules', Module, 'modules'])
    elif table == 2:
        pass
    elif table == 3:
        l.append([forms.addGroupeModule, 'groupes', 1, 'groupes', Groupe, 'groupes'])
    elif table == 4:
        pass
        #l.append([forms.addSalle, 'salles', 1, 'salles', Salle, 'salles'])
    elif table == 5:
        pass
    elif table == 6:
        pass
    elif table == 7:
        l.append([forms.addTypeCour, 'groupe', 1, 'groupe', Groupe, 'groupe'])
        l.append([forms.addPersonnetypeCour, 'personnes', 2, 'personnes', Personne, 'personnes'])
    elif table == 0:
        l.append([forms.addGroupe, 'id_groupes', 1, 'groupes', Groupe, 'groupe_set'])
        
        
        
    return l
def links(table):
    """ Afficher des liens """
    l = []
    if table == 0:
        l.append(['/watch/6/0', 'Lui ajouter des notes'])
        l.append(['/watch/7/0', 'Lui ajouter des cours'])
    elif table == 2:
        l.append(['/watch/3/0', 'Lui ajouter des modules'])
    return l  
        
        
        
def soustable(table):
    """ pour les manytomany dans la fiche et modifier """
    
    """ [a, b, c, d] 
    
    a=0 : taille de d est de 2
    a=1 : taille de d est de 1
    a=2 : taille de d est de 1 et on affiche pas dans fiche seulement dans modifier
    b=0 : normal
    b=1: il y a un set
    c= nom de la caract
    d = lien
    
    
    
    
    """
    
    l = []
    if table == 1:
        l.append([1, 0, 'Personnes', ['personnes'], 0])
        l.append([1, 0, 'Modules', ['modules'], 3])
        l.append([0, 1, 'Cours', ['typecour_set', 'nom'], 7])
    elif table == 2:
        l.append([0, 1, 'Modules', ['module_set', 'nom'], 3])
    elif table == 3:
        l.append([0, 1, 'Groupes', ['groupe_set', 'nom'], 1])
    elif table == 4:
        l.append([2, 0, 'Salles', ['salles'], 5])
    elif table == 5:
        pass
    elif table == 6:
        pass
    elif table == 7:
        l.append([0, 1, 'Groupes', ['groupe', 'nom'], 1])
        l.append([1, 0, 'Profs', ['profs'], 0])
    elif table == 0:
        
        l.append([0, 1, 'Groupes', ['groupe_set', 'nom'], 1])
        l.append([1, 1, 'Horaires', ['horaireprof_set'], 1]) 
    
    return l
def listinside(t):
    """ Affichage des tables """
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
        listeliste.append([0, 'typeCour'])
        listeliste.append([3, 'salles'])
        listeliste.append([2, 'get_jour_display'])
        listeliste.append([0, 'semaineMin'])
        listeliste.append([0, 'semaineMax'])
        listeliste.append([0, 'hmin'])
        listeliste.append([0, 'hmax'])
        
        listeliste.append([0, 'uploadDate'])
    elif t == 6:
        listeliste.append([0, 'note'])
        listeliste.append([0, 'personne'])
        listeliste.append([1, 'module', 'nom'])
        listeliste.append([0, 'prof'])
        listeliste.append([0, 'uploadDate'])
    elif t == 7:
        listeliste.append([0, 'nom'])
        listeliste.append([0, 'isExam'])
        
        
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
    """ Nom des caract """
    l = []
    if t == 1:
        l.append(['Nom', 1])
        l.append(['Ajout', 2])
    elif t == 2:
        l.append(['Nom', 1])
    elif t == 4:
        l.append(['Cour', 1])
        l.append(['Salles', 2])
        l.append(['Jour', 3])
        l.append(['Début seamaine', 4])
        l.append(['Fin de seamaine', 5])
        l.append(['H début', 6])
        l.append(['H fin', 7])
        l.append(['Ajout', 8])
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
        l.append(['Celui qui à noté', 4])
        l.append(['Ajout', 5])
    elif t == 7:
        l.append(['Nom', 1])
        l.append(['Exam', 2])
        
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
    """ nom de la table """
    if t == 1:
        return Groupe
    elif t == 2:
        return UV
    elif t == 3:
        return Module
    elif t == 4:
        return Cour
    elif t == 5:
        return Salle
    elif t == 6:
        return Note
    elif t == 7:
        return TypeCour
    else:
        return Personne
def changecond(table, cond, conditions, obj):
    """ Changer les conditions initiales"""
    if table == 1:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
    elif table == 2:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
    elif table == 4:
        cond.append(('typeCour', 0))
        conditions.append(obj.typeCour.id)
        cond.append(('jour', 0))
        conditions.append(obj.jour)
        cond.append(('semaineMin', 0))
        conditions.append(obj.semaineMin)
        cond.append(('semaineMax', 0))
        conditions.append(obj.semaineMax)
        cond.append(('hmin', 0))
        conditions.append(obj.hmin)
        cond.append(('hmax', 0))
        conditions.append(obj.hmax)
        
        
    elif table == 6:
        cond.append(('note', 0))
        conditions.append(obj.note)
        cond.append(('personne', 0))
        conditions.append(obj.personne.id)
        cond.append(('module', 0))
        conditions.append(obj.module.id)
        
    elif table == 7:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
        cond.append(('isExam', 0))
        conditions.append(obj.isExam)
        
    elif table == 5:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
        if obj.capacite != None:
            cond.append(('capacite', 0))
            conditions.append(obj.capacite)
        if int(obj.type) != INCONNU_STATUT_SALLE:
            conditions.append(obj.type)
            cond.append(('type', 0))
    elif table == 3:
        cond.append(('nom', 0))
        conditions.append(obj.nom)
        cond.append(('uv', 0))
        conditions.append(obj.uv.id)
        
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
            cond.append(('l*ieuDeNaissance', 0))
        if obj.numeroDeTel != None:
            conditions.append(obj.numeroDeTel)
            cond.append(('numeroDeTel', 0)) 
def classer(t, nomClasser):
    """ Pour classer """
    if t == 1:
        if nomClasser == 1:
            column = 'nom'
        else:
            column = 'uploadDate'
    elif t == 2:
        column = 'nom'
    elif t == 4:
        if nomClasser == 1:
            column = 'typeCour__nom'
        elif nomClasser == 2:
            column = 'salles'
        elif nomClasser == 4:
            column = 'semaineMin'
        elif nomClasser == 5:
            column = 'semaineMax'
        elif nomClasser == 6:
            column = 'hmin'
        elif nomClasser == 7:
            column = 'hmax'
        else:
            column = 'jour'
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
    """ Comment filter """
    l = []
    if t == 1:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
    elif t == 2:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
    elif t == 4:
        l.append(['typeCour', 'typeCour', "", 'typeCour__nom__icontains', 0])
        l.append(['salles', 'salles', None, 'salles', 4])
        l.append(['jour', 'jour', SEMAINEINCONNU, 'jour', 1])
        l.append(['semaineMin', 'semaineMin', None, 'semaineMin', 0])
        l.append(['semaineMax', 'semaineMax', None, 'semaineMax', 0])
        l.append(['hmin', 'hmin', None, 'hmin', 0])
        l.append(['hmax', 'hmax', None, 'hmax', 0])
    elif t == 3:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
        l.append(['uv', 'uv', "", 'uv__nom', 3])
    elif t == 6:
        l.append(['note', 'note', None, 'note', 0])
        l.append(['personne', 'personne', "", 'personne__filter__icontains', 0])
        l.append(['module', 'module', "", 'module__nom__icontains', 0])
    elif t == 7:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
        l.append(['isExam', 'isExam', "", 'isExam', 0])
    elif t == 5:
        l.append(['nom', 'nom', "", 'nom__icontains', 0])
        l.append(['capacite', 'capacite', None, 'capacite', 0])
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
    """ LEs formulaires """
    if t == 1:
        if n == 0:
            if post == None:
                return fitrerGroupe()
            else:
                return fitrerGroupe(post)
        elif n == 2:
            if post == None:
                return forms.changeGroupe()
            else:
                return forms.changeGroupe(post)
        elif n == 3:
            return forms.NomFormSet
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
        elif n == 2:
            if post == None:
                return forms.changeUV()
            else:
                return forms.changeUV(post)
        elif n == 3:
            return forms.NomFormSet
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
        elif n == 2:
            if post == None:
                return forms.changeModule()
            else:
                return forms.changeModule(post)
        elif n == 3:
            return forms.moduleFormSet
        else:
            if post == None: 
                return forms.AjouterModule
            else:
                return forms.AjouterModule(post)
    elif t == 4:
        if n == 0:
            if post == None:
                return forms.fitrerCalendrier()
            else:
                return forms.fitrerCalendrier(post)
        elif n == 2:
            if post == None:
                return forms.changeCalendrier()
            else:
                return forms.changeCalendrier(post)
        elif n == 3:
            return forms.CalendrierFormSet
        else:
            if post == None: 
                return forms.AjouterCalendrier
            else:
                return forms.AjouterCalendrier(post) 
    elif t == 6:
        if n == 0:
            if post == None:
                return forms.fitrerNote()
            else:
                return forms.fitrerNote(post)
        elif n == 2:
            if post == None:
                return forms.changeNote()
            else:
                return forms.changeNote(post)
        elif n == 3:
            return forms.BaseNoteFormSet
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
        elif n == 2:
            if post == None:
                return forms.changeSalle()
            else:
                return forms.changeSalle(post)
        elif n == 3:
            return forms.NomFormSet
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
        elif n == 2:
            if post == None:
                return forms.changeCour()
            else:
                return forms.changeCour(post)
        elif n == 3:
            return None
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
        elif n == 2:
            if post == None:
                return forms.changeP()
            else:
                return forms.changeP(post)
        elif n == 3:
            return forms.PersonneFormSet
        else:
            if post == None:
                return AjouterP
            else:
                return AjouterP(post)
            
