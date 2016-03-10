# -*- coding: utf-8 -*-
"""
    The ''forms'' module
    ======================
    
    It represent all the forms of the administration of the site.
    
    :Exemples:
    
    >> form=AjouterCour() 
    >> form
    return html code of the form
    
    >> form=AjouterCour(request.POST) # request.POST is the results of a formula 
    >> form.is_valid()
    True/False
    
    >> form=AjouterCour(request.POST) # request.POST is the results of a formula 
    >> form.save()
    save the formula into the SQL
     
@author: IWIMBDSL
"""
from ajax_select.fields import AutoCompleteSelectField, \
    AutoCompleteSelectMultipleField
from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.forms.formsets import BaseFormSet

from BDD.choices import SEXE, TYPE, INCONNU_STATUT, \
    INCONNU_STATUT_TYPE, SALLES, INCONNU_STATUT_SALLE, CHOICESNB, \
    SEMAINEAAVECINCO, SEMAINEINCONNU
from BDD.models import UV, Personne, Module, Groupe, TypeCour, Salle
from Functions import addData, modiData

class langage(forms.Form):
    txt=forms.CharField(max_length=300)

class semaine(forms.Form):
    nb = forms.IntegerField(label="Semaine :")

class nbAjout(forms.Form):
    """
        Form which ask how much object the user want to add
        
        :Exemples:
    
        >> form=nbAjout() 
        >> form
        return html code with a single choice field (numbers between 1 to 20)
        
    """
    nb = forms.ChoiceField(label="Combien d'ajout ? :", choices=CHOICESNB)
  
