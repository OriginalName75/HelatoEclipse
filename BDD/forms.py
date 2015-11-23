'''
Created on 23 oct. 2015

@author: Moran
'''
from asyncio.tasks import Task

from ajax_select.fields import AutoCompleteField, AutoCompleteSelectField, \
    AutoCompleteSelectMultipleField
from django import forms
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
from django.forms import ValidationError
from django.forms.models import ModelForm

from BDD.choices import SEXE, TYPE, INCONNU_STATUT, \
    INCONNU_STATUT_TYPE, SALLES, INCONNU_STATUT_SALLE, CHOICESNB
from BDD.models import UV, Personne, Module, Groupe
from Functions import addData, modiData


class nbAjout(forms.Form):
    nb = forms.ChoiceField(label="Combien d'ajout ? :", choices=CHOICESNB)
class fitrerCour(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")

    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        isExam = data['isExam']
        modiData.modCour(idP, nom, isExam)
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

class addPersonne(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['personnes']
    
    personnes = AutoCompleteSelectMultipleField('personnes', required=False, help_text=None)
    
    

    def savePerso(self, idP):
        personnes = self.cleaned_data['personnes']
        
        modiData.modGroupe(idP, personnes=personnes)
        
class fitrerGroupe(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        modiData.modGroupe(idP, nom)
class fitrerUV(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        modiData.modUV(idP, nom)
class fitrerNote(forms.Form):
    
    note = forms.IntegerField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Note', 'class':'form-control input-perso'}))
    personne = forms.ModelChoiceField(queryset=Personne.objects.all(), label="Personne notée")
    module = forms.ModelChoiceField(queryset=Module.objects.all(), label="Module")
    def modif(self, idP):
        data = self.cleaned_data
        note = data['note']
        personne = data['personne']
        module = data['module']
        modiData.modNote(idP, note, personne, module)
class fitrerSalle(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)

    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        capacite = data['capacite']
        typee = data['type']
        modiData.modSalle(idP, nom, capacite, typee)
class fitrerAnnee(forms.Form):

    annee = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Année', 'class':'form-control input-perso'}))
    def modif(self, idP):
        data = self.cleaned_data 
        annee = data['annee']
        modiData.modAnnee(idP, annee)
class fitrerModule(forms.Form):

    nom = forms.CharField(required=False, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = forms.ModelChoiceField(queryset=UV.objects.all(), label="UV")
    def modif(self, idP):
        data = self.cleaned_data
        nom = data['nom']
        uv = data['uv']
        modiData.modModule(idP, nom, uv)
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
    personne = forms.ModelChoiceField(required=True, queryset=Personne.objects.all(), label="Personne notée")
    module = forms.ModelChoiceField(required=True, queryset=Module.objects.all(), label="Module")
    def save(self):
        data = self.cleaned_data
        note = data['note']
        personne = data['personne']
        module = data['module']
        addData.addNote(note, personne, module)            
class AjouterGroupe(forms.Form):
    nom = forms.CharField(required=True, label="", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    def clean(self):

        if Groupe.objects.filter(nom=self.cleaned_data.get('nom')).exists():
            raise ValidationError(
                "Le nom de groupe est déjà utlisé"
            )
        return self.cleaned_data
    def save(self):
        
        data = self.cleaned_data
        nom = data['nom']
        
        return addData.addGroupe(nom)
class AjouterCour(forms.Form):
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    isExam = forms.BooleanField(required=False, label="C'est un exam ?")
    def save(self):
        data = self.cleaned_data
        nom = data['nom']
        isExam = data['isExam']
        addData.addCour(nom, isExam)
class AjouterAnnee(forms.Form):
    annee = forms.IntegerField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Année', 'class':'form-control input-perso'}))
    def save(self):
        data = self.cleaned_data
        annee = data['annee']
        addData.newYear(annee)
class AjouterSalle(forms.Form):
    nom = forms.CharField(required=True, max_length=30, label="", widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    capacite = forms.IntegerField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Capacite', 'class':'form-control input-perso'}))
    type = forms.ChoiceField(label="", choices=SALLES, initial=INCONNU_STATUT_SALLE)
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
        addData.addUV(nom)
class AjouterModule(forms.Form):
    nom = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class':'form-control input-perso'}))
    uv = forms.ModelChoiceField(required=True, queryset=UV.objects.all(), label="UV")
    
    def save(self):
        data = self.cleaned_data
        nom = data['nom']
        uv = data['uv']
        addData.addModule(nom, uv)
