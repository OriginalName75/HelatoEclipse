# -*- coding: utf-8 -*-
"""
    The ''mod'' module
    ======================
    
    It defines what is on the database
    
    :Exemple:
    
    >> uv=UV() 
    >> uv.nom="nom de l\'uv"
    >> uv.save()
    save an UV in the database
    
    
@author: IWIMBDSL
"""

from django.contrib.auth.models import User
from django.db import models as mod
from django.utils import timezone
from django.utils.datetime_safe import datetime

from BDD.choices import SEXE, TYPE, INCONNU_STATUT, \
    INCONNU_STATUT_TYPE, SALLES, INCONNU_STATUT_SALLE, SEMAINE, LUNDI, TYPENEWS, \
    TYPENEWSG, AJOUT, TYMO, INCONNU_STATUT_MOD



class Modification(mod.Model):
    """
        A modification is a table that stores the modifications applied to an other table.
        
        A Modification has a datemodif, a typetable, a typemod (to represent if the table were added, 
        deleted or just modified) and an ipmod (which stored the id of the modified table)
        
        :example:
        >> from BDD.choices import AJOUT
        >> mod = mod.Modification()
        >> mod.datemodif = timezone.now()
        >> mod.typetable = 'Groupe'
        >> mod.typemod = AJOUT
        >> mod.ipmod = c.id
        >> mod.save()
        save the modification representing the add of a group
    """
    
    datemodif = mod.DateTimeField(default=datetime.now)
    typetable = mod.CharField(max_length=200, null=True)
    typemod = mod.IntegerField(choices=TYMO, default=INCONNU_STATUT_MOD)
    ipmod = mod.IntegerField (null=True)
    
    def __str__ (self):
        return self.datemodif.strftime('%d/%m/%Y %H:%M:%S')

class ChampsModifie(mod.Model):
    """
        A ChampsModifie is a table that stores one of the modifications applied to an other table.
        
        A ChampsModifie has a champs (which links it to the Modification it is associate with),
        a nomchamp (type of the changed field), and a valchamp (value of this field).
        
        :example:
        >> cm1 = mod.ChampsModifie()
        >> cm1.champs = mod
        >> cm1.nomchamp = 'nom'
        >> cm1.valchamp = nomm
        >> cm1.save()
        save the modification representing the change of the name of the table represented by the Modification
        mod from nomm
    """
    
    champs = mod.ForeignKey(Modification)
    nomchamp = mod.CharField(max_length=50)
    valchamp = mod.CharField(max_length=1000, null=True)
    
    def __str__ (self):
        return self.nomchamp

