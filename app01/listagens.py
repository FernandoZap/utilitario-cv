from .models import Vinculo,Secretaria,Setor,Servidor,Folhames,Funcao,Evento,Refeventos,Municipio


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


def criarDictRefEventos(id_municipio,anomes):
	lista1=[]
	lista2=[]
	refE=Refeventos.objects.filter(id_municipio=id_municipio,anomes=anomes)
	for ref in refE:
		lista1.append(
			ref.cod_servidor
			)
		lista2.append(
			ref.ref_eventos
			)

	return dict(zip(lista1,lista2))


def criarDictNomeServidor(id_municipio):
        lista1=[]
        lista2=[]
        objs = Servidor.objects.filter(id_municipio=id_municipio).values('cod_servidor','nome','data_admissao')
        for obj in objs:
                lista1.append(
                        obj['cod_servidor']
                        )
                lista2.append(
                        {'nome':obj['nome'],'data':obj['data_admissao']}
                        )

        return dict(zip(lista1,lista2))


def criarDictIdSecretarias(id_municipio):
        lista1=[]
        lista2=[]
        secs = Secretaria.objects.filter(id_municipio=id_municipio).values('id_secretaria','secretaria')
        for sec in secs:
                lista1.append(
                        sec['id_secretaria']
                        )
                lista2.append(
                        sec['secretaria']
                        )

        return dict(zip(lista1,lista2))



def criarDictIdSetores(id_municipio):
        lista1=[]
        lista2=[]
        secs = Setor.objects.select_related('secretaria').filter(secretaria__id_municipio=id_municipio).order_by('id_setor')
        for sec in secs:
                lista1.append(
                        sec.id_setor
                        )
                lista2.append(
                        sec.setor
                        )

        return dict(zip(lista1,lista2))


def criarDictIdFuncoes(id_municipio):
        lista1=[]
        lista2=[]
        secs = Funcao.objects.filter(id_municipio=id_municipio).values('id_funcao','funcao')
        for sec in secs:
                lista1.append(
                        sec['id_funcao']
                        )
                lista2.append(
                        sec['funcao']
                        )

        return dict(zip(lista1,lista2))


def criarDictIdVinculos(id_municipio):
        lista1=[]
        lista2=[]
        secs = Vinculo.objects.filter(id_municipio=id_municipio).values('id_vinculo','vinculo')
        for sec in secs:
                lista1.append(
                        sec['id_vinculo']
                        )
                lista2.append(
                        sec['vinculo']
                        )

        return dict(zip(lista1,lista2))


def criarDictIdEventosVantagens(id_municipio):
        lista1=[]
        lista2=[]
        secs = Evento.objects.filter(id_municipio=id_municipio,tipo='V').order_by('evento')
        for sec in secs:
                lista1.append(sec.id_evento)
                lista2.append(sec.evento)
        return dict(zip(lista1,lista2))


def criarDictMunicipios():
        lista1=[]
        lista2=[]
        nums = Municipio.objects.filter(empresa__in=['SS','Layout','Aspec'])
        for obj in nums:
                lista1.append(obj.id_municipio)
                lista2.append(obj.municipio)
        return dict(zip(lista1,lista2))


def colunasValores():
	lista1=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	lista2=[]
	for k in range(9,26):
		lista2.append(lista1[k])
	lista3=[]
	for k in range(0,4):
		c1=lista1[k]
		for l in range(len(lista1)):
			lista3.append(c1+lista1[l])
	return lista2+lista3			

















