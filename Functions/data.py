"""
    The ''data'' module
    ======================
    
    It defines the specifications of each kind of data in templates.
    
    
    
@author: IWIMBDSL
"""
from BDD import forms
from BDD.choices import INCONNU_STATUT, INCONNU_STATUT_TYPE, \
    INCONNU_STATUT_SALLE, SEMAINEINCONNU
from BDD.forms import fitrerP, AjouterP, fitrerGroupe
from BDD.models import Personne, Cour, Groupe, UV, Module, Salle, Note, \
    TypeCour


class ADDMANY():
    """
        
        :formInit: Before adding, ask which objects 
        :tformInit: form
        Ex (add marks) : the form ask which group is marked and which module the group is marked
        :form: form to add an object
        :tform: form
        Ex (add marks) : a form which ask the mark of a person
        :baseForm: BaseForm of :form:, to check errors.
        :tbaseForm: Baseform 
        :listFieldForm: names of the fields of formInit in the right order
        :tlistFieldForm:  list of string
        :listModel: list of the related Model in the right order
        :tlistModel: list of Models
        :QCode:  Qcode (Django)
        :tQCode: string
        
    """
    def __init__(self, formInit, form, baseForm, listFieldForm, listModel, QCode):
        self.formInit = formInit
        self.form = form
        self.baseForm = baseForm
        self.listFieldForm = listFieldForm
        self.listModel= listModel
        self.QCode=QCode
  
class QUIRY():
    """
        
        :nom_form: name of the form's field
        :nom_form: string
        
        :quiry_code: quiry code.
        :quiry_code: string
        Ex "if (VAL) return true; else return false;"
        :string: Error printed
        :string: string 
        
        
    """
    def __init__(self, nom_form, quiry_code, string):
        self.nom_form = nom_form
        self.quiry_code = quiry_code
        self.string = string
       
 
def formsoustable(table):
    """ 
        Defines the forms in the modify view for the many to many relations
    
    
    :param table: it represent which kind of data it is (exemple: a groupe)
    :type table: int 
    
    """
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
        # l.append([forms.addSalle, 'salles', 1, 'salles', Salle, 'salles'])
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

        
        
        
def soustable(table):
    """ 
    For the many to many in modify and fiche view
    
     [a, b, c, d] 
    
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
    """ 
        For the watch view to print the data
        
    :param t: it represent which kind of data it is (exemple: a groupe)
    :type t: int 
    
    
    """
    listeliste = []
    if t == 1:
        listeliste.append([0, 'nom'])
        listeliste.append([0, 'uploadDate'])
    elif t == 2:
        listeliste.append([0, 'nom'])
    elif t == 3:
        listeliste.append([0, 'nom'])
        listeliste.append([1, 'theuv', 'nom'])
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
        listeliste.append([0, 'lanote'])
        listeliste.append([0, 'personnenote'])
        listeliste.append([1, 'themodule', 'nom'])
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
    """
        In the watch view to print the names
    
    :param t: it represent which kind of data it is (exemple: a groupe)
    :type t: int 
    """
    l = []
    if t == 1:
        l.append(['Nom', 1])
        l.append(['Ajout', 2])
    elif t == 2:
        l.append(['Nom', 1])
    elif t == 4:
        l.append(['Cours', 1])
        l.append(['Salles', 2])
        l.append(['Jour', 3])
        l.append(['Debut seamaine', 4])
        l.append(['Fin de seamaine', 5])
        l.append(['H debut', 6])
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
        l.append(['Celui qui a note', 4])
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
    """  
        link between t and the table's name
        
    :param t: it represent which kind of data it is (exemple: a groupe)
    :type t: int 
    
    """
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
    """
        To initiate the value of the forms in the modify view
        
    :param table: it represent which kind of data it is (exemple: a groupe)
    :type table: int 
    :param cond: previous condition
    :type cond: list of tuple
    :param conditions: previous condition
    :type conditions: list of tuple
    :param obj: object to modifie
    :type obj: Model
    
    """
    
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
        conditions.append(obj.lanote)
        cond.append(('personne', 0))
        conditions.append(obj.personnenote.id)
        cond.append(('module', 0))
        conditions.append(obj.themodule.id)
        
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
        cond.append(('theuv', 0))
        conditions.append(obj.theuv.id)
        
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
    """
        link between nomClasser and the name in the watch view
        
    :param t: it represent which kind of data it is (exemple: a groupe)
    :type t: int 
    :param nomClasser:represent witch column
    :type nomClasser: int
    
    """
   
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
            column = 'lanote'
        elif nomClasser == 2:
            column = 'personnenote'
        elif nomClasser == 3:
            column = 'themodule'
        else:
            column = 'uploadDate'
    elif t == 3:
        if nomClasser == 1:
            column = 'nom'
        else:
            column = 'theuv__nom'
    elif t == 7:
        if nomClasser == 1:
            column = 'nom'
        else:
            column = 'isExam'
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
    else:
        column = 'error'
    return column
def filtre(t):
    """ 
        What to filter in the watch view
    
    :param t: it represent which kind of data it is (exemple: a groupe)
    :type t: int 
    
    
    """
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
        l.append(['theuv', 'theuv', "", 'theuv__nom', 3])
    elif t == 6:
        l.append(['note', 'lanote', None, 'lanote', 0])
        l.append(['personne', 'personnenote', "", 'personnenote__filter__icontains', 0])
        l.append(['module', 'themodule', "", 'themodule__nom__icontains', 0])
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
def form(user, t, n, post=None):
    """
        Returns the form in the modify view or in the filter in the watch view
    
    :param user: not used yet
    :type user: not use yet
    :param t: it represent which kind of data it is (exemple: a groupe)
    :type t: int 
    :param n: if =0, it is filter ; if =2 it is change, if =3 it is a formset, else ids to add
    :type n: inr
    :param post: request.POST value
    :type post: request.POST of Django
    """
    
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