class changeCour(forms.Form):
    """
        Form to change a type of lesson in the database. 
        
        :Exemples:
    
        >> form=changeCour() 
        >> form
        return html code of the form with 2 fields
        
        >> form=changeCour(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the type of lesson that the user wants to change 
        
        >> form=changeCour(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the type of lesson which id = 3 regarding the form fields
        
                
    """
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")

    def modif(self, idC, p):
        """
            changes the type of lesson selected regarding the form fields
            
        :param idP: the id of the lesson that the user wnts to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeCour(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the type of lesson which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        nom = data['nom']
        isExam = data['isExam']
        modiData.modCour(idC, p, nom, isExam)
class fitrerCour(forms.Form):
    """
        A form to filter a database 
        
        :Exemples:
    
        >> form=fitrerCour() 
        >> form
        return html code of the form
        
        >> form=fitrerCour(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the type of lesson that the user wants to filter 
                
    """
    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")
class fitrerCalendrier(forms.Form):
    """
        Form to filter lessons. 
        
        :Exemples:
    
        >> form=fitrerCalendrier() 
        >> form
        return html code of the form with 7 fields
        
        >> form=fitrerCalendrier(request.POST) 
        >> form.cleaned_data['jour']
        returns the day of the lesson that the user wants to filter 
                
    """

    typeCour = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom du type de cour', 'class':'form-control input-perso'}))
    salles = AutoCompleteSelectField('salles', required=False, help_text=None)
    jour = forms.ChoiceField(choices=SEMAINEAAVECINCO, initial=SEMAINEINCONNU)
    semaineMin = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Semaine Min', 'class':'form-control input-perso'}))
    semaineMax = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Semaine Max', 'class':'form-control input-perso'}))
    hmin = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'H Min', 'class':'form-control input-perso'}))
    hmax = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'H Max', 'class':'form-control input-perso'}))
    
class AjouterCalendrier(forms.Form):
    """
        A Form to add a lesson to the database. 
        
        :Exemples:
    
        >> form=AjouterCalendrier() 
        >> form
        return html code of the form with 7 fields
        
        >> form=AjouterCalendrier(request.POST) 
        >> form.cleaned_data['jour']
        returns the day of the lesson that the user wants to add 
        
        >> form=AjouterCalendrier(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the lesson
                
    """
    typeCour = AutoCompleteSelectField('typeCour', required=True, label="Type de cour", help_text=None)    
    jour = forms.ChoiceField(choices=SEMAINEAAVECINCO, initial=SEMAINEINCONNU, required=True)
    salles = AutoCompleteSelectMultipleField('salles', required=True, help_text=None)
    semaineMin = forms.IntegerField(required=True, label="Semaine Min", widget=forms.TextInput(attrs={'placeholder': 'Semaine Min', 'class':'form-control input-perso'}))
    semaineMax = forms.IntegerField(required=True, label="Semaine Max", widget=forms.TextInput(attrs={'placeholder': 'Semaine Max', 'class':'form-control input-perso'}))
    hmin = forms.IntegerField(required=True, label="H Min", widget=forms.TextInput(attrs={'placeholder': 'H Min', 'class':'form-control input-perso'}))
    hmax = forms.IntegerField(required=True, label="H max", widget=forms.TextInput(attrs={'placeholder': 'H Max', 'class':'form-control input-perso'}))
    def clean(self):
        """
           Overwrite django clean() function. It adds additional requirements of the form
           It checks if the weeks and the hours are set correctly by the user in the form
           
           clean() is used in the is_valid() function of a form
           
        """
        
        if (self.cleaned_data.get('semaineMin') == None or self.cleaned_data.get('semaineMax') == None or self.cleaned_data.get('semaineMin') > 52 or self.cleaned_data.get('semaineMin') < 0 or self.cleaned_data.get('semaineMax') > 52 or self.cleaned_data.get('semaineMax') < 0):

            raise ValidationError(
                "Les semaines doivent etre positives et strictement plus petit que 53"
            )
        if (self.cleaned_data.get('semaineMax') < self.cleaned_data.get('semaineMin')):

            raise ValidationError(
                "Les semaine min doit etre < que semaine max"
            )
        if (self.cleaned_data.get('hmax') == None or self.cleaned_data.get('hmin') == None or self.cleaned_data.get('hmax') < self.cleaned_data.get('hmin')):

            raise ValidationError(
                "Les h min doit etre < que h max"
            )
        if (self.cleaned_data.get('hmin') < 0 or self.cleaned_data.get('hmin') > 10 or self.cleaned_data.get('hmax') < 0 or self.cleaned_data.get('hmax') > 10):

            raise ValidationError(
                "Les heures doivent etre positives et strictement plus petite que 11"
            )
        return self.cleaned_data
    def save(self, p):
        """
            Add a lesson the the database regarding the form
            
        :param p: the user
        :type p: Personne
        :return: id of the new lesson in the database
        :rtype: int
        
        >> form=AjouterCalendrier(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the lesson
        
        """
        
        data = self.cleaned_data
        typeCour = data['typeCour']
        jour = data['jour']
        salles = data['salles']
        semaineMin = data['semaineMin']
        semaineMax = data['semaineMax']
        hmin = data['hmin']
        hmax = data['hmax']
        return addData.addCalendrier(p, typeCour, jour, semaineMin, semaineMax, hmin, hmax, salles)
class changeCalendrier(forms.Form):
    """
        Form to change a lesson in the database. 
        
        :Exemples:
    
        >> form=changeCalendrier() 
        >> form
        return html code of the form with 7 fields
        
        >> form=changeCalendrier(request.POST) 
        >> form.cleaned_data['jour']
        returns the day of the lesson that the user wants to change 
        
        >> form=changeCalendrier(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the type of lesson which id = 3 regarding the form fields
        
                
    """
    typeCour = AutoCompleteSelectField('typeCour', required=True, label="Type de cour", help_text=None)    
    jour = forms.ChoiceField(choices=SEMAINEAAVECINCO, initial=SEMAINEINCONNU)
    semaineMin = forms.IntegerField(required=False, label="Semaine Min", widget=forms.TextInput(attrs={'placeholder': 'Semaine Min', 'class':'form-control input-perso'}))
    semaineMax = forms.IntegerField(required=False, label="Semaine Max", widget=forms.TextInput(attrs={'placeholder': 'Semaine Max', 'class':'form-control input-perso'}))
    hmin = forms.IntegerField(required=False, label="H Min", widget=forms.TextInput(attrs={'placeholder': 'H Min', 'class':'form-control input-perso'}))
    hmax = forms.IntegerField(required=False, label="H max", widget=forms.TextInput(attrs={'placeholder': 'H Max', 'class':'form-control input-perso'}))
    def modif(self, idP, p):
        """
            changes the lesson selected regarding the form fields
            
        :param idP: the id of the lesson that the user wnts to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeCalendrier(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the lesson which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        typeCour = data['typeCour']
        jour = data['jour']
        semaineMin = data['semaineMin']
        semaineMax = data['semaineMax']
        hmin = data['hmin']
        hmax = data['hmax']
        modiData.modCourLive(idP, p, typeCour=typeCour, jour=jour, semaineMin=semaineMin, semaineMax=semaineMax, hmin=hmin, hmax=hmax)
class BaseNoteFormSet(BaseFormSet):
    """
        class for multiple forms in a same template
        
    """
    def __init__(self, *args, **kwargs):
        """
           Overwrite django __init__() so empty fields are not permitted
           
        """
        super(BaseNoteFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
    def clean(self):
        """
           Overwrite django clean() function to check all the forms
           
           clean() is used in the is_valid() function of a formset
           
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
#         titles = []
#         for form in self.forms:
#             title = form.cleaned_data['title']
#             if title in titles:
#                 raise forms.ValidationError("Articles in a set must have distinct titles.")
#             titles.append(title)
class CalendrierFormSet(BaseFormSet):
    """
        class for multiple forms in a same template
        
    """
    def __init__(self, *args, **kwargs):
        """
           Overwrite django __init__() so empty fields are not permitted
           
        """
        super(CalendrierFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            
            form.empty_permitted = False
    def clean(self):
        """
           Overwrite django clean() function to check all the forms in the formset
           
           clean() is used in the is_valid() function of a formset
           
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
    
class PersonneFormSet(BaseFormSet):
    """
        class for multiple forms in a same template
        
    """
    def __init__(self, *args, **kwargs):
        """
           Overwrite django __init__() so empty fields are not permitted
           
        """
        super(PersonneFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
    def clean(self):
        """
           Overwrite django clean() function to check all the forms in the formset
           Moreover, logins must be different
           
           clean() is used in the is_valid() function of a formset
           
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        logins = []
        for form in self.forms:
            login = form.cleaned_data['login']
            if login in logins:
                raise forms.ValidationError("Les logins doivent etre deux a deux distinct")
            logins.append(login)
class NomFormSet(BaseFormSet):
    """
        class for multiple forms in a same template
        
    """
    def __init__(self, *args, **kwargs):
        """
           Overwrite django __init__() so empty fields are not permitted
           
        """
        super(NomFormSet, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False
    def clean(self):
        """
           Overwrite django clean() function to check all the forms in the formset
           Moreover, names must be different
           
           clean() is used in the is_valid() function of a formset
           
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        logins = []
        for form in self.forms:
            login = form.cleaned_data['nom']
            if login in logins:
                raise forms.ValidationError("Les noms doivent etre deux a deux distinct")
            logins.append(login)
class moduleFormSet(BaseFormSet):
    """
        class for multiple forms in a same template
        
    """
    def __init__(self, *args, **kwargs):
        """
           Overwrite django __init__() so empty fields are not permitted
           
        """
        super(moduleFormSet, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False
    def clean(self):
        """
           Overwrite django clean() function to check all the forms in the formset
           Moreover, names must be different in a same UV
           
           clean() is used in the is_valid() function of a formset
           
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        l = []
        for form in self.forms:
            nom = form.cleaned_data['nom']
            uv = form.cleaned_data['uv']
            for i in l:
                if i[0] == nom and uv == i[1]:
                    raise forms.ValidationError("Les modules doivent etre deux a deux distinct par uv")
                    break
            
            l.append([nom, uv])

class notes(forms.Form):
    """
        A form to mark persons in a group
        
    """
    note = forms.FloatField(required=False, label="")
    nepasnoter = forms.BooleanField(required=False, label="Ne pas noter")
    def clean(self):
        """
           Overwrite django clean() function. It adds additional requirements of the form
           It checks if the mark is set correctly by the user in the form
           
           clean() is used in the is_valid() function of a form
           
        """
        if (self.cleaned_data.get('note') == None and (not self.cleaned_data.get('nepasnoter'))):

            raise ValidationError(
                "Veuillez ajouter une note ou cocher la case ne pas noter"
            )
        
        return self.cleaned_data  
    def save(self, p, solo, multi, prof):
        """
            Add a mark in the database
            
        :param p: The user
        :type p: Personne
        :param solo: the module that the persons are marked
        :type solo:  List of modules
        :param multi: The persons marked 
        :type multi: list of list of list of Personne
        :param prof: Teacher who has mark the group
        :type prof: Personne
        """
        
        if (not self.cleaned_data['nepasnoter']):
            
            addData.addNote(p, self.cleaned_data['note'], multi[0][0], solo[0], prof)
class chooseGroupe(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = Personne
        fields = ['groupes']

    groupes = AutoCompleteSelectMultipleField('groupes', required=True, help_text=None)
    module = AutoCompleteSelectField('module', required=True, help_text=None)
class addGroupe(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = Personne
        fields = ['groupes']

    groupes = AutoCompleteSelectMultipleField('groupes', required=False, help_text=None)
    def __init__(self, *args, **kwargs):
        """
            Overwrite usual initiation of the class so the form is correctly filled
            
        """
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if 'instance' in kwargs:
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.                
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['groupes'] = [t.pk for t in kwargs['instance'].groupe_set.all()]
        super(addGroupe, self).__init__(*args, **kwargs)

    def savePerso(self, idP, p):
        """
            Changes the person selected regarding the form fields
            
        :param idP: the id of the person to modify
        :type idP: int 
        :param p: the user
        :type p: Personne
        
        :exemple:
        
        >> form=addGroupe(request.POST) 
        >> if form.is_valid():
        >>     form.savePerso(3, request.user.personne)
        modify in the database the person which id is 3 regarding what is in the form
        
        """
        
        groupes = self.cleaned_data['groupes']
        modiData.modPersonne(p, idP, groupes=groupes)
class addModule(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = Groupe
        fields = ['modules']

    modules = AutoCompleteSelectMultipleField('module', required=False, help_text=None)


    def savePerso(self, idP, p):
        """
            Changes the group selected regarding the form fields
            
        :param idP: the id of the group to modify
        :type idP: int 
        :param p: the user
        :type p: Personne
        
        :exemple:
        
        >> form=addModule(request.POST) 
        >> if form.is_valid():
        >>     form.savePerso(3, request.user.personne)
        modify in the database the group which id is 3 regarding what is in the form
        
        """
        modules = self.cleaned_data['modules']
        modiData.modGroupe(idP, p, modules=modules)
class addSalle(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = Salle
        fields = ['salles']

    salles = AutoCompleteSelectMultipleField('salles', required=False, help_text=None)


    def savePerso(self, idP, p):
        """
            Changes the lesson selected regarding the form fields
            
        :param idP: the id of the lesson to modify
        :type idP: int 
        :param p: the user
        :type p: Personne
        
        :exemple:
        
        >> form=addSalle(request.POST) 
        >> if form.is_valid():
        >>     form.savePerso(3, request.user.personne)
        modify in the database the lesson which id is 3 regarding what is in the form
        
        """
        salles = self.cleaned_data['salles']
        modiData.modCourLive(idP, p, salles=salles)
        
class addGroupeModule(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = Module
        fields = ['groupes']

    groupes = AutoCompleteSelectMultipleField('groupes', required=False, help_text=None)
    def __init__(self, *args, **kwargs):
        """
            Overwrite usual initiation of the class so the form is correctly filled
            
        """
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if 'instance' in kwargs:
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.                
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['groupes'] = [t.pk for t in kwargs['instance'].groupe_set.all()]
        super(addGroupeModule, self).__init__(*args, **kwargs)

    def savePerso(self, idP, p):
        """
            Changes the module selected regarding the form fields
            
        :param idP: the id of the module to modify
        :type idP: int 
        :param p: the user
        :type p: Personne
        
        :exemple:
        
        >> form=addGroupeModule(request.POST) 
        >> if form.is_valid():
        >>     form.savePerso(3, request.user.personne)
        modify in the database the module which id is 3 regarding what is in the form
        
        """
        groupes = self.cleaned_data['groupes']
        modiData.modModule(idP, p, groupes=groupes)

class addTypeCour(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = TypeCour
        fields = ['groupe']
    
    groupe = AutoCompleteSelectMultipleField('groupes', required=False, help_text=None)    
    def savePerso(self, idP, p):
        """
            Changes the type of lesson selected regarding the form fields
            
        :param idP: the id of the type of lesson to modifie
        :type idP: int 
        :param p: the user
        :type p: Personne
        
        :exemple:
        
        >> form=addTypeCour(request.POST) 
        >> if form.is_valid():
        >>     form.savePerso(3, request.user.personne)
        modify in the database the the type of lesson which id is 3 regarding what is in the form
        
        """
        groupe = self.cleaned_data['groupe']
        modiData.modCour(idP, p,  groupes=groupe)
 
class addPersonnetypeCour(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = TypeCour
        fields = ['profs']
    
    profs = AutoCompleteSelectMultipleField('personnes', required=False, help_text=None)   
    def savePerso(self, idP, p):
        """
            Changes the type of lesson selected regarding the form fields
            
        :param idP: the id of the type of lesson to modify
        :type idP: int 
        :param p: the user
        :type p: Personne
        
        :exemple:
        
        >> form=addPersonnetypeCour(request.POST) 
        >> if form.is_valid():
        >>     form.savePerso(3, request.user.personne)
        modify in the database the person which id is 3 regarding what is in the form
        
        """
        personnes = self.cleaned_data['profs']
        
        modiData.modCour(idP,p, profs=personnes)    
class addPersonne(forms.ModelForm):
    """
        A form that find with an AJAX script data regarding what is on the fields in the form.
        It is more or less like google: it update itself when the user adds or delete a letter in a field.
            
    """
    class Meta:
        """
            Overwrite Django ModelForm to limit the number of field
            
        """
        model = Personne
        fields = ['personnes']
    
    personnes = AutoCompleteSelectMultipleField('personnes', required=False, help_text=None)
  
    

    def savePerso(self, idP, p):
        """
            Changes the group selected regarding the form fields
            
        :param idP: the id of the group to modify
        :type idP: int 
        :param p: the user
        :type p: Personne
        
        :exemple:
        
        >> form=addPersonne(request.POST) 
        >> if form.is_valid():
        >>     form.savePerso(3, request.user.personne)
        modify in the database the group which id is 3 regarding what is in the form
        
        """
        personnes = self.cleaned_data['personnes']
        
        modiData.modGroupe(idP, p, personnes=personnes)
class changeGroupe(forms.Form):
    """
        Form to change a group in the database. 
        
        :Exemples:
    
        >> form=changeGroupe() 
        >> form
        return html code of the form with a Char field
        
        >> form=changeGroupe(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the group that the user wants to change 
        
        >> form=changeGroupe(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the group which id = 3 regarding the form fields
        
                
    """
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def modif(self, idP, p):
        """
            changes the group selected regarding the form fields
            
        :param idP: the id of the group that the user wants to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeGroupe(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the group which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        nom = data['nom']
        modiData.modGroupe(idP, p, nom)    
class fitrerGroupe(forms.Form):
    """
        A form to filter groups
        
        :Exemples:
    
        >> form=fitrerGroupe() 
        >> form
        return html code of the form
        
        >> form=fitrerGroupe(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the group that the user wants to filter 
                
    """
    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
class changeUV(forms.Form):
    """
        Form to change an UV in the database. 
        
        :Exemples:
    
        >> form=changeUV() 
        >> form
        return html code of the form with a char field
        
        >> form=changeUV(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the UV that the user wants to change 
        
        >> form=changeUV(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the UV which id = 3 regarding the form fields
        
                
    """ 
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def modif(self, idP, p):
        """
            changes the UV selected regarding the form fields
            
        :param idP: the id of the lesson that the user wnts to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeUV(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the UV which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        nom = data['nom']  
        modiData.modUV(idP, p, nom)      
class fitrerUV(forms.Form):
    """
        A form to filter UVs
        
        :Exemples:
    
        >> form=fitrerUV() 
        >> form
        return html code of the form
        
        >> form=fitrerUV(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the UV that the user wants to filter 
                
    """
        
    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
class changeNote(forms.Form):
    """
        Form to change a mark in the database. 
        
        :Exemples:
    
        >> form=changeNote() 
        >> form
        return html code of the form with 3 fields
        
        >> form=changeNote(request.POST) 
        >> form.cleaned_data['note']
        returns the mark that the user wants to change 
        
        >> form=changeNote(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the mark which id = 3 regarding the form fields
        
                
    """
    note = forms.IntegerField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Note', 'class':'form-control input-perso'}))
    personne = AutoCompleteSelectField('personnes', required=True, help_text=None, label="Personne notee")
    module = AutoCompleteSelectField('module', required=True, help_text=None, label="Module")
    def modif(self, idP, p):
        """
            changes the mark selected regarding the form fields
            
        :param idP: the id of the mark that the user wnts to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeNote(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the mark which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        note = data['note']
        personne = data['personne']
        module = data['module']
        modiData.modNote(idP, p, note, personne, module)
class fitrerNote(forms.Form):
    """
        A form to filter marks
        
        :Exemples:
    
        >> form=fitrerNote() 
        >> form
        return html code of the form
        
        >> form=fitrerNote(request.POST) 
        >> form.cleaned_data['note']
        returns the mark that the user wants to filter 
                
    """
    
    note = forms.IntegerField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'Note', 'class':'form-control input-perso'}))
    personne = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Personne', 'class':'form-control input-perso'}))
    module = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Module', 'class':'form-control input-perso'}))

class changeSalle(forms.Form):
    """
        Form to change a classroom in the database. 
        
        :Exemples:
    
        >> form=changeSalle() 
        >> form
        return html code of the form with 3 fields
        
        >> form=changeSalle(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the classroom that the user wants to change 
        
        >> form=changeSalle(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the classroom which id = 3 regarding the form fields
        
                
    """
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)

    def modif(self, idP, p):
        """
            changes the classroom selected regarding the form fields
            
        :param idP: the id of the classroom that the user wnts to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeSalle(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the classroom which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        nom = data['nom']
        capacite = data['capacite']
        typee = data['type']
        modiData.modSalle(idP, p, nom, capacite, typee)
class fitrerSalle(forms.Form):
    """
        A form to filter classrooms
        
        :Exemples:
    
        >> form=fitrerSalle() 
        >> form
        return html code of the form
        
        >> form=fitrerSalle(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the classroom that the user wants to filter 
                
    """

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)

class changeModule(forms.Form):
    """
        Form to change a module in the database. 
        
        :Exemples:
    
        >> form=changeModule() 
        >> form
        return html code of the form with 2 fields
        
        >> form=changeModule(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the module that the user wants to change 
        
        >> form=changeModule(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the module which id = 3 regarding the form fields
        
                
    """
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = AutoCompleteSelectField('uv', required=True, help_text=None)
    def modif(self, idP, p):
        """
            changes the module selected regarding the form fields
            
        :param idP: the id of the module that the user wnts to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeModule(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the module which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        nom = data['nom']
        uv = data['uv']
        modiData.modModule(idP, p, nom, uv)
class fitrerModule(forms.Form):
    """
        A form to filter modules 
        
        :Exemples:
    
        >> form=fitrerModule() 
        >> form
        return html code of the form
        
        >> form=fitrerModule(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the module that the user wants to filter 
                
    """
    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'UV', 'class':'form-control input-perso'}))
class fitrerP(forms.Form):
    """
        A form to filter persons
        
        :Exemples:
    
        >> form=fitrerP() 
        >> form
        return html code of the form
        
        >> form=fitrerP(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the person that the user wants to filter 
                
    """
    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    prenom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Prenom', 'class':'form-control input-perso'}))
    login = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'class':'form-control input-perso'}), max_length=30)
    mail = forms.EmailField(required=False, max_length=100, label="", widget=forms.TextInput(attrs={'placeholder': 'Mail', 'class':'form-control input-perso'}))
    sexe = forms.ChoiceField(label="", choices=SEXE, initial=INCONNU_STATUT)
    adresse = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Adresse', 'class':'form-control input-perso'}), max_length=300)
    promotion = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Promotion', 'class':'form-control input-perso'}), required=False)
    typeP = forms.ChoiceField(label="", choices=TYPE, initial=INCONNU_STATUT_TYPE)
    dateDeNaissance = forms.DateField(label="", required=False, input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'placeholder': 'Date naissance :jj/mm/aaaa', 'class':'form-control input-perso'}))
    lieuDeNaissance = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Lieu de Naissance', 'class':'form-control input-perso'}), required=False, max_length=100)
    numeroDeTel = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Numero de telephone', 'class':'form-control input-perso'}), required=False)
    
class changeP(forms.Form):
    """
        Form to change a person in the database. 
        
        :Exemples:
    
        >> form=changeP() 
        >> form
        return html code of the form
        
        >> form=changeP(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the person that the user wants to change 
        
        >> form=changeP(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the person which id = 3 regarding the form fields
        
                
    """
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    prenom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Prenom', 'class':'form-control input-perso'}))
    login = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'class':'form-control input-perso'}), max_length=30)
    mail = forms.EmailField(required=False, max_length=100, label="", widget=forms.TextInput(attrs={'placeholder': 'Mail', 'class':'form-control input-perso'}))
    sexe = forms.ChoiceField(label="", choices=SEXE, initial=INCONNU_STATUT)
    adresse = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Adresse', 'class':'form-control input-perso'}), max_length=300)
    promotion = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Promotion', 'class':'form-control input-perso'}), required=False)
    typeP = forms.ChoiceField(label="", choices=TYPE, initial=INCONNU_STATUT_TYPE)
    dateDeNaissance = forms.DateField(label="", required=False, input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'placeholder': 'Date naissance :jj/mm/aaaa', 'class':'form-control input-perso'}))
    lieuDeNaissance = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Lieu de Naissance', 'class':'form-control input-perso'}), required=False, max_length=100)
    numeroDeTel = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Numero de telephone', 'class':'form-control input-perso'}), required=False)
    def modif(self, idP, p):
        """
            changes the person selected regarding the form fields
            
        :param idP: the id of the person that the user wnts to change
        :type idP: int
        :param p: the user
        :type p: Personne
        
        :exemple:
        >> form=changeP(request.POST) 
        >> if form.is_valid():
        >>     form.modif(3, request.user.personne)
        changes the person which id = 3 regarding the form fields
        
        """
        data = self.cleaned_data
        nom = data['nom']
        prenom = data['prenom']
        login = data['login']
        mail = data['mail']
        sexe = data['sexe']
        adresse = data['adresse']
        promotion = data['promotion']
        typeP = data['typeP']
        dateDeNaissance = data['dateDeNaissance']
        lieuDeNaissance = data['lieuDeNaissance']
        numeroDeTel = data['numeroDeTel']
        modiData.modPersonne(p, int(idP), nom, prenom, login, None, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, mail) 

class AjouterP(forms.Form):
    """
        A Form to add a person to the database. 
        
        :Exemples:
    
        >> form=AjouterP() 
        >> form
        return html code of the form
        
        >> form=AjouterP(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the person that the user wants to add 
        
        >> form=AjouterP(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the person
                
    """
    nom = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    prenom = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Prenom', 'class':'form-control input-perso'}))
    login = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'class':'form-control input-perso'}), max_length=30, min_length=3)
    mdp = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class':'form-control input-perso'}), max_length=50, min_length=6)
    mdp2 = forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez Mot de passe', 'class':'form-control input-perso'}), max_length=50, min_length=6)
    mail = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder': 'Email', 'class':'form-control input-perso'}), required=False, max_length=200)
    sexe = forms.ChoiceField(label="", choices=SEXE, initial=INCONNU_STATUT)
    adresse = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'adresse', 'class':'form-control input-perso'}), required=False, max_length=300)
    promotion = forms.IntegerField(label="", widget=forms.TextInput(attrs={'placeholder': 'Promotion', 'class':'form-control input-perso'}), required=False)
    typeP = forms.ChoiceField(label="", required=False, choices=TYPE, initial=INCONNU_STATUT_TYPE)
    dateDeNaissance = forms.DateField(label="", required=False, input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'placeholder': 'Naissance : jj/mm/aaaa', 'class':'form-control input-perso'}))
    lieuDeNaissance = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Lieu de naissance', 'class':'form-control input-perso'}), required=False, max_length=300)
    numeroDeTel = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Numero de telephone', 'class':'form-control input-perso'}), required=False)
  
    def clean(self):
        """
           Overwrite django clean() function. It adds additional requirements of the form
           It checks if the password and the login are set correctly by the user in the form
           
           clean() is used in the is_valid() function of a form
           
        """
        if (self.cleaned_data.get('mdp') != 
            self.cleaned_data.get('mdp2')):

            raise ValidationError(
                "Les mots de passes sont differents"
            )
        if User.objects.filter(username=self.cleaned_data.get('login')).exists():
            raise ValidationError(
                "Le nom d'utilisateur est deja utlise"
            )
        return self.cleaned_data
    def save(self, p):
        """
            Add a person the the database regarding the form
            
        :param p: the user
        :type p: Personne
        :return: id of the new lesson in the database
        :rtype: int
        
        >> form=AjouterP(request.POST) 
        >> if form.is_valid():
        >>     form.save(request.user.person)
        save in the database the person
        
        """
        data = self.cleaned_data
        nom = data['nom']
        prenom = data['prenom']
        login = data['login']
        mdp = data['mdp']
        mail = data['mail']
        sexe = data['sexe']
        adresse = data['adresse']
        promotion = data['promotion']
        typeP = data['typeP']
        dateDeNaissance = data['dateDeNaissance']
        lieuDeNaissance = data['lieuDeNaissance']
        numeroDeTel = data['numeroDeTel']
        addData.addPersonne(p, nom, prenom, login, mdp, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, mail)
