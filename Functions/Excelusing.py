'''
Created on 23 févr. 2016

@author: Morgan
'''
from _datetime import datetime, timedelta
from datetime import date
from math import floor
import os
from time import time

import django
import openpyxl

from BDD.models import Modification, Personne, Groupe, TypeCour, UV, Module,\
    Note, Salle, ChampsModifie

def savmod(Modification, wb):
    sheet = wb.get_sheet_by_name('Modification')
    m = sheet.max_row
    i=1
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    sheet.cell(row=i,column=1).value = Modification.datemodif
    sheet.cell(row=i,column=2).value = Modification.id
    sheet.cell(row=i,column=3).value = Modification.typetable
    sheet.cell(row=i,column=4).value = Modification.typemod
    sheet.cell(row=i,column=5).value = Modification.ipmod
    sheet = wb.get_sheet_by_name('ChampsModifie')
    for cm in ChampsModifie.objects.filter(champs=Modification).all():
        m = sheet.max_row
        i=1
        while (sheet.cell(row=i,column=1).value != None and i<m+2):
            i=i+1
        sheet.cell(row=i,column=1).value = Modification.datemodif
        sheet.cell(row=i,column=2).value = cm.id
        sheet.cell(row=i,column=3).value = Modification.id
        sheet.cell(row=i,column=4).value = cm.nomchamp
        sheet.cell(row=i,column=5).value = cm.valchamp
    
def savpers(Personne, sheet):
    m = sheet.max_row
    i=1
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    sheet.cell(row=i,column=1).value = Personne.uploadDate
    sheet.cell(row=i,column=2).value = Personne.id
    sheet.cell(row=i,column=3).value = Personne.user.first_name+' '+Personne.user.last_name
    sheet.cell(row=i,column=4).value = Personne.user.email
    sheet.cell(row=i,column=5).value = Personne.sexe
    sheet.cell(row=i,column=6).value = Personne.adresse
    sheet.cell(row=i,column=7).value = Personne.dateDeNaissance
    sheet.cell(row=i,column=8).value = Personne.lieuDeNaissance
    sheet.cell(row=i,column=9).value = Personne.numeroDeTel
    sheet.cell(row=i,column=10).value = Personne.type
    sheet.cell(row=i,column=11).value = Personne.promotion
    sheet.cell(row=i,column=12).value = Personne.isvisible
   
def savgrp(Groupe, sheet):
    m = sheet.max_row
    i=1
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    pers = ''
    for p in Groupe.personnes.all():
        pers = pers+str(p)+' '
    sheet.cell(row=i,column=1).value = Groupe.uploadDate
    sheet.cell(row=i,column=2).value = Groupe.id
    sheet.cell(row=i,column=3).value = pers
    sheet.cell(row=i,column=4).value = Groupe.nom
    sheet.cell(row=i,column=5).value = Groupe.isvisible
    
def savcour(TypeCour, sheet):
    m = sheet.max_row
    i=1
    prof = ''
    for p in TypeCour.profs.all():
        prof = prof+str(p)+' '
    grp = ''
    for g in TypeCour.groupe.all():
        grp = grp+str(g)+' '
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    sheet.cell(row=i,column=1).value = TypeCour.uploadDate
    sheet.cell(row=i,column=2).value = TypeCour.id
    sheet.cell(row=i,column=3).value = TypeCour.nom
    sheet.cell(row=i,column=4).value = prof
    sheet.cell(row=i,column=5).value = grp
    sheet.cell(row=i,column=6).value = TypeCour.isExam
    sheet.cell(row=i,column=7).value = TypeCour.isvisible
    
def savuv(UV, sheet):
    m = sheet.max_row
    i=1
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    sheet.cell(row=i,column=1).value = UV.uploadDate
    sheet.cell(row=i,column=2).value = UV.id
    sheet.cell(row=i,column=3).value = UV.nom

def savmodu(Module, sheet):
    m = sheet.max_row
    i=1
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    sheet.cell(row=i,column=1).value = Module.uploadDate
    sheet.cell(row=i,column=2).value = Module.id
    sheet.cell(row=i,column=3).value = Module.nom
    sheet.cell(row=i,column=4).value = Module.uv.nom
    sheet.cell(row=i,column=5).value = Module.isvisible
    
def savnot(Note, sheet):
    m = sheet.max_row
    i=1
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    sheet.cell(row=i,column=1).value = Note.uploadDate
    sheet.cell(row=i,column=2).value = Note.id
    sheet.cell(row=i,column=3).value = Note.note
    sheet.cell(row=i,column=4).value = Note.personne.user.first_name+' '+Note.personne.user.last_name
    sheet.cell(row=i,column=5).value = Note.module.nom
    sheet.cell(row=i,column=6).value = Note.isvisible
    
