from .models import Funcao,Vinculo,Secretaria,Vinculo,Evento,Setor


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


def listagemFuncoes(id_municipio):
	lista=[]
	funcoes = Funcao.objects.filter(id_municipio=id_municipio)
	for funcao in funcoes:
		lista.append(funcao.funcao)
	return lista


def listagemEventos(id_municipio):
	lista=[]
	eventos = Evento.objects.filter(id_municipio=id_municipio)
	for evento in eventos:
		lista.append(evento.evento)
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


def criarDictFuncoes(id_municipio):
	lista1=[]
	lista2=[]
	secs = Funcao.objects.filter(id_municipio=id_municipio).order_by('id_funcao')
	for sec in secs:
		lista1.append(
			sec.funcao
			)
		lista2.append(
			sec.id_funcao
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


def criarDictEventos(id_municipio):
	lista1=[]
	lista2=[]
	secs = Evento.objects.filter(id_municipio=id_municipio).order_by('id_evento')
	for sec in secs:
		lista1.append(
			sec.evento
			)
		lista2.append(
			sec.id_evento
			)

	return dict(zip(lista1,lista2))


def criarDictTiposDeEventos(id_municipio):
	lista1=[]
	lista2=[]
	secs = Evento.objects.filter(id_municipio=id_municipio).order_by('id_evento')
	for sec in secs:
		lista1.append(
			sec.id_evento
			)
		lista2.append(
			sec.tipo
			)

	return dict(zip(lista1,lista2))


'''
def dictSecretarias(id_municipio):
	if id_municipio==86:
		return dict(lista_secretarias_86)
	elif id_municipio==15:
		return dict(lista_secretarias_15)

def dictSetores(id_municipio):
	if id_municipio==86:
		return dict(lista_setores_86)
	elif id_municipio==15:
		return dict(lista_setores_15)


def dictFuncoes(id_municipio):
	if id_municipio==86:
		return dict(lista_funcoes_86)
	elif id_municipio==15:
		return dict(lista_funcoes_15)


def dictVinculos(id_municipio):
	if id_municipio==86:
		return dict(lista_vinculos_86)
	elif id_municipio==15:
		return dict(lista_vinculos_15)


def dictEventos(id_municipio):
	if id_municipio==86:
		return dict(lista_eventos_86)
	elif id_municipio==15:
		return dict(lista_eventos_15)


def dictTiposEventos(id_municipio):
	if id_municipio==86:
		return dict(lista_tipos_eventos_86)
	elif id_municipio==15:
		return dict(lista_tipos_eventos_15)

'''