class Personne(mod.Model):
    """
        It defines how a person is stocked in the database.
        
        A person is related to an user (OnetoOne relation)
        (A user has especially a first name, last name, email, login and a password)
        
        A Person has a sex, an address, a promotion, a type (professor/admin/student...), a date of birth,  
        a place of birth, a phone number.
        
        It has also an upload date.
        
        It has also a filter (which defines a person in a unique way), used in forms.
        
        :exemple:
        >> from django.contrib.auth.mod import User
        >> from BDD.choices import HOMME_STATUT, ELEVE_STATUT
        >> user=User(first_name="Jimmy", last_name="Page", username="LedZep", password="123456", email="jimmy@ledzep.com")
        >> user.save()
        >> p = Personne()
        >> p.sexe=HOMME_STATUT
        >> p.type=ELEVE_STATUT
        >> p.user=user
        >> p.save()
        save a person in the database (some files like promotion are optional)
        
    """
    
    sexe = mod.IntegerField(choices=SEXE, default=INCONNU_STATUT)  # true = femme; false = homme
    adresse = mod.CharField(max_length=200, null=True)  # adresse de le personne
    promotion = mod.IntegerField(null=True)  # ex : 2017
    type = mod.IntegerField(choices=TYPE, default=INCONNU_STATUT_TYPE)
    dateDeNaissance = mod.DateField(null=True)  # date
    lieuDeNaissance = mod.CharField(max_length=200, null=True)  # lieu de la naissance
    numeroDeTel = mod.CharField(null=True, max_length=40)  # son 06
    user = mod.OneToOneField(User)  # l'authentification est gérée pas django
    uploadDate = mod.DateTimeField(default=timezone.now())  # date de l'upload
    filter = mod.CharField(max_length=200)  # adresse de le personne
    isvisible = mod.BooleanField(default = True)
    def __str__ (self):
        return self.filter
    def links(self):
        """ Print links in fiche and modifie view
        :param table: it represent which kind of data it is (exemple: a groupe)
        :type table: int 
        
        """
        l = []
        
        l.append(['/watch/6/0', 'Lui ajouter des notes'])
        l.append(['/watch/7/0', 'Lui ajouter des cours'])
    
        return l  
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        l.append(QUIRY('prenom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        l.append(QUIRY('login', "if (VAL.length > 3 && VAL) return true; else return false;"  , 'Ce champ doit avoir au moins 4 caracteres'))
        l.append(QUIRY('numeroDeTel', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'))
        l.append(QUIRY('promotion', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'))
        l.append(QUIRY('mdp', "if (VAL.length > 5 && VAL) return true; else return false;"  , 'Au moins 6 caracteres'))
        l.append(QUIRY('mdp2', "if ((VAL == jQuery('#id_form-'+lolo+'-mdp').val()) && VAL) return true; else return false;"  , 'Les mots de passe sont differents'))
        l.append(QUIRY('mail', "if (VAL.match(/^[^\\W][a-zA-Z0-9\\_\\-\\.]+([a-zA-Z0-9\\_\\-\\.]+)*\\@[a-zA-Z0-9_]+(\\.[a-zA-Z0-9_]+)*\\.[a-zA-Z]{2,4}$/)) return true; else return false;"  , 'Ce n\'est pas un mail valide'))
        l.append(QUIRY('dateDeNaissance', "if (!isValidDate(parseInt(VAL.split('/')[2]), parseInt(VAL.split('/')[0]), parseInt(VAL.split('/')[1]))) return false; else return true;"  , 'Ce n\'est pas une date valide'))
    
        return l
class horaireProf(mod.Model):
    """ 
        Pas encore utilisé
    """
    prof = mod.ForeignKey(Personne)
    jdelaSemaine = mod.IntegerField(choices=SEMAINE, default=LUNDI)
    hminMatin = mod.IntegerField()
    hmaxMatin = mod.IntegerField()
    hminApresMidi = mod.IntegerField()
    hmaxApresMidi = mod.IntegerField()
    isvisible = mod.BooleanField(default = True)
    def __str__ (self):
        return self.get_jdelaSemaine_display() + " : " + str(self.hminMatin) + "/" + str(self.hmaxMatin) + " + " + str(self.hminApresMidi) + "/" + str(self.hmaxApresMidi)
class Groupe(mod.Model):
    """
        It defines how a group is stocked in the database.
        
        A group has a name
         
        A group is related to persons and modules (ManytoMany relation)
    
        It has also an upload date.
        
        :exemples:
        
        >> g = Group()
        >> g.nom="MPSI 1"
        >> g.save()
        save a groupe in the database (some files like promotion are optional and the upload date is made automatically)
        
        >> uv=UV(nom="2.9")
        >> uv.save()
        >> m = Module(nom="connaissance de soi", uv=uv)
        >> m.save()
        >> g = Groupe(nom="CM2")
        >> g.modules.add(m) 
        >> g.save()
        add a module in a group
        
    """
    nom = mod.CharField(max_length=30)  # nom du groupe
    personnes = mod.ManyToManyField(Personne, blank=True)  # un groupe a plusieurs oersonne et une personne a plusieur groupe
    uploadDate = mod.DateTimeField(default=timezone.now())  # date de l'upload
    
    
    modules=mod.ManyToManyField('Module', blank=True)
    
    isvisible = mod.BooleanField(default = True)
    def __str__ (self):
        return self.nom
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        
        return l
class UV(mod.Model):
    """
        It defines how an UV is stocked in the database.
        
        An UV has a name
       
        :exemple:
        
        >> uv=UV(nom="7.5")
        >> uv.save()
        save an UV in the database 
        
    """
    nom = mod.CharField(max_length=30)  # nom de l'UV
    isvisible = mod.BooleanField(default = True)
    uploadDate = mod.DateTimeField(default=timezone.now()) 
    def links(self):
        """ Print links in fiche and modifie view
        :param table: it represent which kind of data it is (exemple: a groupe)
        :type table: int 
        
        """
        l = []
    
        l.append(['/watch/3/0', 'Lui ajouter des modules'])
        return l  
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        
        return l
    def __str__ (self):
        
        return "%s" %(self.nom)
    
    
class Module(mod.Model):
    """
        It defines how a module is stocked in the database.
        
        A module has a name and it is related to an UV (OnetoMany relation)
        
        :exemple:
        
        >> uv=UV(nom="2.9")
        >> uv.save()
        >> m = Module(nom="géopolitique de brest", uv=uv)
        >> m.save()
        save a module in the database 
    """  
    nom = mod.CharField(max_length=30)  # nom du module    
    theuv = mod.ForeignKey(UV)
    isvisible = mod.BooleanField(default = True)
    uploadDate = mod.DateTimeField(default=timezone.now()) 
    def __str__ (self):
        
        return "%s - %s" % (self.nom, self.theuv.nom)
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        l.append(QUIRY('theuv', "if (VAL) return true; else return false;"  , 'Choisissez un uv svp'))
        
        return l
 
class Salle(mod.Model):
    """
        It defines how a classroom is stocked in the database.
        
        A classroom has a name, a capacity, and a type (classroom with comptuer/lab...)
        
        :exemple:
        >> from BDD.choices import INFO_STATUT
        >> s=SALLE(nom="404", capacite=30, type= INFO_STATUT)
        >> s.save()
        save a classroom in the database 
    """
   
    nom = mod.CharField(max_length=30)
    capacite = mod.IntegerField(null=True)
    type = mod.IntegerField(choices=SALLES, default=INCONNU_STATUT_SALLE)
    isvisible = mod.BooleanField(default = True) 
    def __str__ (self):
        return self.nom
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        l.append(QUIRY('capacite', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'))
        
        return l  
class Note(mod.Model):
    """
        It defines how a mark is stocked in the database.
        
        It has a number (the mark), and an upload date.
        
        Tt is related to persons (the persons marked and in an other place professors) 
        and modules (OnetoMany relation)
        
        :exemple:
        
        >> p= Personne.objects.get(id=3) # get a person which his id is equal to 3
        >> m = Module.objects.get(id=2)
        >> prof = Module.objects.get(id=1)
        >> note = Note(note=0, personne=p, module=m, prof=prof)
        >> note.save()
        save a mark in the database 
    """
   
    lanote = mod.IntegerField(default=0, blank=True, null=True)
    personnenote = mod.ForeignKey(Personne)
    themodule = mod.ForeignKey(Module)
    prof= mod.ForeignKey(Personne, related_name="ANoter")
    uploadDate = mod.DateTimeField(default=timezone.now())  # date de l'upload
    isvisible = mod.BooleanField(default = True)
    def ajouterPlusieurs(self):
        """
            See ajouterPlusieurs of mod.Model
        """
        from BDD.forms import chooseGroupe, notes, BaseNoteFormSet
        from Functions.data import ADDMANY
        return ADDMANY(chooseGroupe, notes, BaseNoteFormSet, ["groupes","module"], [Personne,Module],'groupe__in')
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('note', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        l.append(QUIRY('note', "if (!isNaN(VAL)) return true; else return false;"  , 'Ce n\'est pas un nombre'))
        l.append(QUIRY('personne', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        l.append(QUIRY('module', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        
        return l
    def __str__ (self):
        return str(self.lanote)    
class TypeCour(mod.Model):
    """
        It defines a type of lesson.
        
        It has a name and a boolean value which defines if it is an exam or not.
        
        Tt is related to persons (professors) and groups (ManytoMany relations)
        
        :exemple:
        
        >> m = Groupe.objects.get(id=2)
        >> prof = Module.objects.get(id=1)
        >> t = TypeCour(nom="Sport")
        >> t.profs.add(prof)
        >> t.groups.add(groupe)
        >> t.save()
        save a type of lesson in the database 
    """
    nom = mod.CharField(max_length=30)
    profs = mod.ManyToManyField(Personne, blank=True)
    groupe = mod.ManyToManyField(Groupe, blank=True)
    isExam = mod.BooleanField()
    isvisible = mod.BooleanField(default = True)
    uploadDate = mod.DateTimeField(default=timezone.now()) 
    def __str__ (self):
        return self.nom
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('nom', "if (VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        return l
    
class Cour(mod.Model):
    """
        It defines a lesson.
        
        It has a name, an upload date, 2 integers which represent the start and the end of the lesson in weeks,
        2 others for the hours and another for the day.
        
        It is related to a type of lesson (OneToMany relation) and classrooms (ManyToMany relation)
        
        :exemple:
        >> from BDD.choices import MARDI
        >> t = TypeCour.objects.get(id=2)
        >> s = SALLE.objects.get(id=1)
        >> l = Cour(typeCour=t, jour=MARDI, hmin=0, hmax=2, semaineMin=1, semaineMax=2)
        >> l.salles.add(s)
        >> l.save()
        save a lesson in the database 
    """
    
    typeCour = mod.ForeignKey(TypeCour)
    salles = mod.ManyToManyField(Salle, blank=True)
    uploadDate = mod.DateTimeField(default=timezone.now())  # date de l'upload
    semaineMin = mod.IntegerField()
    semaineMax = mod.IntegerField()
    jour = mod.IntegerField(choices=SEMAINE, default=LUNDI)
    hmin = mod.IntegerField()
    hmax = mod.IntegerField()
    isvisible = mod.BooleanField(default = True)
    def __str__ (self):
        return self.typeCour.nom
    def quiery(self):
        from Functions.data import QUIRY
        l=[]
        l.append(QUIRY('jour', "if ((VAL) return true; else return false;"  , 'Ce champ est obligatoire'))
        l.append(QUIRY('semaineMin', "if (VAL && VAL>=0 && VAL<=52) return true; else return false;"  , 'Ce champ est obligatoire et >-1 et <53'))
        l.append(QUIRY('semaineMax', "if (VAL && VAL>=0 && VAL<=52) return true; else return false;"  , 'Ce champ est obligatoire et >-1 et <53'))
        l.append(QUIRY('hmin', "if (VAL && VAL>=0 && VAL<=10) return true; else return false;"  , 'Ce champ est obligatoireet >-1 et <11'))
        l.append(QUIRY('hmax', "if (VAL && VAL>=0 && VAL<=52) return true; else return false;"  , 'Ce champ est obligatoireet >-1 et <11'))
        
      
        return l
class News(mod.Model):
    """
        It defines a news.
        
        It has a text, an upload date and 2 types of news (delete, add... and the kind of object)
        
        It is related to  persons (ManyToMany relation)
        
        :exemple:
        >> from BDD.choices import AJOUT, PERSONNESTATUT
        >> p = Personne.objects.get(id=2)
        >> l = News(txt="Welcome", type=PERSONNESTATUT, typeG=AJOUT)
        >> l.personne.add(p)
        >> l.save()
        save a lesson in the database (the upload date is automatic)
    """
    
    personne=mod.ManyToManyField(Personne)
    txt=mod.CharField(max_length=100)
    type = mod.IntegerField(choices=TYPENEWS, default=INCONNU_STATUT_TYPE)
    typeG= mod.IntegerField(choices=TYPENEWSG, default=AJOUT)
    uploadDate = mod.DateTimeField(default=timezone.now())  # date de l'upload
    isvisible = mod.BooleanField(default = True)
    sens= mod.BooleanField(default = True)
    def __str__ (self):
        return self.txt

    
     
    
    
