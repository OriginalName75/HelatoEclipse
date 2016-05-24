# -*- coding: utf-8 -*-
from Functions.addData import *
from Functions.modiData import *
from Functions.delete import *
from BDD.models import *
import ply.lex as lx
import ply.yacc as yacc

global iddddddd
global listeNom
listeNom=[]
global listePrenom
listePrenom=[]
global glob_str
glob_str=""
global dic_fal_modifier_module
dic_fal_modifier_module={'nom':None,'uv':None,'groupe':None}
dic_condi_modifier_personne={}
dic_but_modifier_personne={}
dic_temp_modifier_personne={}

reserved={'ajouter':'AJOUTER',
          'personne':'PERSONNE',
          'groupe':'GROUPE',
          'supprimer':'SUPPRIMER',
          'afficher':'AFFICHER',
          'modifier':'MODIFIER',
          'prenom':'PRENOM',
          'nom':'NOM',
          'equals':'EQUALS',
          'et':'ET',
          'par':'PAR',
          'numero':'NUMERO',
          'dateN':'DATENAIS',
          'sexe':'SEXE',
          'sex': 'SEX',
          'num':'NUM',
          'mail':'MAIL',
          'mailxp':'MAILXP',
          'lieu_naissance':'LIEUNAIS',
          'adresse':'ADRS',
          'Text':'TEXT',
          'type':'TYPE',
          'promotion':'PROMOTION',
          'promoxp':'PROMOXP',
          'mdp':'MDPASS',
          'login':'LOGIN',
          'id':'ID',
          'float':'FLOAT',
          'nouveau':'NOUVEAU',
          'uv':'UV',
          'module':'MODULE',
          'help':'HELP'
          }

tokens=['DATE']+list(reserved.values())
print(tokens)


# Cette partie consiste a definir les tokens et leurs expressions regulieres
# Cette partie intervient dans l'analyse lexicale

t_ignore = ' \t\x0c'
def t_TEXT(t):
    r'\'.+?\''
    t.type = reserved.get(t.value,"TEXT")
    return t

def t_PROMOXP(t):
    r'20[0-9][0-9]'
    t.type = reserved.get(t.value,"PROMOXP")
    return t

def t_DATENAIS(t):
    r'date_naissance'
    return t

def t_SEX(t):
    r'homme|femme'
    return t

def t_DATE(t):
    r'[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]'
    t.type = reserved.get(t.value,"DATE")
    return t

def t_FLOAT(t):
    r'[1-9]\.[1-9]'
    t.type = reserved.get(t.value,"FLOAT")
    return t

def t_NUM(t):
    r'[0-9]+|\+[0-9]+'
    t.type = reserved.get(t.value,"NUM")
    return t
def t_MAILXP(t):
    r'[a-zA-Z\._-]+@[a-zA-Z\._-]+(\.[a-zA-Z]+)+'
    t.type = reserved.get(t.value,"MAILXP")
    return t
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_\d]*'
    t.type= reserved.get(t.value,"ID")
    return t

def t_EQUALS(t):
    r'\='
    t.type = reserved.get(t.value,"EQUALS")
    return t

def t_ADRS(t):
    r'adresse'
    return t
def t_NOM(t):
    r'nom'
    return t
def t_MODIFIER(t):
    r'modifier'
    return t
def t_ET(t):
    r'et'
    return t
def t_AJOUTER(t):
    r'ajouter'
    return t
def t_PAR(t):
    r'par'
    return t
def t_PERSONNE(t):
    r'personne'
    return t
def t_GROUPE(t):
    r'groupe'
    return t
def t_SUPPRIMER(t):
    r'supprimer'
    return t
def t_AFFICHER(t):
    r'afficher'
    return t
def t_HELP(t):
    r'help'
    return t
def t_PRENOM(t):
    r'prenom'
    return t

def t_LOGIN(t):
    r'login'
    return t
def t_MDPASS(t):
    r'mdp'
    return t
def t_PROMOTION(t):
    r'promotion'
    return t
def t_TYPE(t):
    r'type'
    return t
def t_LIEUNAIS(t):
    r'lieu_naissance'
    return t
def t_NUMERO(t):
    r'numero'
    return t