def savsal(Salle, sheet):
    m = sheet.max_row
    i=1
    while (sheet.cell(row=i,column=1).value != None and i<m+2):
        i=i+1
    sheet.cell(row=i,column=1).value = Salle.uploadDate
    sheet.cell(row=i,column=2).value = Salle.id
    sheet.cell(row=i,column=3).value = Salle.nom
    sheet.cell(row=i,column=4).value = Salle.capacite
    sheet.cell(row=i,column=5).value = Salle.type
    sheet.cell(row=i,column=6).value = Salle.isvisible

def clearall(dat):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'sauvegarde.xlsx')
    file_path2 = os.path.join(module_dir, 'tempo.xlsx')
    wb = openpyxl.load_workbook(file_path)
    typ=datetime.now
    for p in wb.get_sheet_names():
        sheet = wb.get_sheet_by_name(p)
        mc = sheet.max_column
        mr = sheet.max_row
        for i in range (2,mr+1):
            if (isinstance(sheet.cell(row=i,column=1).value,float)):
                typ=convfdat(sheet.cell(row=i,column=1).value)
            else:
                typ=sheet.cell(row=i,column=1).value
            if (typ!=None and typ < dat):
                for j in range (1,mc+1):
                    sheet.cell(row=i,column=j).value = None
    wb.save(file_path2)
    wb2 = openpyxl.load_workbook(file_path2)
    wb2.save(file_path)
    print('all deleted')
    
def clearmod(dat):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'sauvegarde.xlsx')
    file_path2 = os.path.join(module_dir, 'tempo.xlsx')
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.get_sheet_by_name('Modification')
    mc = sheet.max_column
    mr = sheet.max_row
    for i in range (2,mr+1):
        if (isinstance(sheet.cell(row=i,column=1).value,float)):
            typ=convfdat(sheet.cell(row=i,column=1).value)
        else:
            typ=sheet.cell(row=i,column=1).value
        if (typ!=None and typ < dat):
            for j in range (1,mc+1):
                sheet.cell(row=i,column=j).value = None
    wb.save(file_path2)
    wb2 = openpyxl.load_workbook(file_path2)
    wb2.save(file_path)
    print('mod deleted')

def convfdat(a):
    exord = datetime.toordinal(date(1900,1,1))-2
    d = datetime.fromordinal(floor(a)+exord)
    sec=round(((a-floor(a))*10**9)/11574)
    d4=d+timedelta(seconds=sec)
    return(d4)

def saveall():
    django.setup()
    t=time()
    clearall(datetime.now())
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'sauvegarde.xlsx')
    file_path2 = os.path.join(module_dir, 'tempo.xlsx')
    wb = openpyxl.load_workbook(file_path)
    svallpers(wb)
    svallgrp(wb)
    svallcour(wb)
    svalluv(wb)
    svallmodu(wb)
    svallnot(wb)
    svallsal(wb)
    svallmod(wb)
    wb.save(file_path2)
    wb2 = openpyxl.load_workbook(file_path2)
    wb2.save(file_path)
    t=time()-t
    print('done in', t, 'sec')
    
def svallpers(wb):
    sheet = wb.get_sheet_by_name('Personne')
    for p in Personne.objects.all():
        savpers(p, sheet)
         
def svallgrp(wb):
    sheet = wb.get_sheet_by_name('Groupe')
    for g in Groupe.objects.all():
        savgrp(g, sheet)
        
def svallcour(wb):
    sheet = wb.get_sheet_by_name('TypeCour')
    for c in TypeCour.objects.all():
        savcour(c, sheet)

def svalluv(wb):
    sheet = wb.get_sheet_by_name('UV')
    for u in UV.objects.all():
        savuv(u, sheet)
        
def svallmodu(wb):
    sheet = wb.get_sheet_by_name('Module')
    for m in Module.objects.all():
        savmodu(m, sheet)
        
def svallnot(wb):
    sheet = wb.get_sheet_by_name('Note')
    for n in Note.objects.all():
        savnot(n, sheet)
        
def svallsal(wb):
    sheet = wb.get_sheet_by_name('Salle')
    for s in Salle.objects.all():
        savsal(s, sheet)
        
def svallmod(wb):
    for m in Modification.objects.all():
        savmod(m, wb)

d = datetime.now()- timedelta(seconds=3660)
saveall()