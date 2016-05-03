

from Functions.addData import addGroupe
import ply.lex as lx
import ply.yacc as yacc

global iddddddd

global glob_str
glob_str=""

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
          'module':'MODULE'
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
def t_LA(t):
    r'la'
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

# def t_IDNOM(t):
#     r'[A-Z][A-Z]+'
#     t.type = reserved.get(t.value,"IDNOM")
#     return t
# def t_IDPRENOM(t):
#     r'[A-Z][a-z]+'
#     t.type = reserved.get(t.value,"IDPRENOM")
#     return t



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

def p_expression_afficher(p):
    '''expression : AFFICHER PERSONNE
                  | AFFICHER PERSONNE facul3'''
    pass

def p_expression_facul3(p):
    '''facul3 : NOM EQUALS noms facul2
              | facul2 '''
    pass

def p_expression_facul2(p):
    '''facul2 : PRENOM EQUALS prenoms facul
              | facul'''
    try :
        print('prenom : ')
        print(set(listePrenom))
    except Exception:
        pass



def p_expression_ajouter(p):
    'expression : AJOUTER PERSONNE NOM EQUALS noms PRENOM EQUALS prenoms facul'
    print(set(listeNom))
    print(set(listePrenom))
    pass

listeNom=[]
listePrenom=[]
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


def p_condition_modifier_per(p):
    '''condition_modif : attribut EQUALS element
                       | attribut EQUALS element ET condition_modif'''
    pass

def p_attribut_personne(p):
    '''attribut : NOM
                | PRENOM
                | ADRS
                | SEXE
                | PROMOTION
                | MAIL
                | LIEUNAIS
                | NUMERO
                | LOGIN
                | MDPASS
                | DATENAIS
    '''
    pass

def p_element_personne(p):
    '''element : ID
               | TEXT
               | NUM
               | MAILXP
               | DATE
               | PROMOXP
               | SEX

               '''

def p_expression_modifier(p):
    'expression : MODIFIER attribut PERSONNE condition_modif NOUVEAU EQUALS element '
    pass



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
    print("la date de naissance : \n")
    print(p[3])

def p_expression_facultative2(p):
    'sexuality : SEXE EQUALS SEX'
    print('sexe de la personne :')
    print(p[3])
    pass

def p_expression_facultative4(p):
    'adresses : ADRS EQUALS TEXT'
    print("l'adresse : ")
    print(p[3])


def p_expression_facultative3(p):
    'lieu_nais : LIEUNAIS EQUALS TEXT'
    print("Lieu de naissance : ")
    print(p[3])

def p_expression_facultative5(p):
    'type : TYPE EQUALS NUM'
    pass

def p_expression_facultative6(p):
    'promotion : PROMOTION EQUALS PROMOXP'
    print('la promotion : ')
    print(p[3])
    pass

def p_expression_facultative7(p):
    'mdp : MDPASS EQUALS TEXT'
    print('le mot de passe :')
    print(p[3])
    pass

def p_expression_facultative8(p):
    'numero : NUMERO EQUALS NUM'
    print('le numero de telephone :')
    print(p[3])
    pass

def p_expression_facultative9(p):
    'mail : MAIL EQUALS MAILXP'
    print("l'adresse mail : ")
    print(p[3])
    pass

def p_expression_facultative10(p):
    'login : LOGIN EQUALS ID'
    print('login de la personne :')
    print(p[3])
    pass

#Partie de jules

def p_expression_afficher_groupe(p):
    '''expression : AFFICHER GROUPE'''
    pass


def p_expression_afficher_uv(p):
    '''expression : AFFICHER UV'''
    pass

def p_expression_afficher_module(p):
    '''expression : AFFICHER MODULE facul_uv'''
    pass

def p_expression_facul_uv(p):
    '''facul_uv : UV EQUALS TEXT'''
    pass

def p_expression_ajouter_groupe(p):
    '''expression : AJOUTER GROUPE TEXT'''
    global glob_str
    
    global iddddddd
    if p[3]!=None and p[3]!="":
        addGroupe(iddddddd,p[3])
        glob_str="Vous avez ajoute le groupe "+ p[3]

def p_expression_modifier_groupe(p):
    '''expression : MODIFIER GROUPE condition_modifier_groupe NOUVEAU EQUALS TEXT'''
    pass

def p_condition_modifier_groupe(p):
    '''condition_modifier_groupe : NOM EQUALS TEXT '''
    pass

def p_expression_supprimer_groupe(p):
    '''expression : SUPPRIMER GROUPE TEXT'''
    pass

def p_expression_ajouter_uv(p):
    '''expression : AJOUTER UV TEXT NUM EQUALS FLOAT '''
    pass

def p_expression_modifier_uv(p):
    '''expression : MODIFIER UV condition_modifier_uv NOUVEAU EQUALS TEXT'''
    pass

def p_condition_modifier_uv(p):
    ''' condition_modifier_uv : NOM EQUALS TEXT'''
    pass

def p_expression_supprimer_uv(p):
    '''expression : SUPPRIMER UV TEXT'''
    pass


def p_expression_ajouter_module(p):
    '''expression : AJOUTER MODULE TEXT UV EQUALS TEXT'''
    pass

def p_expression_modifier_module(p):
    '''expression : MODIFIER MODULE condition_modifier_module but_modifier_module'''
    pass

def p_condition_modifier_module(p):
    ''' condition_modifier_module : NOM EQUALS TEXT'''
    pass

def p_but_modifier_module(p):
    ''' but_modifier_module : NOUVEAU EQUALS TEXT
    | NOUVEAU EQUALS TEXT UV EQUALS TEXT'''
    pass

def p_expression_supprimer_module(p):
    '''expression : SUPPRIMER MODULE TEXT'''

    pass


def p_error(t):
    global glob_str
  
    try:
        glob_str="Erreur syntaxique '"+ str(t.value) +"'"
        print("Erreur syntaxique '"+ str(t.value) +"'")
    except Exception:
        glob_str="Erreur LEXICALE "
        print("Erreur LEXICALE ")

 
parser=yacc.yacc() 
def use(strr, iid):
    global iddddddd
    iddddddd=iid
    
    parser.parse(strr)
    return glob_str
