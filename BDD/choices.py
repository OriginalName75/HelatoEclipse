'''
Created on 28 oct. 2015

@author: Moran
'''
HOMME_STATUT=1
FEMME_STATUT=2
INCONNU_STATUT=0
INCONNU_STATUT_SALLE=0
INCONNU_STATUT_TYPE=4
PROF_STATUT=0
ELEVE_STATUT=1
ADMINISTRATION_STATUT=2
ADMINISTRATEUR_STATUT=3
CLASSE_STATUT=1
LABO_STATUT=2
INFO_STATUT=3
LUNDI=0
MARDI=1
MECREDI=2
JEUDI=3
VENDREDI=4
SAMEDI=5
DIMANCHE=6
SEMAINEINCONNU=100

CHOICESNB=[]
for i in range(1,20):
    CHOICESNB.append((i,str(i)))

PASVAC=0
SEMI=1
VAC=2
VACANCETYPE=((PASVAC,'Pas de vacance'),(SEMI,'Un peu en vac'),(VAC,'Vacance'))    
SEMAINE = ((LUNDI, 'Lundi'), (MARDI, 'Mardi'), (MECREDI, 'Mecredi'), (JEUDI, 'Jeudi'), (VENDREDI, 'Vendredi'), (SAMEDI, 'Samedi'), (DIMANCHE, 'Dimanche'))
SEMAINEAAVECINCO = ((SEMAINEINCONNU, 'Inconnue'), (LUNDI, 'Lundi'), (MARDI, 'Mardi'), (MECREDI, 'Mecredi'), (JEUDI, 'Jeudi'), (VENDREDI, 'Vendredi'), (SAMEDI, 'Samedi'), (DIMANCHE, 'Dimanche'))

SALLES = ((INCONNU_STATUT_SALLE, 'Type inconnu'), (CLASSE_STATUT, 'Classe'), (LABO_STATUT, 'Labo'), (INFO_STATUT, 'Info'))
SEXE = ((INCONNU_STATUT, 'Sexe Inconnu'), (HOMME_STATUT, 'Homme'), (FEMME_STATUT, 'Femme'))
TYPE = ((INCONNU_STATUT_TYPE, 'Statut Inconnu'), (PROF_STATUT, 'Prof/Chercheur'), (ELEVE_STATUT, 'Eleve'), (ADMINISTRATION_STATUT, 'Administration'), (ADMINISTRATEUR_STATUT, 'Administrateur Du Site'))