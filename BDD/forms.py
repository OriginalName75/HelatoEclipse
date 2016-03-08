'''
Created on 23 oct. 2015

@author: Moran
'''

from ajax_select.fields import AutoCompleteSelectField, \
    AutoCompleteSelectMultipleField
from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.forms.formsets import BaseFormSet

from BDD.choices import SEXE, TYPE, INCONNU_STATUT, \
    INCONNU_STATUT_TYPE, SALLES, INCONNU_STATUT_SALLE, CHOICESNB, SEMAINE, LUNDI, \
    SEMAINEAAVECINCO, SEMAINEINCONNU
from BDD.models import UV, Personne, Module, Groupe, TypeCour, Salle
from Functions import addData, modiData

class semaine(forms.Form):
    nb = forms.IntegerField(label="Semaine :")




class nbAjout(forms.Form):
    nb = forms.ChoiceField(label="Combien d'ajout ? :", choices=CHOICESNB)

class changeCour(forms.Form):

    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")

    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        isExam = data['isExam']
        modiData.modCour(idP, nom, isExam)
class fitrerCour(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")
class fitrerCalendrier(forms.Form):
    typeCour = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom du type de cour', 'class':'form-control input-perso'}))
    salles = AutoCompleteSelectField('salles', required=False, help_text=None)
    jour = forms.ChoiceField(choices=SEMAINEAAVECINCO, initial=SEMAINEINCONNU)
    semaineMin = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Semaine Min', 'class':'form-control input-perso'}))
    semaineMax = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Semaine Max', 'class':'form-control input-perso'}))
    hmin = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'H Min', 'class':'form-control input-perso'}))
    hmax = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'H Max', 'class':'form-control input-perso'}))
    
class AjouterCalendrier(forms.Form):
    pass
class changeCalendrier(forms.Form):
    typeCour = AutoCompleteSelectField('typeCour', required=True, label="Type de cour", help_text=None)    
    jour = forms.ChoiceField(choices=SEMAINEAAVECINCO, initial=SEMAINEINCONNU)
    semaineMin = forms.IntegerField(required=False, label="Semaine Min", widget=forms.TextInput(attrs={'placeholder': 'Semaine Min', 'class':'form-control input-perso'}))
    semaineMax = forms.IntegerField(required=False, label="Semaine Max", widget=forms.TextInput(attrs={'placeholder': 'Semaine Max', 'class':'form-control input-perso'}))
    hmin = forms.IntegerField(required=False, label="H Min", widget=forms.TextInput(attrs={'placeholder': 'H Min', 'class':'form-control input-perso'}))
    hmax = forms.IntegerField(required=False, label="H max", widget=forms.TextInput(attrs={'placeholder': 'H Max', 'class':'form-control input-perso'}))
    def modif(self, idP):
        data = self.cleaned_data
        typeCour = data['typeCour']
        jour = data['jour']
        semaineMin = data['semaineMin']
        semaineMax = data['semaineMax']
        hmin = data['hmin']
        hmax = data['hmax']
        modiData.modCourLive(idP, typeCour=typeCour, jour=jour, semaineMin=semaineMin, semaineMax=semaineMax, hmin=hmin, hmax=hmax)
class BaseNoteFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseNoteFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
    def clean(self):
        
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
#         titles = []
#         for form in self.forms:
#             title = form.cleaned_data['title']
#             if title in titles:
#                 raise forms.ValidationError("Articles in a set must have distinct titles.")
#             titles.append(title)

class PersonneFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(PersonneFormSet, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False
    def clean(self):
        
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        logins = []
        for form in self.forms:
            login = form.cleaned_data['login']
            if login in logins:
                raise forms.ValidationError("Les logins doivent être deux à deux distinct")
            logins.append(login)
class NomFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(NomFormSet, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False
    def clean(self):
        
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        logins = []
        for form in self.forms:
            login = form.cleaned_data['nom']
            if login in logins:
                raise forms.ValidationError("Les noms doivent être deux à deux distinct")
            logins.append(login)
class moduleFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(moduleFormSet, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False
    def clean(self):
        
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        l = []
        for form in self.forms:
            nom = form.cleaned_data['nom']
            uv = form.cleaned_data['uv']
            for i in l:
                if i[0] == nom and uv == i[1]:
                    raise forms.ValidationError("Les modules doivent être deux à deux distinct par uv")
                    break
            
            l.append([nom, uv])

class notes(forms.Form):
    note = forms.FloatField(required=False, label="")
    nepasnoter = forms.BooleanField(required=False, label="Ne pas noter")
    def clean(self):
        if (self.cleaned_data.get('note') == None and (not self.cleaned_data.get('nepasnoter'))):

            raise ValidationError(
                "Veuillez ajouter une note ou cocher la case ne pas noter"
            )
        
        return self.cleaned_data  
    def save(self, solo, multi):
        if (not self.cleaned_data['nepasnoter']):
            
            addData.addNote(self.cleaned_data['note'], multi[0][0], solo[0])
class chooseGroupe(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['groupes']

    groupes = AutoCompleteSelectMultipleField('groupes', required=True, help_text=None)
    module = AutoCompleteSelectField('module', required=True, help_text=None)
class addGroupe(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['groupes']

    groupes = AutoCompleteSelectMultipleField('groupes', required=False, help_text=None)
    def __init__(self, *args, **kwargs):
        
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

    def savePerso(self, idP):
        groupes = self.cleaned_data['groupes']
        modiData.modPersonne(idP, groupes=groupes)
class addModule(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['modules']

    modules = AutoCompleteSelectMultipleField('module', required=False, help_text=None)


    def savePerso(self, idP):
        modules = self.cleaned_data['modules']
        modiData.modGroupe(idP, modules=modules)
class addSalle(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['salles']

    salles = AutoCompleteSelectMultipleField('salles', required=False, help_text=None)


    def savePerso(self, idP):
        salles = self.cleaned_data['salles']
        modiData.modCourLive(idP, salles=salles)
        
class addGroupeModule(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['groupes']

    groupes = AutoCompleteSelectMultipleField('groupes', required=False, help_text=None)
    def __init__(self, *args, **kwargs):
        
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

    def savePerso(self, idP):
        groupes = self.cleaned_data['groupes']
        modiData.modModule(idP, groupes=groupes)

class addTypeCour(forms.ModelForm):
    class Meta:
        model = TypeCour
        fields = ['groupe']
    
    groupe = AutoCompleteSelectMultipleField('groupes', required=False, help_text=None)    
    def savePerso(self, idP):
        
        groupe = self.cleaned_data['groupe']
        modiData.modCour(idP, groupes=groupe)
 
class addPersonnetypeCour(forms.ModelForm):
    class Meta:
        model = TypeCour
        fields = ['profs']
    
    profs = AutoCompleteSelectMultipleField('personnes', required=False, help_text=None)   
    def savePerso(self, idP):
        personnes = self.cleaned_data['profs']
        
        modiData.modCour(idP, profs=personnes)    
class addPersonne(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['personnes']
    
    personnes = AutoCompleteSelectMultipleField('personnes', required=False, help_text=None)
  
    

    def savePerso(self, idP):
        personnes = self.cleaned_data['personnes']
        
        modiData.modGroupe(idP, personnes=personnes)
class changeGroupe(forms.Form):

    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        modiData.modGroupe(idP, nom)    
class fitrerGroupe(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
class changeUV(forms.Form):
        
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']  
        modiData.modUV(idP, nom)      
class fitrerUV(forms.Form):
        
    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
class changeNote(forms.Form):
    
    note = forms.IntegerField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Note', 'class':'form-control input-perso'}))
    personne = AutoCompleteSelectField('personnes', required=True, help_text=None, label="Personne notée")
    module = AutoCompleteSelectField('module', required=True, help_text=None, label="Module")
    def modif(self, idP):
        data = self.cleaned_data
        note = data['note']
        personne = data['personne']
        module = data['module']
        modiData.modNote(idP, note, personne, module)
class fitrerNote(forms.Form):
    
    note = forms.IntegerField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'Note', 'class':'form-control input-perso'}))
    personne = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Personne', 'class':'form-control input-perso'}))
    module = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Module', 'class':'form-control input-perso'}))

class changeSalle(forms.Form):

    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)

    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        capacite = data['capacite']
        typee = data['type']
        modiData.modSalle(idP, nom, capacite, typee)
class fitrerSalle(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)

class changeModule(forms.Form):
    
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = AutoCompleteSelectField('uv', required=True, help_text=None)
    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        uv = data['uv']
        modiData.modModule(idP, nom, uv)
class fitrerModule(forms.Form):
    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'UV', 'class':'form-control input-perso'}))
class fitrerP(forms.Form):

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
    numeroDeTel = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone', 'class':'form-control input-perso'}), required=False)
    
class changeP(forms.Form):

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
    numeroDeTel = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone', 'class':'form-control input-perso'}), required=False)
    def modif(self, idP):
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
        modiData.modPersonne(int(idP), nom, prenom, login, None, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, mail) 

class AjouterP(forms.Form):
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
    numeroDeTel = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone', 'class':'form-control input-perso'}), required=False)
  
    def clean(self):

        if (self.cleaned_data.get('mdp') != 
            self.cleaned_data.get('mdp2')):

            raise ValidationError(
                "Les mots de passes sont différents"
            )
        if User.objects.filter(username=self.cleaned_data.get('login')).exists():
            raise ValidationError(
                "Le nom d'utilisateur est déjà utlisé"
            )
        return self.cleaned_data
    def save(self):
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
        addData.addPersonne(nom, prenom, login, mdp, sexe, typeP, adresse, promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, mail)
class AjouterNote(forms.Form):
    note = forms.IntegerField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Note', 'class':'form-control input-perso'}))
    personne = AutoCompleteSelectField('personnes', required=True, help_text=None)
    module = AutoCompleteSelectField('module', required=True, help_text=None)
    def save(self):
        data = self.cleaned_data
        note = data['note']
        personne = data['personne']
        module = data['module']
        addData.addNote(note, personne, module)            
class AjouterGroupe(forms.Form):
    nom = forms.CharField(required=True, label="", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    personne = AutoCompleteSelectMultipleField('personnes', required=False, help_text=None)
    modules = AutoCompleteSelectMultipleField('module', required=False, help_text=None, label="Module(s) noté(s)")
    def clean(self):

        if Groupe.objects.filter(nom=self.cleaned_data.get('nom')).exists():
            raise ValidationError(
                "Le nom de groupe est déjà utlisé"
            )
        return self.cleaned_data
    def save(self):
        
        data = self.cleaned_data
        nom = data['nom']
        personne = data['personne']
        modules = data['modules']
        return addData.addGroupe(nom, personnes=personne, modules=modules)
class AjouterCour(forms.Form):
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")
    def save(self):
        data = self.cleaned_data
        nom = data['nom']
        isExam = data['isExam']
        addData.addCour(nom, isExam)
class AjouterSalle(forms.Form):
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)
    def clean(self):

        if Salle.objects.filter(nom=self.cleaned_data.get('nom')).exists():
            raise ValidationError(
                "Le nom de la salle est déjà utlisé"
            )
        return self.cleaned_data
    def save(self):
        data = self.cleaned_data 
        nom = data['nom']
        capacite = data['capacite']
        typee = data['type']
        addData.addSalle(nom, capacite, typee)
class AjouterUV(forms.Form):
    nom = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def save(self):
        data = self.cleaned_data
        nom = data['nom']
        return addData.addUV(nom)
    def clean(self):

        if UV.objects.filter(nom=self.cleaned_data.get('nom')).exists():
            raise ValidationError(
                "Cet UV est déjà créé"
            )
        return self.cleaned_data   
class AjouterModule(forms.Form):
    
    nom = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = AutoCompleteSelectField('uv', required=True, help_text=None)
    def clean(self):

        if Module.objects.filter(nom=self.cleaned_data.get('nom'), uv=self.cleaned_data.get('uv')).exists():
            raise ValidationError(
                "Ce module est déjà créé pour cet uv"
            )
        return self.cleaned_data   
    def save(self):
        data = self.cleaned_data
        nom = data['nom']
        uv = data['uv']
        addData.addModule(nom, uv)