class AjouterNote(forms.Form):
    """
        A Form to add a mark to the database. 
        
        :Exemples:
    
        >> form=AjouterNote() 
        >> form
        return html code of the form 
        
        >> form=AjouterNote(request.POST) 
        >> form.cleaned_data['note']
        returns the mark that the user wants to add 
        
        >> form=AjouterNote(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the mark
                
    """
    note = forms.IntegerField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Note', 'class':'form-control input-perso'}))
    personne = AutoCompleteSelectField('personnes', required=True, help_text=None)
    module = AutoCompleteSelectField('module', required=True, help_text=None)
    def save(self, prof):
        data = self.cleaned_data
        note = data['note']
        personne = data['personne']
        module = data['module']
        addData.addNote(prof, note, personne, module, prof)            
class AjouterGroupe(forms.Form):
    """
        A Form to add a group to the database. 
        
        :Exemples:
    
        >> form=AjouterGroupe() 
        >> form
        return html code of the form 
        
        >> form=AjouterGroupe(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the group that the user wants to add 
        
        >> form=AjouterGroupe(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the group
                
    """
    nom = forms.CharField(required=True, label="", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    personne = AutoCompleteSelectMultipleField('personnes', required=False, help_text=None)
    modules = AutoCompleteSelectMultipleField('module', required=False, help_text=None, label="Module(s) note(s)")
    def clean(self):
        """
           Overwrite django clean() function. It adds additional requirements of the form
           It checks if the name is set correctly by the user in the form
           
           clean() is used in the is_valid() function of a form
           
        """
        if Groupe.objects.filter(nom=self.cleaned_data.get('nom')).exists():
            raise ValidationError(
                "Le nom de groupe est deja utlise"
            )
        return self.cleaned_data
    def save(self, pers):
        
        data = self.cleaned_data
        nom = data['nom']
        personne = data['personne']
        modules = data['modules']
        return addData.addGroupe(pers, nom, personnes=personne, modules=modules)
class AjouterCour(forms.Form):
    """
        A Form to add a type of lesson to the database. 
        
        :Exemples:
    
        >> form=AjouterCour() 
        >> form
        return html code of the form 
        
        >> form=AjouterCour(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the of the lesson that the user wants to add 
        
        >> form=AjouterCour(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the type of lesson
                
    """
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")
    def save(self,p):
        data = self.cleaned_data
        nom = data['nom']
        isExam = data['isExam']
        addData.addCour(p,nom, isExam)
class AjouterSalle(forms.Form):
    """
        A Form to add a classroom to the database. 
        
        :Exemples:
    
        >> form=AjouterSalle() 
        >> form
        return html code of the form 
        
        >> form=AjouterSalle(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the classroom that the user wants to add 
        
        >> form=AjouterSalle(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the classroom
                
    """
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)
    def clean(self):
        """
           Overwrite django clean() function. It adds additional requirements of the form
           It checks if the name is set correctly by the user in the form
           
           clean() is used in the is_valid() function of a form
           
        """
        if Salle.objects.filter(nom=self.cleaned_data.get('nom')).exists():
            raise ValidationError(
                "Le nom de la salle est deja utlise"
            )
        return self.cleaned_data
    def save(self, p):
        """
            Add a classroom the the database regarding the form
            
        :param p: the user
        :type p: Personne
        :return: id of the new lesson in the database
        :rtype: int
        
        >> form=AjouterP(request.POST) 
        >> if form.is_valid():
        >>     form.save(request.user.person)
        save in the database the classroom
        
        """
        data = self.cleaned_data 
        nom = data['nom']
        capacite = data['capacite']
        typee = data['type']
        addData.addSalle(p, nom, capacite, typee)
