# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import Departamento,Setor,Cargo,Vinculo,ProvDesc,LogErro,Funcionario,Funcao,Lotacao,Municipio,FolhaMes,ProventosMes



def gravarLog(codigo,observacao,id_municipio):
	LogErro.objects.create(id_municipio=id_municipio,codigo=codigo,observacao=observacao)


def gravar_departamento(lista_set,id_municipio):

	lista = list(lista_set)

	for id in range(len(lista)):
		cod=lista[id][0:3]
		dep=lista[id][3:]

		obj = Departamento.objects.filter(id_municipio=id_municipio,codigo=cod).first()
		if obj is None:
			Departamento.objects.create(id_municipio=id_municipio,codigo=cod,departamento=dep)


def gravar_setor(lista_set,id_municipio):
	lista = list(lista_set)

	for id in range(len(lista)):
		cod_depto=lista[id][0:3]
		cod_setor=lista[id][3:9]
		departamento=searchDepartamento(id_municipio=id_municipio,codigo=cod_depto)
		if departamento is not None:
			id_departamento=departamento.id_departamento
			setor=lista[id][9:]
			obj = Setor.objects.filter(id_municipio=id_municipio,departamento=departamento,codigo=cod_setor).first()
			if obj is None:	
				Setor.objects.create(id_municipio=id_municipio,departamento=departamento,codigo=cod_setor,setor=setor)


def gravar_funcionario(lista_set,id_municipio):
	lista = list(lista_set)

	for id in range(len(lista)):
		string=(lista[id]).split(';')
		if len(string)==2:
			codigo=string[0][0:5]
			nome=string[0][5:]
			matricula=string[1]
			obj = Funcionario.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
			if obj is None:	
				Funcionario.objects.create(id_municipio=id_municipio,codigo=codigo,nome=nome,matricula=matricula)
	return None				



def gravar_proventos(lista,id_municipio):

	for id in range(len(lista)):
			codigo=(lista[id])[0:4]
			nome=(lista[id])[4:]
			obj = ProvDesc.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
			if obj is None:	
				if codigo in ['0051','0052','0053','0123','0130','0147','0166']:
					tipo='DESCONTO'
				else:
					tipo='VANTAGEM'
				ProvDesc.objects.create(id_municipio=id_municipio,tipo=tipo,codigo=codigo,descricao=nome)
	return None				

def gravar_funcao(lista_set,id_municipio):

	lista = list(lista_set)

	for id in range(len(lista)):
		codigo=(lista[id])[0:4]
		nome=(lista[id])[4:]
		obj = Funcao.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
		if obj is None:	
				Funcao.objects.create(id_municipio=id_municipio,codigo=codigo,funcao=nome)
	return None				

def gravar_vinculo(lista_set,id_municipio):

	lista = list(lista_set)

	for id in range(len(lista)):
		codigo=(lista[id])[0:4]
		nome=(lista[id])[4:]
		obj = Vinculo.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
		if obj is None:	
				Vinculo.objects.create(id_municipio=id_municipio,codigo=codigo,vinculo=nome)
	return None				


def gravar_lotacao(lista_set,id_municipio):

	lista = list(lista_set)

	for id in range(len(lista)):
		codigo=(lista[id])[0:4]
		nome=(lista[id])[4:]
		obj = Lotacao.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
		if obj is None:	
				Lotacao.objects.create(id_municipio=id_municipio,codigo=codigo,lotacao=nome)
	return None				


def gravar_folhaMensal(id_municipio,anomes,cod_depto,cod_setor,cod_funcionario,cod_matricula,cod_funcao,cod_lotacao,cod_vinculo,lista_provdesc):
	funcionario=searchFuncionario(id_municipio,cod_funcionario)
	setor=searchSetor(cod_depto,cod_setor)
	funcao=searchFuncao(id_municipio,cod_funcao)
	lotacao=searchLotacao(id_municipio,cod_lotacao)
	vinculo=searchVinculo(id_municipio,cod_vinculo)

	'''
	FolhaMes.objects.create(
		anomes=anomes,
		funcionario=funcionario,
		id_municipio=id_municipio,
		setor=setor,
		funcao=funcao,
		lotacao=lotacao,
		vinculo=vinculo
		)
	'''

	flmes = FolhaMes(anomes=anomes,funcionario=funcionario,id_municipio=id_municipio,setor=setor,funcao=funcao,lotacao=lotacao,vinculo=vinculo)
	flmes.save()

	#obj = FolhaMes.objects.filter(anomes=anomes,funcionario=funcionario).first()



	for k in range(len(lista_provdesc)):
		codigo_provdesc=lista_provdesc[k]['codigo']
		valor_provdesc=lista_provdesc[k]['valor']
		valor_p = valor_provdesc.replace('.','')
		valor_p = valor_p.replace(',','.')
		valor_v = float(valor_p)

		provdesc=ProvDesc.objects.filter(id_municipio=id_municipio,codigo=codigo_provdesc).first()

		prov = ProventosMes(
			anomes=anomes,
			id_municipio=id_municipio,
			folhames=flmes,
			provdesc=provdesc,
			valor=valor_v)
		prov.save()




def searchFuncionario(id_municipio,codigo):
	obj=Funcionario.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
	if obj is not None:
		return obj
	return None


def searchDepartamento(id_municipio,codigo):
	obj=Departamento.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
	if obj is None:
		observacao='Departamento nao encontrado: '+codigo
		LogErro.objects.create(id_municipio=id_municipio,codigo='01',observacao=observacao)
		return None
	return obj


def searchSetor(cod_depto,cod_setor):

	obj=Setor.objects.select_related('departamento').filter(codigo=cod_setor,departamento__codigo=cod_depto).first()
	if obj is None:
		observacao='Setor nao encontrado: '+str(id_departamento)+';'+codigo
		LogErro.objects.create(id_municipio=id_municipio,codigo='01',observacao=observacao)
		return None
	return obj


def searchLotacao(id_municipio,codigo):
	obj=Lotacao.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
	if obj is None:
		observacao='Lotacao nao encontrado: '+codigo
		LogErro.objects.create(id_municipio=id_municipio,codigo='01',observacao=observacao)
		return None
	return obj

def searchFuncao(id_municipio,codigo):
	obj=Funcao.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
	if obj is None:
		observacao='Funcao nao encontrado: '+codigo
		LogErro.objects.create(id_municipio=id_municipio,codigo='01',observacao=observacao)
		return None
	return obj


def searchVinculo(id_municipio,codigo):
	obj=Vinculo.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
	if obj is None:
		observacao='Vinculo nao encontrado: '+codigo
		LogErro.objects.create(id_municipio=id_municipio,codigo='01',observacao=observacao)
		return None
	return obj




