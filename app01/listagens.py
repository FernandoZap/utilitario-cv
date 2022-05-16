from .models import Vinculo,Secretaria,Setor,Servidor,Folhames,Funcao,Evento


def listagemSecretarias(id_municipio):
	lista=[]
	secretarias = Secretaria.objects.filter(id_municipio=id_municipio)
	for secretaria in secretarias:
		lista.append(secretaria.secretaria.upper())
	return lista



def listagemSetores(id_municipio):
	lista=[]
	setores = Setor.objects.select_related('secretaria').filter(secretaria__id_municipio=id_municipio)
	for setor in setores:
		lista.append(setor.secretaria.secretaria.upper()+setor.setor.upper())
	return lista

def listagemSetores2(id_municipio):
	lista=[]
	setores = Setor.objects.select_related('secretaria').filter(secretaria__id_municipio=id_municipio)
	for setor in setores:
		lista.append(str(setor.secretaria.id_secretaria)+setor.setor.upper())
	return lista


def listagemVinculos(id_municipio):
	lista=[]
	vinculos = Vinculo.objects.filter(id_municipio=id_municipio)
	for vinculo in vinculos:
		lista.append(vinculo.vinculo.upper())
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
			sec.secretaria.upper()
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
			sec.secretaria.secretaria.upper()+sec.setor.upper()
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
			sec.vinculo.upper()
			)
		lista2.append(
			sec.id_vinculo
			)

	return dict(zip(lista1,lista2))



def listagemEventos(id_municipio):
	lista=[]
	eventos = Evento.objects.filter(id_municipio=id_municipio)
	for evento in eventos:
		lista.append(evento.evento.upper())
	return lista


def criarDictEventos(id_municipio):
	lista1=[]
	lista2=[]
	secs = Evento.objects.filter(id_municipio=id_municipio).order_by('id_evento')
	for sec in secs:
		lista1.append(
			sec.evento.upper()
			)
		if sec.id_evento_cv==0:
			id_object=sec.id_evento
		else:
			id_object=sec.id_evento_cv
		lista2.append(
			id_object
			)

	return dict(zip(lista1,lista2))


def listagemFuncoes(id_municipio):
	lista=[]
	funcoes = Funcao.objects.filter(id_municipio=id_municipio)
	for funcao in funcoes:
		lista.append(funcao.funcao.upper())
	return lista



def criarDictFuncoes(id_municipio):
	lista1=[]
	lista2=[]
	secs = Funcao.objects.filter(id_municipio=id_municipio).order_by('id_funcao')
	for sec in secs:
		lista1.append(
			sec.funcao.upper()
			)
		if sec.id_funcao_cv==0:
			id_object=sec.id_funcao
		else:
			id_object=sec.id_funcao_cv

		lista2.append(
			id_object
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