class AjouterUV(forms.Form):
    """
        A Form to add a UV to the database. 
        
        :Exemples:
    
        >> form=AjouterUV() 
        >> form
        return html code of the form 
        
        >> form=AjouterUV(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the UV that the user wants to add 
        
        >> form=AjouterUV(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the UV
                
    """
    nom = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))

    def save(self, p):
        """
            Add an UV the the database regarding the form
            
        :param p: the user
        :type p: Personne
        :return: id of the new lesson in the database
        :rtype: int
        
        >> form=AjouterUV(request.POST) 
        >> if form.is_valid():
        >>     form.save(request.user.person)
        save in the database the UV
        
        """
        data = self.cleaned_data
        nom = data['nom']
        return addData.addUV(p, nom)
    def clean(self):
        """
           Overwrite django clean() function. It adds additional requirements of the form
           It checks if the name is set correctly by the user in the form
           
           clean() is used in the is_valid() function of a form
           
        """
        if UV.objects.filter(nom=self.cleaned_data.get('nom')).exists():
            raise ValidationError(
                "Cet UV est deja cree"
            )
        return self.cleaned_data   
class AjouterModule(forms.Form):
    """
        A Form to add a module to the database. 
        
        :Exemples:
    
        >> form=AjouterModule() 
        >> form
        return html code of the form 
        
        >> form=AjouterModule(request.POST) 
        >> form.cleaned_data['nom']
        returns the name of the module that the user wants to add 
        
        >> form=AjouterModule(request.POST) 
        >> if form.is_valid():
        >>     form.save()
        save in the database the module
                
    """
    nom = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = AutoCompleteSelectField('uv', required=True, help_text=None)
    def clean(self):
        """
           Overwrite django clean() function. It adds additional requirements of the form
           It checks if the module is set correctly by the user in the form
           
           clean() is used in the is_valid() function of a form
           
        """
        if Module.objects.filter(nom=self.cleaned_data.get('nom'), uv=self.cleaned_data.get('uv')).exists():
            raise ValidationError(
                "Ce module est deja cree pour cet uv"
            )
        return self.cleaned_data   
    def save(self, p):
        """
            Add a module the the database regarding the form
            
        :param p: the user
        :type p: Personne
        :return: id of the new lesson in the database
        :rtype: int
        
        >> form=AjouterModule(request.POST) 
        >> if form.is_valid():
        >>     form.save(request.user.person)
        save in the database the module
        
        """
        data = self.cleaned_data
        nom = data['nom']
        uv = data['uv']
        addData.addModule(p, nom, uv)