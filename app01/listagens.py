from .models import Vinculo,Secretaria,Vinculo,Evento,Setor,Servidor,Folhames ,Grupo_eventos,Funcao,Grupo_funcoes


def listagemSecretarias(id_municipio):
	lista=[]
	secretarias = Secretaria.objects.filter(id_municipio=id_municipio)
	for secretaria in secretarias:
		lista.append(secretaria.secretaria)
	return lista



def listagemSetores(id_municipio):
	lista=[]
	setores = Setor.objects.select_related('secretaria').filter(secretaria__id_municipio=id_municipio)
	for setor in setores:
		lista.append(setor.secretaria.secretaria+setor.setor)
	return lista

def listagemVinculos(id_municipio):
	lista=[]
	vinculos = Vinculo.objects.filter(id_municipio=id_municipio)
	for vinculo in vinculos:
		lista.append(vinculo.vinculo)
	return lista



def listagemServidores(id_municipio):
    lista=[]
    servidores = Servidor.objects.filter(id_municipio=id_municipio)
    for servidor in servidores:
        lista.append(str(servidor.cod_servidor))
    return lista


def listagemFolhames(id_municipio,anomes):
    lista=[]
    folhames = Folhames.objects.filter(id_municipio=id_municipio,anomes=anomes)
    for folha in folhames:
        lista.append(str(folha.cod_servidor)+'-'+str(anomes))
    return lista



def criarDictSecretarias(id_municipio):
	lista1=[]
	lista2=[]
	secs = Secretaria.objects.filter(id_municipio=id_municipio).order_by('id_secretaria')
	for sec in secs:
		lista1.append(
			sec.secretaria
			)
		lista2.append(
			sec.id_secretaria
			)

	return dict(zip(lista1,lista2))



def criarDictSetores(id_municipio):
	lista1=[]
	lista2=[]
	secs = Setor.objects.select_related('secretaria').filter(secretaria__id_municipio=id_municipio).order_by('id_setor')
	for sec in secs:
		lista1.append(
			sec.secretaria.secretaria+sec.setor
			)
		lista2.append(
			sec.id_setor
			)

	return dict(zip(lista1,lista2))


def criarDictVinculos(id_municipio):
	lista1=[]
	lista2=[]
	secs = Vinculo.objects.filter(id_municipio=id_municipio).order_by('id_vinculo')
	for sec in secs:
		lista1.append(
			sec.vinculo
			)
		lista2.append(
			sec.id_vinculo
			)

	return dict(zip(lista1,lista2))



def listagemGrupoEventos(empresa):
    lista=[]
    geventos = Grupo_eventos.objects.filter(empresa=empresa)
    for gevento in geventos:
        lista.append(gevento.evento_original)
    return lista

def criarDictGrupoEventos(empresa):
	lista1=[]
	lista2=[]
	secs = Grupo_eventos.objects.filter(empresa=empresa).order_by('id_grupo')
	for sec in secs:
		lista1.append(
			sec.evento_original
			)
		lista2.append(
			sec.evento_principal
			)

	return dict(zip(lista1,lista2))


def listagemEventos(empresa):
	lista=[]
	eventos = Evento.objects.filter(empresa=empresa)
	for evento in eventos:
		lista.append(evento.evento)
	return lista


def criarDictEventos(empresa):
	lista1=[]
	lista2=[]
	secs = Evento.objects.filter(empresa=empresa).order_by('id_evento')
	for sec in secs:
		lista1.append(
			sec.evento
			)
		lista2.append(
			sec.id_evento
			)

	return dict(zip(lista1,lista2))


def listagemGrupoFuncoes(empresa):
    lista=[]
    gfuncoes = Grupo_funcoes.objects.filter(empresa=empresa).all().order_by('funcao_original')
    for gfunc in gfuncoes:
        lista.append(gfunc.funcao_original)
    return lista

def criarDictGrupoFuncoes(empresa):
	lista1=[]
	lista2=[]
	funcs = Grupo_funcoes.objects.filter(empresa=empresa).order_by('id_grupo')
	for func in funcs:
		lista1.append(
			func.funcao_original
			)
		lista2.append(
			func.funcao_principal
			)

	return dict(zip(lista1,lista2))


def listagemFuncoes(empresa):
	lista=[]
	funcoes = Funcao.objects.filter(empresa=empresa)
	for funcao in funcoes:
		lista.append(funcao.funcao)
	return lista

def criarDictFuncoes(empresa):
	lista1=[]
	lista2=[]
	secs = Funcao.objects.filter(empresa=empresa).order_by('id_funcao')
	for sec in secs:
		lista1.append(
			sec.funcao
			)
		lista2.append(
			sec.id_funcao
			)

	return dict(zip(lista1,lista2))


def criarDictTiposDeEventos(empresa):
	lista1=[]
	lista2=[]
	secs = Evento.objects.filter(empresa=empresa).order_by('id_evento')
	for sec in secs:
		lista1.append(
			sec.id_evento
			)
		lista2.append(
			sec.tipo
			)

	return dict(zip(lista1,lista2))

