# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import Departamento,Setor,Cargo,Vinculo,ProvDesc
import zipfile
import re
import PyPDF2 as p2



def searchDepartamento(id_municipio,chave,tipo):
    if tipo=='nome':
        obj=Departamento.objects.filter(id_municipio=id_municipio).filter(departamento=chave).first()
    else:
        obj=Departamento.objects.filter(id_municipio=id_municipio).filter(codigo=chave).first()

    if obj is None:
        id_departamento=0
    else:
        id_departamento=obj.id_departamento
    return id_departamento

def searchSetor(id_municipio,chave,tipo):
    if tipo=='nome':
        obj=Setor.objects.filter(id_municipio=id_municipio).filter(setor=chave).first()
    else:
        obj=Setor.objects.filter(id_municipio=id_municipio).filter(codigo=chave).first()
    if obj is None:
        id_setor=0
    else:
        id_setor=obj.id_setor
    return id_setor



'''
def searchCargo(id_municipio,nome_do_cargo,operacao):
    obj=Cargo.objects.filter(id_municipio=id_municipio).filter(cargo=nome_do_cargo).first()
    if obj is None:
        if operacao=='incluir':
            Cargo.objects.create(id_municipio=id_municipio,cargo=nome_do_cargo)
            obj=Cargo.objects.filter(id_municipio=id_municipio,cargo=nome_do_cargo).first()
            id_cargo=obj.id_cargo
        else:
            id_cargo=0
    else:
        id_cargo=obj.id_cargo
    return id_cargo

'''

def searchVinculo(id_municipio,nome_do_vinculo,operacao):
    obj=Vinculo.objects.filter(id_municipio=id_municipio).filter(vinculo=nome_do_vinculo).first()
    if obj is None:
        if operacao=='incluir':
            Vinculo.objects.create(id_municipio=id_municipio,vinculo=nome_do_vinculo)
            obj=Vinculo.objects.filter(id_municipio=id_municipio,vinculo=nome_do_vinculo).first()
            id_vinculo=obj.id_vinculo
        else:
            id_vinculo=0
    else:
        id_vinculo=obj.id_vinculo
    return id_vinculo

def searchProvDesc(id_municipio,tipo,codigo,descricao,incluir):
    obj=ProvDesc.objects.filter(id_municipio=id_municipio).filter(codigo=codigo).first()
    if obj is None:
        if incluir:
            ProvDesc.objects.create(id_municipio=id_municipio,tipo=tipo,codigo=codigo,descricao=descricao)
            obj=ProvDesc.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
            id_provdesc=obj.id_provdesc
        else:
            id_provdesc=0
    else:
        id_provdesc=obj.id_provdesc
    return id_provdesc


def mesPorExtenso(mes,modelo):

    lista_mes=['','JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    if modelo==1:
        return lista_mes[int(mes)]
    elif modelo==2:
        return (lista_mes[int(mes)])[0:3]


'''
def gravarFuncionario_local(codigo,nome,id_dep,id_set,id_cargo,id_vinculo,data,carga_horaria):
    

    cursor = connection.cursor()

    cursor.execute("INSERT INTO tab_funcionario (codigo,nome,id_dep,id_setor,id_cargo,id_vinculo) values (%s,%s,%s,%s,%s,%s)", [codigo,nome,id_dep,id_set,id_cargo,id_vinculo])

    cursor.close()
    del cursor
    connection.close()
'''


def gravarFuncionario(id_municipio,codigo,nome,id_dep,id_set,id_cargo,id_vinculo,data_admissao,carga_horaria):
    if data_admissao=='':
        data_admissao=None

    obj = Funcionario.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
    if obj is None:
        Funcionario.objects.create(
            id_departamento = id_dep,
            id_setor = id_set,
            id_cargo = id_cargo,
            id_vinculo = id_vinculo,
            id_municipio = id_municipio,
            nome = nome,
            codigo = codigo,
            data_admissao=data_admissao,
            carga_horaria=carga_horaria
            )

def proventosFuncionario(id_municipio,anomes,id_funcionario):
    lista=[]
    objs = ProvDesc.objects.filter(id_municipio=id_municipio,tipo='VANTAGEM').order_by('ordenacao1')
    for obj in objs:
        id_obj=obj.id_provdesc
        obj_f=Folha.objects.filter(id_municipio=id_municipio,anomes=anomes,id_funcionario=id_funcionario,id_provento=id_obj).first()
        if obj_f is not None:
            valor=obj_f.valor
        else:
            valor=0
        lista.append(str(valor))
    return lista


def cabecalhoFolha(id_municipio):
    lista=[]
    lista.append('Secretaria')
    lista.append('Lotacao')
    lista.append('Codigo')
    lista.append('Nome')
    lista.append('Funcao')
    lista.append('Vinculo')
    lista.append('Dias')
    objs=ProvDesc.objects.filter(id_municipio=id_municipio,tipo='VANTAGEM').order_by('ordenacao1')
    for obj in objs:
        lista.append(obj.descricao)
    lista.append('Soma')
    return lista


def gravarProventos(file_zip,id_municipio):

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        contador=0
        for filename in zip.namelist():
            file = zip.open(filename)

            pdf_reader = p2.PdfFileReader(file)

            n = pdf_reader.numPages
            for i in range(n-1,n):
                page = pdf_reader.getPage(i)
                page_content = (page.extractText())
                print (page_content)



def modelos(string_id_municipio):
    modelos_lista = [('86', 2), ('76', 1)]
    modelos = dict(modelos_lista)    
    return modelos[string_id_municipio]


def strings_pesquisa(string_id_municipio):
    modelos_lista = [
    ('86', 'PREFEITURA MUNICIPAL DE CARIDADE'), 
    ('76', 'PREFEITURA MUNICIPAL DE INDEPENDENCIA')]
    modelos = dict(modelos_lista)    
    return modelos[string_id_municipio]
