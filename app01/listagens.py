from .models import Funcao,Vinculo,Secretaria,Vinculo,Evento,Setor,Servidor,Folhames,Grupo_eventos


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


def listagemGrupoEventos(id_municipio):
    lista=[]
    geventos = Grupo_eventos.objects.filter(id_municipio=id_municipio)
    for gevento in geventos:
        lista.append(gevento.desc_evento)
    return lista


def listagemEventosRef(id_municipio):
    lista=[]
    geventos = Eventos.objects.filter(id_municipio=id_municipio,ref_evento=1)
    for gevento in geventos:
        lista.append(gevento.evento)
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



def criarDictGrupoEventos(id_municipio):
	lista1=[]
	lista2=[]
	secs = Grupo_eventos.objects.filter(id_municipio=id_municipio).order_by('id_grupo')
	for sec in secs:
		lista1.append(
			sec.desc_evento
			)
		lista2.append(
			sec.desc_evento_principal
			)

	return dict(zip(lista1,lista2))