def t_MAIL(t):
    r'mail'
    return t
def t_SEXE(t):
    r'sexe'
    return t
t_MODULE=r'module'
t_UV=r'uv'
t_NOUVEAU=r'nouveau'


def t_comment(t):
    r' /\*(.|\n)*?\*/'
    t.lineno += t.value.count('\n')

def t_error(t):
    glob_str="lolololo"
    print ("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



lexer = lx.lex()


# data = '''
# ajouter une personne ZIANE Mahrez
# afficher la personne ZIANE Mahrez
# '''
#
# # Give the lexer some input
data="'math info 3'"
lexer.input(data)


# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

# def p_expression_operations(p):
#     '''expression : operation element personne
#     operation : AJOUTER
#     | SUPPRIMER
#     | AFFICHER
#     element : UN GROUPE
#     | UNE PERSONNE
#     personne : IDNOM prenom
#     prenom : prenom
#     | IDPRENOM'''
#
#     print(len(p))
#     for i in range(len(p)):
#         print (p[i])


#   Cette partie definit la grammaire du langage
#   Le parseur utilise une analyse ascendante de type LALR



def p_expression_supprimer(p):
    'expression : SUPPRIMER PERSONNE NOM EQUALS noms facul2 '
    print('suppression de la personne : \n nom :')
    print(set(listeNom))

global promotion_aff,sexe_aff,login_aff,numeroDeTel_aff,email_aff,bool_aff,prenom_aff,nom_aff
bool_aff=False
promotion_aff=None
sexe_aff=None
numeroDeTel_aff=None
email_aff=None
prenom_aff=None
nom_aff=None


def p_expression_afficher(p):
    'expression : AFFICHER PERSONNE faculaff'

    global promotion_aff,sexe_aff,login_aff,numeroDeTel_aff,email_aff,bool_aff,prenom_aff,nom_aff,glob_str

    if bool_aff==False:

        personnes = Personne.objects.all()
        glob_str='Liste des personnes : [ '
        for i in range(len(personnes)):
            glob_str+=str(personnes[i])+' , '

        glob_str+=' ] '

    else:
        print(Personne.objects.all())
        personnes=Personne.objects.all()
        print(nom_aff)
        if(promotion_aff!=None):
            personnes=set(personnes).intersection(Personne.objects.filter(promotion=int(promotion_aff)))
        if(sexe_aff!=None):
            if(sexe_aff!=None):
                if sexe_aff=='homme':
                    temp=1
                else:
                    temp=2
                personnes=set(personnes).intersection(Personne.objects.filter(sexe=temp))
        if(numeroDeTel_aff!=None):
            personnes=set(personnes).intersection(Personne.objects.filter(numerDeTel=numeroDeTel_aff))
        if(nom_aff!=None):
            personnes=set(personnes).intersection(Personne.objects.filter(user__last_name=nom_aff))
        if(prenom_aff!=None):
            personnes=set(personnes).intersection(Personne.objects.filter(user__first_name=prenom_aff))
        personnes=list(personnes)

        glob_str='Liste des personnes filtrees : [ '
        for i in range(len(personnes)):
            glob_str+=str(personnes[i])+' , '

        glob_str+=' ] '
        personnes=[]
    pass

def p_facultatif_affichage(p):

    '''faculaff : sexualityaff faculaff
             | promotionaff faculaff
             | loginaff faculaff
             | mailaff faculaff
             | numeroaff faculaff
             | nomaff faculaff
             | prenomaff faculaff
             |
             '''
    pass

def p_expression_facultative_aff(p):
    'sexualityaff : SEXE EQUALS SEX'
    global sexe_aff,bool_aff
    bool_aff=True
    sexe_aff=p[3]
    pass

def p_expression_facultative_aff2(p):
    'promotionaff : PROMOTION EQUALS PROMOXP'
    global promotion_aff,bool_aff
    bool_aff=True
    promotion_aff=p[3]
    pass

def p_expression_facultative_aff3(p):
    'loginaff : LOGIN EQUALS ID'

    global login_aff,bool_aff
    bool_aff=True
    login_aff=p[3]
    pass

def p_expression_facultative_aff4(p):
    'mailaff : MAIL EQUALS MAILXP'

    global email_aff,bool_aff
    bool_aff=True
    email_aff=p[3]
    pass

def p_expression_facultative_aff5(p):
    'numeroaff : NUMERO EQUALS NUM'
    global numeroDeTel_aff,bool_aff
    bool_aff=True
    numeroDeTel_aff=p[3]
    pass


def p_expression_facultative_aff6(p):
    'nomaff : NOM EQUALS ID'
    global nom_aff,bool_aff
    bool_aff=True
    nom_aff=p[3]
    pass

def p_expression__facultative_aff7(p):
    'prenomaff : PRENOM EQUALS ID'
    global prenom_aff,bool_aff
    bool_aff=True
    prenom_aff=p[3]
    pass


def p_expression_afficher_groupe(p):
    '''expression : AFFICHER GROUPE'''
    global glob_str
    glob_str='Liste des groupes : [ '
    groupes = Groupe.objects.filter(isvisible=True)
    for i in range(len(groupes)):
        glob_str+=str(groupes[i])+' , '

    glob_str+=' ] '

    pass


def p_expression_afficher_uv(p):
    'expression : AFFICHER UV'
    global glob_str
    glob_str='Liste des UVs : [ '
    uvs = UV.objects.filter(isvisible=True)
    for i in range(len(uvs)):
        glob_str+=str(uvs[i].nom)+' , '

    glob_str+=' ] '

    pass

def p_expression_afficher_toutemodule(p):
    'expression : AFFICHER MODULE'
    global glob_str
    glob_str='Liste des modules : [ '
    modules = Module.objects.filter(isvisible=True)
    for i in range(len(modules)):
        glob_str+=str(modules[i])+' , '

    glob_str+=' ] '

    pass

global uvActive

def p_expression_afficher_module(p):
    '''expression : AFFICHER MODULE facul_uv'''
    global glob_str, uvActive
    if uvActive== 'all':

        glob_str='Liste des modules : [ '
        modules = Module.objects.filter(isvisible=True)
        for i in range(len(modules)):
            glob_str+=str(modules[i])+' , '

        glob_str+=' ] '
    else:
        glob_str='Liste des modules : [ '
        uv_temp=UV.objects.filter(nom=uvActive)
        modules = Module.objects.filter(theuv=uv_temp)
        for i in range(len(modules)):
            glob_str+=str(modules[i].nom)+' , '

        glob_str+=' ] '
        uvActive=None
    pass

def p_expression_facul_uv(p):
    '''facul_uv : UV EQUALS TEXT'''
    global uvActive
    uvActive=p[3][1:-1]
    pass


global adresse, promotion,dateDeNaissance,lieuDeNaissance,numeroDeTel,email
adresse=None
promotion=None
dateDeNaissance=None
lieuDeNaissance=None
numeroDeTel=None
email=None

def p_expression_ajouter(p):
    'expression : AJOUTER PERSONNE NOM EQUALS noms PRENOM EQUALS prenoms LOGIN EQUALS ID MDPASS EQUALS TEXT SEXE EQUALS SEX TYPE EQUALS ID facul_aj'
#    print(set(listeNom))
#    print(set(listePrenom))
    global glob_str
    global userID
    global listeNom
    global listePrenom
    global adresse,promotion,dateDeNaissance,lieuDeNaissance,numeroDeTel,email


    p5=listeNom[0]
    p8=listePrenom[0]
    if p[17]=='homme':
        p17=1
    else:
        p17=2

    if p[20]=='prof':
        p20=0
    elif p[20]=='eleve':
        p20=1
    elif p[20]=='administration':
        p20=2
    elif p[20]=='administrateur':
        p20=3
    listeNom=set(listeNom)
    listePrenom=set(listePrenom)
    for i in range(1,len(listeNom)):p5=p5+" "+listeNom[i]
    for i in range(1,len(listePrenom)):p8=p8+" "+listePrenom[i]
    if (p5!=None and p5!="") and (p8!=None and p8!=""):
        addPersonne(userID,p5,p8,p[11],p[14][1:-1],p17,p20,adresse ,promotion, dateDeNaissance, lieuDeNaissance, numeroDeTel, email)
        glob_str="<font color='green'>Vous avez ajoute la personne "+p5 +" "+p8+"</font>"
    listeNom=[]
    listePrenom=[]

def p_facultatif_aj(p):

    '''facul_aj : date_naiss_aj facul_aj
             | sexuality_aj facul_aj
             | lieu_nais_aj facul_aj
             | adresses_aj facul_aj
             | type_aj facul_aj
             | promotion_aj facul_aj
             | login_aj facul_aj
             | mail_aj facul_aj
             | mdp_aj facul_aj
             | numero_aj facul_aj
             |
             '''
    pass

from datetime import datetime
def p_expression_facultative_aj1(p):
    'date_naiss_aj : DATENAIS EQUALS DATE'
    global dateDeNaissance
    print("la date de naissance : \n")
    dateDeNaissance = datetime.strptime(p[3], '%d/%m/%Y')
    print(p[3])

def p_expression_facultative_aj2(p):
    'sexuality_aj : SEXE EQUALS SEX'

    print('sexe de la personne :')
    print(p[3])
    pass

def p_expression_facultative_aj4(p):
    'adresses_aj : ADRS EQUALS TEXT'
    global adresse
    print("l'adresse : ")
    adresse=p[3][1:-1]
    print(p[3])


def p_expression_facultative_aj3(p):
    'lieu_nais_aj : LIEUNAIS EQUALS TEXT'
    global lieuDeNaissance
    print("Lieu de naissance : ")
    lieuDeNaissance=p[3][1:-1]
    print(p[3])

def p_expression_facultative_aj5(p):
    'type_aj : TYPE EQUALS NUM'
    pass

def p_expression_facultative_aj6(p):
    'promotion_aj : PROMOTION EQUALS PROMOXP'
    global promotion
    print('la promotion : ')
    promotion=int(p[3])
    print(p[3])
    pass

def p_expression_facultative_aj7(p):
    'mdp_aj : MDPASS EQUALS TEXT'
    print('le mot de passe :')
    print(p[3])
    pass

def p_expression_facultative_aj8(p):
    'numero_aj : NUMERO EQUALS NUM'
    global numeroDeTel
    print('le numero de telephone :')
    numeroDeTel=p[3]
    print(p[3])
    pass

def p_expression_facultative_aj9(p):
    'mail_aj : MAIL EQUALS MAILXP'
    global email
    print("l'adresse mail : ")
    email=p[3]
    print(p[3])
    pass

def p_expression_facultative_aj10(p):
    'login_aj : LOGIN EQUALS ID'
    print('login de la personne :')
    print(p[3])
    pass

def p_expression_nom(p):
    '''noms : ID
    | ID noms
    '''

    listeNom.append(p[1])



def p_expression_prenoms(p):
    ''' prenoms : ID
    | ID prenoms
    '''

    listePrenom.append(p[1])


def p_expression_modifier(p):
    '''expression : MODIFIER PERSONNE  condition_modifier_personne NOUVEAU but_modifier_personne'''
    global glob_str
    global iddddddd
    global dic_condi_modifier_personne
    global dic_but_modifier_personne
    global dic_temp_modifier_personne
    print('dic_condi_modifier_personne=',dic_condi_modifier_personne)
    personnes=Personne.objects.filter(**dic_condi_modifier_personne)
    nombre=len(personnes)
    if (1<=nombre<=500):
        for personne in personnes:
            print('dic_but_modifier_personne=',dic_but_modifier_personne)
            modPersonne(iddddddd,personne.id,**dic_but_modifier_personne)
            glob_str=" Modification finie: "+str(nombre)+" record"
    elif (nombre==0):
        glob_str="<font color='red'>Cette personne n'existe pas.</font>"
    else:
        glob_str="<font color='red'>Modification échouée : trop de record.</font>"
    dic_condi_modifier_personne.clear()
    dic_but_modifier_personne.clear()

def p_condition_expression_modifier(p):
    '''condition_modifier_personne : facul3'''
    global dic_condi_modifier_personne
    global dic_temp_modifier_personne
    dic_condi_modifier_personne=dic_temp_modifier_personne.copy()
    dic_temp_modifier_personne.clear()
    pass

def p_but_expression_modifier(p):
    '''but_modifier_personne : facul3'''
    global dic_but_modifier_personne
    global dic_temp_modifier_personne
    dic_but_modifier_personne=dic_temp_modifier_personne.copy()
    dic_but_modifier_personne['nom']=dic_but_modifier_personne.pop('user__last_name','')
    dic_but_modifier_personne['prenom']=dic_but_modifier_personne.pop('user__first_name','')
    dic_temp_modifier_personne.clear()
    pass

def p_expression_facul3(p):
    '''facul3 : NOM EQUALS noms facul2
              | facul2 '''
    global listeNom
    global dic_temp_modifier_personne
    if (len(listeNom)>0):
        temp_nom=listeNom[0]
        for i in range(1,len(listeNom)):temp_nom=temp_nom+" "+listeNom[i]
        dic_temp_modifier_personne['user__last_name']=temp_nom
        listeNom=[]
        print('nom=',temp_nom)

def p_expression_facul2(p):
    '''facul2 : PRENOM EQUALS prenoms facul
              | facul'''
    global listePrenom
    global dic_temp_modifier_personne
    if (len(listePrenom)>0):
        temp_prenom=listePrenom[0]
        for i in range(1,len(listePrenom)):temp_prenom=temp_prenom+" "+listePrenom[i]
        dic_temp_modifier_personne['user__first_name']=temp_prenom
        listePrenom=[]
        print('prenom=',temp_prenom)

def p_facultatif(p):

    '''facul : date_naiss facul
             | sexuality facul
             | lieu_nais facul
             | adresses facul
             | type facul
             | promotion facul
             | login facul
             | mail facul
             | mdp facul
             | numero facul
             |
             '''
    pass



def p_expression_facultative1(p):
    'date_naiss : DATENAIS EQUALS DATE'
    global dic_temp_modifier_personne
    print("la date de naissance : \n")
    print(p[3])
    dic_temp_modifier_personne['dateDeNaissance']=p[3]

def p_expression_facultative2(p):
    'sexuality : SEXE EQUALS SEX'
    print('sexe de la personne :')
    print(p[3])
    global dic_temp_modifier_personne
    if p[3]=='homme':
        dic_temp_modifier_personne['sexe']=0
    else:
        dic_temp_modifier_personne['sexe']=1

def p_expression_facultative4(p):
    'adresses : ADRS EQUALS TEXT'
    global dic_temp_modifier_personne
    print("l'adresse : ")
    print(p[3])
    dic_temp_modifier_personne['adresse']=p[3][1:-1]


def p_expression_facultative3(p):
    'lieu_nais : LIEUNAIS EQUALS TEXT'
    print("Lieu de naissance : ")
    print(p[3])
    global dic_temp_modifier_personne
    dic_temp_modifier_personne['lieuDeNaissance']=p[3][1:-1]

def p_expression_facultative5(p):
    'type : TYPE EQUALS NUM'
    global dic_temp_modifier_personne
    dic_temp_modifier_personne['typeP']=int(p[3])
    pass

def p_expression_facultative6(p):
    'promotion : PROMOTION EQUALS PROMOXP'
    print('la promotion : ')
    print(p[3])
    global dic_temp_modifier_personne
    dic_temp_modifier_personne['promotion']=int(p[3])
    pass

def p_expression_facultative7(p):
    'mdp : MDPASS EQUALS TEXT'
    print('le mot de passe :')
    print(p[3])
    global dic_temp_modifier_personne
    dic_temp_modifier_personne['mdp']=p[3][1:-1]
    pass

def p_expression_facultative8(p):
    'numero : NUMERO EQUALS NUM'
    print('le numero de telephone :')
    print(p[3])
    global dic_temp_modifier_personne
    dic_temp_modifier_personne['numeroDeTel']=p[3]
    pass

def p_expression_facultative9(p):
    'mail : MAIL EQUALS MAILXP'
    print("l'adresse mail : ")
    print(p[3])
    global dic_temp_modifier_personne
    #dic_temp_modifier_personne['user__email']=p[3]
    pass

def p_expression_facultative10(p):
    'login : LOGIN EQUALS ID'
    print('login de la personne :')
    print(p[3])
    global dic_temp_modifier_personne
    dic_temp_modifier_personne['login']=p[3]
    pass





def p_expression_ajouter_groupe(p):
    '''expression : AJOUTER GROUPE TEXT'''
    global glob_str
    global iddddddd
    if p[3]!=None and p[3]!="":
        addGroupe(iddddddd,p[3][1:-1])
        glob_str="<font color='green'>Vous avez ajouté le groupe "+ p[3]+"</font>"
    else:
        glob_str="<font color='red'>Echouer de ajouter ce groupe!</font>"

def p_expression_modifier_groupe(p):
    '''expression : MODIFIER GROUPE NOM EQUALS TEXT NOUVEAU EQUALS TEXT'''
    global glob_str
    global iddddddd
    groupes=Groupe.objects.filter(nom=p[5][1:-1])
    if len(groupes)==1:
        idGroupe=groupes[0].id
        modGroupe(idGroupe, iddddddd, p[8][1:-1], personnes=None, modules=None)
        glob_str="<font color='green'>Vous avez modifié le groupe "+ p[5] +" avec le nouveau nom "+p[8]+"</font>"
    else:
        glob_str="<font color='red'>Echouer de modifier ce groupe!</font> "+str(len(groupes))


def p_expression_supprimer_groupe(p):
    '''expression : SUPPRIMER GROUPE TEXT'''
    global glob_str
    global iddddddd

    groupes=Groupe.objects.filter(nom=p[3][1:-1])
    glob_str="jules"
    if len(groupes)==1:
        idGroupe=groupes[0].id
        supr_salles(1,idGroupe,iddddddd)
        glob_str="<font color='green'>Vous avez supprimé le groupe "+ p[3]+"</font>"
    else:
        glob_str="<font color='red'>Echouer de supprimer ce groupe!</font> "

def p_expression_ajouter_uv(p):
    '''expression : AJOUTER UV TEXT'''
    global glob_str
    global iddddddd
    if p[3]!=None and p[3]!="":
        addUV(iddddddd,p[3][1:-1])
        glob_str="<font color='green'>Vous avez ajouté l'UV "+ p[3]+ "</font>"
    else:
        glob_str="<font color='red'>Echouer de ajouter cette UV!</font>"

def p_expression_modifier_uv(p):
    '''expression : MODIFIER UV NOM EQUALS TEXT NOUVEAU EQUALS TEXT'''
    global glob_str
    global iddddddd
    uvs=UV.objects.filter(nom=p[5][1:-1])
    if len(uvs)==1:
        idUV=uvs[0].id
        modUV(idUV,iddddddd,p[8][1:-1])
        glob_str="<font color='green'>Vous avez modifié l'UV "+ p[5] +" avec le nouveau nom "+p[8]+"</font>"
    else:
        glob_str="<font color='red'>Echouer de modifier cette UV!</font>"

def p_expression_supprimer_uv(p):
    '''expression : SUPPRIMER UV TEXT'''
    global glob_str
    global iddddddd
    uvs=UV.objects.filter(nom=p[3][1:-1])
    if len(uvs)==1:
        idUV=uvs[0].id
        supr_salles(2,idUV,iddddddd)
        glob_str="<font color='green'>Vous avez supprimé l'UV "+ p[3]+"/font"
    else:
        glob_str="<font color='red'>Echouer de supprimer cette UV!</font>"


def p_expression_ajouter_module(p):
    '''expression : AJOUTER MODULE TEXT UV EQUALS TEXT'''
    global glob_str
    global iddddddd
    nommodule=p[3][1:-1]
    nomuv=p[6][1:-1]
    uvs=UV.objects.filter(nom=nomuv)
    if (nommodule!="") and (nomuv!="") and (len(uvs)==1):
        addModule(iddddddd,nommodule,uvs[0])
        glob_str="<font color='green'>Vous avez ajouté le module "+ p[3] +" dans l'UV" + p[6]+"</font>"
    elif (len(uvs)==0):
        glob_str="<font color='red'>Echouer de ajouter ce module! L'UV n'existe pas.</font>"
    else:
        glob_str="<font color='red'>Echouer de ajouter ce module!</font>"

    '''expression : MODIFIER MODULE TEXT but_modifier_module'''
def p_expression_modifier_module(p):
    global glob_str
    global iddddddd
    global dic_fal_modifier_module
    nommodule=p[3][1:-1]
    nomuv=dic_fal_modifier_module['uv']
    nomgroupe=dic_fal_modifier_module['groupe']
    modules=Module.objects.filter(nom=nommodule)
    uvs=UV.objects.filter(nom=nomuv)
    groupes=Groupe.objects.filter(nom=nomgroupe)

    if (len(modules)==1):
        modModule(modules[0].id, iddddddd, nom=dic_fal_modifier_module['nom'], uv=uvs[0], groupes=groupes)
        glob_str="<font color='green'>Vous avez modifié le module "+ p[3]+"/font"
    elif (len(modules)==0):
        glob_str="<font color='red'>ce module n'existe pas.</font>"
    else:
        glob_str="<font color='red'>Echouer de modifier ce module!</font>"
    dic_fal_modifier_module={'nom':None,'uv':None,'groupe':None}


def p_but_modifier_module(p):
    ''' but_modifier_module : nom_modifier_module but_modifier_module
    | uv_modifier_module but_modifier_module
    | groupe_modifier_module but_modifier_module
    |
    '''
    pass

def p_but_modifier_module_1(p):
    '''nom_modifier_module : NOM EQUALS TEXT'''
    global dic_fal_modifier_module
    dic_fal_modifier_module['nom']=p[3][1:-1]

def p_but_modifier_module_2(p):
    '''uv_modifier_module : UV EQUALS TEXT'''
    global dic_fal_modifier_module
    dic_fal_modifier_module['uv']=p[3][1:-1]

def p_but_modifier_module_3(p):
    '''groupe_modifier_module : GROUPE EQUALS TEXT'''
    global dic_fal_modifier_module
    dic_fal_modifier_module['groupe']=p[3][1:-1]


def p_expression_supprimer_module(p):
    '''expression : SUPPRIMER MODULE TEXT'''
    global glob_str
    global iddddddd
    modules=Module.objects.filter(nom=p[3][1:-1])
    if len(modules)==1:
        idmodule=modules[0].id
        supr_salles(3,idmodule,iddddddd)
        glob_str="<font color='green'>Vous avez supprimé le module "+ p[3]+"</font>"
    else:
        glob_str="<font color='red'>Echouer de supprimer ce module!</font>"

def p_expression_help(p):
    '''expression : HELP'''
    global glob_str
    glob_str="<font color='red'>HELP</font>: Vous pouve choisir les fonctions par:>>><font color='green'>help [afficher,ajouter,modifier,supprimer]</font>"

def p_expression_help_ajouter(p):
    '''expression : HELP AJOUTER'''
    global glob_str
    glob_str="<font color='red'>HELP</font> ajouter: >>><font color='green'>ajouter [personne,groupe,uv,module]</font>"

def p_expression_help_afficher(p):
    '''expression : HELP AFFICHER'''
    global glob_str
    glob_str="<font color='red'>HELP</font> afficher: >>><font color='green'>afficher [personne,groupe,uv,module]</font>"

def p_expression_help_modifier(p):
    '''expression : HELP MODIFIER'''
    global glob_str
    glob_str="<font color='red'>HELP</font> modifier: >>><font color='green'>modifier [personne,groupe,uv,module]</font>"

def p_expression_help_supprimer(p):
    '''expression : HELP SUPPRIMER'''
    global glob_str
    glob_str="<font color='red'>HELP</font> supprimer: >>><font color='green'>supprimer [groupe,uv,module]</font>"

def p_error(t):
    global glob_str

    try:
        glob_str="<font color='red'>Erreur syntaxique</font>"+ str(t.value) +"'"
        print("Erreur syntaxique '"+ str(t.value) +"'")
    except Exception:
        glob_str="<font color='red'>Erreur LEXICALE</font> "
        print("Erreur LEXICALE ")


parser=yacc.yacc()
def use(strr, iid):
    global iddddddd,userID
    iddddddd=iid
    userID=iid
    parser.parse(strr)
    return glob_str
