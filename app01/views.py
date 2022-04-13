from django.shortcuts import render,redirect
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import choices,importarPlanilha,listagens,funcoes_gerais,cadastro_01
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Municipio,Planilha,Folhames,Secretaria,Setor,Vinculo
from accounts.models import User
from django.db.models import Count,Sum
import csv
import datetime
import os
import json
import mysql.connector
import openpyxl
import re
from django.core.files import File
import zipfile
from django.db import connection
import unicodedata

#https://docs.djangoproject.com/en/4.0/topics/db/sql/




# git remote set-url origin git@github.com:FernandoZap/utilitario-cv.git



# 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

#curl -H 'Authorization: token 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' https://api.github.com/FernandoZap/utilitario-cv


def get(self, request, *args, **kwargs):
    self.request.session['funcao'] = self.request.user.funcao
    self.request.session['username'] = self.request.user.username
    return super().get(request, *args, **kwargs)  



def sessao(request):
    if not request.session.get('username'):
        request.session['username'] = request.user.username
    return




def processUserInfo(request,userInfo):
    #userInfo = json.loads(userInfo)
    print()
    print("USER INFO RECEIVED")
    print('--------------------------')
    #print(f"User Name: {userInfo['name']}")
    #print(f"User Type: {userInfo['type']}")
    print()
    return "Info received successfuly"


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def formatMilhar(valor):
    vd = f"{valor:,.2f}"
    vd = vd.replace('.','-')
    vd = vd.replace(',','.')
    vd = vd.replace('-',',')
    return vd


def importacaoFolhaExcel(request):
    #lista = listagens.listagemSetores2(86)
    #print (lista)

    #------------------------------------------------------------------------------
    # esta rotina para ler o arquivo .zip da folha de pagamento de cada municipio
    # e gravar no banco os departamentos/setores/funcionarios/cargos/vinculos,
    #  proventos e descontos.
    #-----------------------------------------------------------------------------
    titulo_html = 'Importar Folha - Atenção: informe apenas arquivo .zip'

    '''
    objs=Eventos_cv.objects.all()
    for obj in objs:
        evento=obj.evento
        evento=funcoes_gerais.remove_combining_fluent(evento)
        obj.evento=evento
    Eventos_cv.objects.bulk_update(objs,['evento'])

    ls1=[e.id_evento_cv for e in Eventos_cv.objects.all()]
    ls2=[e.id_evento_cv for e in Evento.objects.all()]
    ls3=set(ls2)

    for k in range(len(ls1)):
        if ls1[k] not in ls3:
            #print (ls1[k])
            Eventos_cv.objects.get(pk=ls1[k]).delete()

    ls1=[e.id_funcao_cv for e in Funcoes_cv.objects.all()]
    ls2=[e.id_funcao_cv for e in Funcao.objects.all()]
    ls3=set(ls2)

    for k in range(len(ls1)):
        if ls1[k] not in ls3:
            #print (ls1[k])
            Funcoes_cv.objects.get(pk=ls1[k]).delete()
    '''            


    lista=[]

    lista.append('ADMINISTRADOR')
    lista.append('ADVOGADO')
    lista.append('AGENTE ADMINISTRATIVO')
    lista.append('AGENTE COMUNITARIO DE SAUDE')
    lista.append('AGENTE DE COLABORAÇÃO EXTERNA')
    lista.append('AGENTE DE COMBATE ENDEMIAS')
    lista.append('AGENTE SOCIAL')
    lista.append('AGRONOMO')
    lista.append('ALMOXARIFE')
    lista.append('ANALISTA AMBIENTAL')
    lista.append('ANALISTA DE POLITICAS PUBLICAS')
    lista.append('ANALISTA DE TECNOLOGIA DA INFORMACAO')
    lista.append('ARQUITETO URBANISTA')
    lista.append('ARQUIVISTA')
    lista.append('ASSESSOR COMUNITARIO')
    lista.append('ASSESSOR DE ANALISE DE CREDITO')
    lista.append('ASSESSOR DE APOIO A CIDADANIA')
    lista.append('ASSESSOR DE COMUNICACAO SOCIAL I')
    lista.append('ASSESSOR DE COMUNICAÇÃO SOCIAL II')
    lista.append('ASSESSOR DE COMUNICACAO SOCIAL III')
    lista.append('ASSESSOR DE GABINETE')
    lista.append('ASSESSOR DE IMPRENSA')
    lista.append('ASSESSOR DE MARKETING')
    lista.append('ASSESSOR DE PLANEJAMENTO')
    lista.append('ASSESSOR ESPECIAL')
    lista.append('ASSESSOR ESPECIAL DE ART. INSTITUCIONAL')
    lista.append('ASSESSOR ESPECIAL DE ASSUNTOS LEGISLATIVOS')
    lista.append('ASSESSOR ESPECIAL DE DES. DO MICRO E PEQUENO EMPREENDEDORISM')
    lista.append('ASSESSOR ESPECIAL DE MOBILIZAÇÃO SOCIAL')
    lista.append('ASSESSOR EXECUTIVO')
    lista.append('ASSESSOR FINANCEIRO')
    lista.append('ASSESSOR JURIDICO')
    lista.append('ASSESSOR TECNICO')
    lista.append('ASSIST. DE GAB. DO PROCURADOR')
    lista.append('ASSISTENTE DA DEFESA CIVIL')
    lista.append('ASSISTENTE DE APOIO ADM I')
    lista.append('ASSISTENTE DE APOIO ADM II')
    lista.append('ASSISTENTE DE APOIO ADM III')
    lista.append('ASSISTENTE DE ATIVIDADES CULTURAIS E DESPORTIVAS')
    lista.append('ASSISTENTE DE COMPRAS')
    lista.append('ASSISTENTE DE COORD. DE POLITICAS PUB. SOBRE DROGAS')
    lista.append('ASSISTENTE DE GABINETE I')
    lista.append('ASSISTENTE DE GABINETE II')
    lista.append('ASSISTENTE JURÍDICO')
    lista.append('ASSISTENTE SOCIAL')
    lista.append('ATENDENTE DE ENFERMAGEM')
    lista.append('AUDITOR DE CONTROLE INTERNO')
    lista.append('AUDITOR FISCAL DA RECEITA MUNICIPAL')
    lista.append('AUXILIAR DE ENFERMAGEM')
    lista.append('AUXILIAR DE SERVIÇOS GERAIS')
    lista.append('AUXILIAR EM SAUDE BUCAL')
    lista.append('BIBLIOTECARIO(A)')
    lista.append('BOMBEIRO HIDRAULICO')
    lista.append('CH. AS. MED. HOSP.')
    lista.append('CHEFE DA CELULA DE INSTANCIA E JULGAMENTO DE DEFESA')
    lista.append('CHEFE DA DIV DE VIGILANCIA EPIDEMIOLOGICA')
    lista.append('CHEFE DA FARMACIA')
    lista.append('CHEFE DA MAN. E FISC. DA REDE')
    lista.append('CHEFE DA MECANICA')
    lista.append('CHEFE DA SERRARIA')
    lista.append('CHEFE DE DIV DE ACOES DAS UBASF')
    lista.append('CHEFE DE DIV DE ADM DE PESSOAL')
    lista.append('CHEFE DE DIV. DE APOIO AO CREDITO')
    lista.append('CHEFE DE DIV DE APOIO A QUALIFICACAO PROFISSIONAL')
    lista.append('CHEFE DE DIV DE ARTES PLASTICAS E LITERATURA')
    lista.append('CHEFE DE DIV DE ASSISTENCIA FARMACEUTICA')
    lista.append('CHEFE DE DIV DE ASSISTENCIA ODONTOLOGICO')
    lista.append('CHEFE DE DIV DE CADASTRO TECNICO MULTIFINALITARIO')
    lista.append('CHEFE DE DIV. DE CONSERVAÇÃO AMBIENTAL')
    lista.append('CHEFE DE DIV DE CONTROLE DE ENDEMIAS')
    lista.append('CHEFE DE DIV DE DANÇAS REG E ARTESANATO')
    lista.append('CHEFE DE DIV DE DES DO COMERCIO')
    lista.append('CHEFE DE DIV. DE DIVULGAÇÃO E PROMOÇÃO')
    lista.append('CHEFE DE DIV DE EDUCAÇÃO DE TRANSITO E TRANSPORTE')
    lista.append('CHEFE DE DIV DE ENGENHARIA, SINALIZAÇÃO, ESTUDOS DE TRANSPOR')
    lista.append('CHEFE DE DIV DE FISCALIZAÇÃO, ADM, CADASTRO E VISTORIA')
    lista.append('CHEFE DE DIV. DE FISCALIZAÇÃO DE OBRAS')
    lista.append('CHEFE DE DIV DE FISCALIZAÇÃO DE OBRAS-SRP')
    lista.append('CHEFE DE DIV DE GESTÃO DE EQUIPAMENTOS TURISTICOS')
    lista.append('CHEFE DE DIV. DE LIMPEZA PUB. E MANUTENÇÃO')
    lista.append('CHEFE DE DIV. DE MÚSICA')
    lista.append('CHEFE DE DIV DE OBRAS E MANUTENCAO')
    lista.append('CHEFE DE DIV DE OBRAS E SANEAMENTO')
    lista.append('CHEFE DE DIV DE PECUARIA')
    lista.append('CHEFE DE DIV DE PESQUISAS E INFORMACOES TURISTICAS')
    lista.append('CHEFE DE DIV DE PLANEJAMENTO ORÇAMENTARIO E PROJETOS ESPECIA')
    lista.append('CHEFE DE DIV DE PLANEJAMENTO URBANO')
    lista.append('CHEFE DE DIV DE PROTOCOLO')
    lista.append('CHEFE DE DIV DE SERVIÇOS GERAIS')
    lista.append('CHEFE DE DIV DE SISTEMA DE REFERENCIA E CONTRA-REFERENCIA')
    lista.append('CHEFE DE DIVISAO DE ADM DE RH')
    lista.append('CHEFE DE DIVISÃO DE ADMINISTRAÇÃO')
    lista.append('CHEFE DE DIVISAO DE CICLISMO E ATLETISMO')
    lista.append('CHEFE DE DIVISÃO DE EXECUÇÃO')
    lista.append('CHEFE DE DIVISAO DE FINANCAS')
    lista.append('CHEFE DE DIVISÃO DE FUTEBOL')
    lista.append('CHEFE DE DIVISAO DE FUTSAL')
    lista.append('CHEFE DE DIVISAO DE MANUTENÇÃO')
    lista.append('CHEFE DE DIVISAO DE URBANISMO')
    lista.append('CHEFE DE DIVISAO DO ALMOXARIFADO')
    lista.append('CHEFE DE DIVISÃO FINANCEIRA')
    lista.append('CHEFE DE DIVISÃO TÉCNICA')
    lista.append('CHEFE DE DIV. PROTAGONISMO JUVENIL')
    lista.append('CHEFE DE PROJETOS')
    lista.append('CHEFE DIV DESENVOLVIMENTO DA INDUSTRIA')
    lista.append('CHEFE DIV. INFOR. ESTATISTICA')
    lista.append('CHEFE DIVISÃO DE VOLEI')
    lista.append('CHEFE DIV. PART. COMUNITARIA')
    lista.append('CHEFE DO ALMOXARIFADO CENTRAL')
    lista.append('CHEFE DO DEP. DE OBRAS E MANUTENÇÃO')
    lista.append('CHEFE DO ESCRITORIO DE FORTALEZA')
    lista.append('CHEFE DO SERV. DE ENG. DE PESCA')
    lista.append('CHEFE POSTO SERV DIVERSOS')
    lista.append('COND TRANS ESCOLAR CAT D')
    lista.append('CONTADOR(A)')
    lista.append('CONTRA-MESTRO')
    lista.append('COORD ADMINISTRATIVO DA UPA')
    lista.append('COORD. ADMINISTRATIVO DO CEMITERIO')
    lista.append('COORD DA ATENCAO SECUNDARIA E TERCIARIA')
    lista.append('COORD DA GESTAO DE RECURSOS HUMANO')
    lista.append('COORD. DA JUVENTUDE, ESPORTE E CULTURA')
    lista.append('COORD. DA VIGILÂNCIA SOCIAL')
    lista.append('COORD. DE ADM. GESTÃO ESTRATÉGICA E PESSOAS')
    lista.append('COORD DE CIENCIA, TECNOLOGIA E INOVAÇAO')
    lista.append('COORD. DE CONTROLE AVALIAÇÃO REGULAÇÃO E AUDITORIA')
    lista.append('COORD. DE POLITICAS PUB. SOBRE DROGAS')
    lista.append('COORD DISTRITAL DA TAIBA E SIUPE')
    lista.append('COORD DO POLO DE ATENDIMENTO')
    lista.append('COORDENADOR ADMINISTRATIVO FINANCEIRO')
    lista.append('COORDENADOR DA ACAO SOCIAL')
    lista.append('COORDENADOR DA ATENÇÃO BÁSICA')
    lista.append('COORDENADOR DA DEFESA CIVIL')
    lista.append('COORDENADOR DA FISIOTERAPIA')
    lista.append('COORDENADOR DA ILHA DIGITAL')
    lista.append('COORDENADOR DAS ACOES BASICAS')
    lista.append('COORDENADOR DA SECAO CADISTA')
    lista.append('COORDENADOR DE AGENTES DA VIG DA SAU')
    lista.append('COORDENADOR DE AREA')
    lista.append('COORDENADOR DE ARTICULAÇÃO INSTITUCIONAL')
    lista.append('COORDENADOR DE ASSUNTOS EDUCACIONAIS')
    lista.append('COORDENADOR DE CAPOEIRA')
    lista.append('COORDENADOR DE COMPRAS E SERVIÇOS')
    lista.append('COORDENADOR DE DANÇA')
    lista.append('COORDENADOR DE EQUIPAMENTOS ESPORTIVOS')
    lista.append('COORDENADOR DE ESPORTE')
    lista.append('COORDENADOR DE ESPORTES')
    lista.append('COORDENADOR DE IMPRENSA')
    lista.append('COORDENADOR DE MOBILIZAÇÃO SOCIAL')
    lista.append('COORDENADOR DE PLANEJAMENTO ORÇAMENTO E MODERNIZAÇÃO')
    lista.append('COORDENADOR DE POSTO')
    lista.append('COORDENADOR DE PROJETOS I')
    lista.append('COORDENADOR DE PROJETOS III')
    lista.append('COORDENADOR DE REGULARIZAÇÃO FUNDIÁRIA URBANA E RURAL')
    lista.append('COORDENADOR DE SERVIÇOS GERAIS')
    lista.append('COORDENADOR DE TRANSPORTES')
    lista.append('COORDENADOR DISTRITAL I')
    lista.append('COORDENADOR DISTRITAL II')
    lista.append('COORDENADOR DISTRITAL III')
    lista.append('COORDENADOR DISTRITAL IV')
    lista.append('COORDENADOR DISTRITAL V')
    lista.append('COORDENADOR DO CACI')
    lista.append('COORDENADOR DO CADASTRO UNICO')
    lista.append('COORDENADOR DO CADASTRO UNICO II')
    lista.append('COORDENADOR DO CAPS')
    lista.append('COORDENADOR DO CENTRO DE FEIRAS E CONCENÇÕES')
    lista.append('COORDENADOR DO CREAS')
    lista.append('COORDENADOR DO NASF')
    lista.append('COORDENADOR DO PETI')
    lista.append('COORDENADOR DO PRO-JOVEM')
    lista.append('COORDENADOR DO SETOR DE BIOLOGIA DA SEMEIO')
    lista.append('COORDENADOR GERAL DA EQUIPE TECNICA FAMILIA ACOLHEDORA')
    lista.append('COORDENADOR LIMPEZA I')
    lista.append('COORDENADOR LIMPEZA II')
    lista.append('COORDENADOR PEDAGÓGICO')
    lista.append('COORDENADOR PROJETOS II')
    lista.append('COORDENADOR REGIONAL I')
    lista.append('COORDENADOR REGIONAL II')
    lista.append('COORD MUN DE POLITICAS P/ CRIANÇAS E ADOLESCENTES')
    lista.append('COORD MUNICIPAL DE POLITICAS PÚBLICAS PARA AS MULHERES')
    lista.append('COZINHEIRO(A)')
    lista.append('DIGITADOR(A)')
    lista.append('DIRETOR ASSISTENCIA ODONTOLOGICA')
    lista.append('DIRETOR BANDA MUSICA')
    lista.append('DIRETOR CLINICO-TECNICO DA UPA')
    lista.append('DIRETOR CORPO CLINICO')
    lista.append('DIRETOR DA DEFESA CIVIL PATRIMONIAL E CIDADANIA')
    lista.append('DIRETOR DA UPA PECÉM')
    lista.append('DIRETOR DE DEP. ADMINISTRATIVO-FINANCEIRO')
    lista.append('DIRETOR DE DEPARTAMENTO DE CONSERVAÇÃO')
    lista.append('DIRETOR DE DEPARTAMENTO DE OBRAS')
    lista.append('DIRETOR DE DEPARTAMENTO PEDAGOGICO')
    lista.append('DIRETOR DE DEP DE CULTURA')
    lista.append('DIRETOR DE DEP DE DES DO TURISMO')
    lista.append('DIRETOR DE DEP DE DES URBANO')
    lista.append('DIRETOR DE DEP. DE ESPORTE')
    lista.append('DIRETOR DE DEP DE GERAÇÃO DE EMPREGO, RENDA E EMPREENDEDORIS')
    lista.append('DIRETOR DE DEP DE PROTEÇÃO SOCIAL ESPECIAL')
    lista.append('DIRETOR DE DEP DE RECURSOS HIDRICOS')
    lista.append('DIRETOR DEP. ADM. E FINANCAS')
    lista.append('DIRETOR DEPARTAMENTO')
    lista.append('DIRETOR DEPARTAMENTO DE PLANEJAMENTO')
    lista.append('DIRETOR DEP. DES.IND.COMERCIO')
    lista.append('DIRETOR DEP MEIO AMBIENTE')
    lista.append('DIRETOR DE PROJETOS ESPECIAIS')
    lista.append('DIRETOR DEP TEC DE SERV DE SAUDE')
    lista.append('DIRETOR DE UNIDADE ESCOLAR I')
    lista.append('DIRETOR DE UNIDADE ESCOLAR IV')
    lista.append('DIRETOR DE UNIDADE ESCOLAR V')
    lista.append('DIRETOR DE UNIDADE ESCOLAR VI')
    lista.append('DIRETOR DO DEPARTAMENTO DE PROJETOS')
    lista.append('DIRETOR PROJETOS')
    lista.append('EDUCADOR INFANTIL')
    lista.append('EDUCADOR SOCIAL')
    lista.append('ELETRICISTA')
    lista.append('ENCARREGADO PARA ASSUNTO EXTERNOS')
    lista.append('ENFERMEIRO(A)')
    lista.append('ENFERMEIRO(A) PSF')
    lista.append('ENFERMEIRO CHEFE DO PSF')
    lista.append('ENGENHEIRO AGRONOMO')
    lista.append('ENGENHEIRO CIVIL')
    lista.append('ENGENHEIRO ELETRICISTA')
    lista.append('ENGENHEIRO FLORESTAL')
    lista.append('ENTREVISTADOR')
    lista.append('ESTATISTICO')
    lista.append('FACILITADOR(A)')
    lista.append('FARMACEUTICO(A) BIOQUIMICO(A)')
    lista.append('FISCAL AMBIENTAL')
    lista.append('FISCAL DE OBRAS')
    lista.append('FISCAL DE OBRAS COM CNH')
    lista.append('FISCAL DE OBRAS E POSTURAS')
    lista.append('FISCAL DE VIGILANCIA EM SAUDE')
    lista.append('FISIOTERAPEUTA')
    lista.append('FONOAUDIOLOG0')
    lista.append('FORMADOR ANOS FINAIS ENS FUND LINGUA PORTUGUESA')
    lista.append('FORMADOR ANOS FINAIS ENS FUND MATEMATICA')
    lista.append('FORMADOR DA EDUCAÇÃO INFANTIL')
    lista.append('FORMADOR DOS ANOS INICIAIS DO ENS FUNDAMENTAL')
    lista.append('GARI VARRIÇÃO E CAPINA')
    lista.append('GEOGRAFO')
    lista.append('GERENTE ADMINISTRATIVO')
    lista.append('GERENTE DA CELULA DE ASSISTENCIA SOCIAL')
    lista.append('GERENTE DE BIOLOGIA')
    lista.append('GERENTE DE CADASTRO')
    lista.append('GERENTE DE CADASTRO E ARREGIMENTAÇÃO DAS FAMILIAS')
    lista.append('GERENTE DE CADASTRO E EXTESAO FLORESTAL')
    lista.append('GERENTE DE CELULA DE ATENÇÃO AO INFANTE')
    lista.append('GERENTE DE CONTENCIOSO JUDICIAL')
    lista.append('GERENTE DE ESTUDO GEOLÓGICO')
    lista.append('GERENTE DE LICITAÇÕES')
    lista.append('GERENTE DE MARKETING AO TURISMO')
    lista.append('GERENTE DE PARECERES E PROCESSOS')
    lista.append('GERENTE DE TRIAGEM')
    lista.append('GERENTE DO SISTEMA TURISTICO')
    lista.append('GUARDA CIVIL MUNICIPAL')
    lista.append('INSTRUTOR DA ESCOLINHA DE FUTEBOL')
    lista.append('INSTRUTOR DE ARTES PLASTICAS E CENICAS')
    lista.append('INSTRUTOR DE BASQUETE')
    lista.append('INSTRUTOR DE CAPOEIRA')
    lista.append('INSTRUTOR DE DANÇA')
    lista.append('INSTRUTOR DE MUSICA')
    lista.append('INSTRUTOR DE XADREZ')
    lista.append('MAESTRO')
    lista.append('MARCENEIRO')
    lista.append('MEDICO CARDIOLOGISTA')
    lista.append('MEDICO CIRURGIAO')
    lista.append('MEDICO PLANTONISTA')
    lista.append('MEDICO PSF')
    lista.append('MEMBRO DO CONS. TUTELAR')
    lista.append('MOTORISTA')
    lista.append('MOTORISTA CAT B')
    lista.append('MOTORISTA CAT. D')
    lista.append('NUTRICIONISTA')
    lista.append('ODONTOLOGO(A)')
    lista.append('ODONTOLOGO(A) PSF')
    lista.append('OPERADOR DE MAQUINAS')
    lista.append('ORIENTADOR SOCIAL')
    lista.append('OUVIDOR DO MUNICIPIO')
    lista.append('PEDAGOGA')
    lista.append('PORTEIRO')
    lista.append('PREFEITO MUNICIPAL')
    lista.append('PREGOEIRO')
    lista.append('PRESIDENTE DA COMISSÃO DE LICITAÇÃO')
    lista.append('PROCURADOR DO MUNICIPIO')
    lista.append('PROCURADOR GERAL DO MUNICIPIO')
    lista.append('PROF ANOS FINAIS ENS FUND LINGUA INGLESA')
    lista.append('PROF ANOS FINAIS ENS FUND LINGUA PORTUGUESA')
    lista.append('PROF ENS FUND II EDUCAÇÃO FISICA')
    lista.append('PROF ENS FUND II GEOGRAFIA')
    lista.append('PROF ENS FUND II HISTORIA')
    lista.append('PROF ENS FUND II INGLES')
    lista.append('PROF ENS FUND II LIBRAS')
    lista.append('PROF ENS FUND II LINGUA PORTUGUESA')
    lista.append('PROF ENS FUND II MATEMATICA')
    lista.append('PROFESSOR ANOS FINAIS ENS FUND ARTE')
    lista.append('PROFESSOR ANOS FINAIS ENS FUND CIENCIAS')
    lista.append('PROFESSOR ANOS FINAIS ENS FUND EDUC FISICA')
    lista.append('PROFESSOR ANOS FINAIS ENS FUND ENS RELIGIOSO')
    lista.append('PROFESSOR ANOS FINAIS ENS FUND HISTORIA')
    lista.append('PROFESSOR ANOS FINAIS ENS FUND MATEMATICA')
    lista.append('PROFESSOR ANOS INICIAIS ENSINO FUNDAMENTAL')
    lista.append('PROFESSOR DA EDUCAÇÃO INFANTIL')
    lista.append('PROFESSOR DE EDUC INFANTIL')
    lista.append('PROFESSOR EDUC BASICA I')
    lista.append('PROFESSOR EJA 1º SEG')
    lista.append('PROFESSOR ENS FUND I')
    lista.append('PROFESSOR ENS FUND II')
    lista.append('PROFESSOR SALAS ATEND EDUCACIONAL ESPECIALIZADO')
    lista.append('PROF FUND II CIENCIAS')
    lista.append('PSICOLOGO')
    lista.append('PSICOPEDAGOGO')
    lista.append('REGENTE DE ENSINO')
    lista.append('SEC.DO TRABALHO E DESENVOLVIMENTO SOCIAL')
    lista.append('SECRETÁRIA DO GABINETE')
    lista.append('SECRETARIO(A) EXECUTIVO')
    lista.append('SECRETÁRIO DA CULTURA')
    lista.append('SECRETARIO DA INFRAESTRUTURA')
    lista.append('SECRETÁRIO DA SEC REGIONAL DO PECÉM')
    lista.append('SECRETARIO DAS FINANCAS')
    lista.append('SECRETARIO DE CONTROLADORIA OUVIDORIA E TRANSPARENCIA')
    lista.append('SECRETÁRIO DE PLANEJAMENTO ADM E GESTÃO')
    lista.append('SECRETARIO DO DES AGRARIO E RURAL')
    lista.append('SECRETARIO DO DES ECONOMICO')
    lista.append('SECRETÁRIO DO ESPORTE E JUVENTUDE')
    lista.append('SECRETARIO DO GOVERNO')
    lista.append('SECRETARIO DO MEIO AMBIENTE E URBANISMO')
    lista.append('SECRETARIO ESCOLAR')
    lista.append('SECRETARIO ESCOLAR COMISSIONADO')
    lista.append('SECRETARIO EXECUTIVO DOS CONSELHOS')
    lista.append('SUPERVISOR PEDAGOGICO')
    lista.append('TECNICO(A) RADIOLOGIA')
    lista.append('TECNICO EM AGROPECUARIA')
    lista.append('TECNICO EM EDIFICACAO')
    lista.append('TECNICO EM ENFERMAGEM')
    lista.append('TECNICO EM RECURSOS HUMANOS')
    lista.append('TECNICO EM SAUDE BUCAL')
    lista.append('TELEFONISTA')
    lista.append('TERAPEUTA OCUPACIONAL')
    lista.append('TOPÓGRAFO')
    lista.append('TRATORISTA')
    lista.append('TURISMÓLOGO')
    lista.append('VETERINARIO(A)')
    lista.append('VICE-PREFEITO')
    lista.append('VIGIA')
    lista.append('VISITADOR')

    carga_funcao=[]

    for kk in range(len(lista)):
        func38=lista[kk]
        func38=remove_combining_fluent(func38)
        objf=Funcao(
            id_municipio=38,
            empresa='SS',
            funcao=func38,
            id_funcao_cv=0
            )
        carga_funcao.append(objf)

    Funcao.objects.bulk_create(carga_funcao)
    lista=[]


    mensagem=''
    municipios=Municipio.objects.all().order_by('municipio')
    if (request.method == "POST"):

        current_user = 0  #request.user.iduser
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        tabela=request.POST['tabela']
        anomes=int(ano+mes)


        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
        else:
            empresa = ''
            logerro=LogErro(
            id_municipio = id_municipio,
            anomes = anomes,
            observacao = 'Empresa do municipio nao identificada')
            logerro.save()

        entidade='PREFEITURA MUNICIPAL DE '+municipio.upper()
        if id_municipio==38:
            entidade='GOVERNO MUNICIPAL DE SAO GONCALO DO AMARANTE'



        '''
        obj = Folhames.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
        if obj is not None:
            return render(request, 'app01/planilhaErrada.html',
                    {
                        'titulo': 'Processamento da Folha',
                        'municipio':municipio,
                        'anomes':str(mes)+'/'+str(ano),
                        'mensagem':'A Folha selecionada já foi processada!'

                    }
                )
        '''

        mes_ref = funcoes_gerais.mesReferencia(mes)

        if tabela=='SecFuncVincEvento':
            retorno = importarPlanilha.importarSecFuncVincEventos(id_municipio,anomes,entidade,empresa)
        elif tabela=='Setor':    
            retorno = importarPlanilha.importarSetores(id_municipio,anomes,entidade,empresa)
        elif tabela=='Servidor':            
            retorno = importarPlanilha.importarServidores(id_municipio,anomes,entidade,empresa)
        elif tabela=='Folha':
            retorno = importarPlanilha.importarFolha(id_municipio,anomes,entidade,empresa)
        elif tabela == 'Geral':
            retorno = importarPlanilha.importarSecFuncVincEventos(id_municipio,anomes,entidade,empresa)
            if retorno==1:
                retorno = importarPlanilha.importarSetores(id_municipio,anomes,entidade,empresa)
                retorno = importarPlanilha.importarServidores(id_municipio,anomes,entidade,empresa)
                retorno = importarPlanilha.importarFolha(id_municipio,anomes,entidade,empresa)
            else:                
                return render(request, 'app01/planilhaErrada.html',
                        {
                            'titulo': 'Processamento da Folha',
                            'municipio':municipio,
                            'anomes':str(mes)+'/'+str(ano),
                            'mensagem':'Nao existe nenhum registro desse municipio e desse mes para ser processado!'

                        }
                    )

        return HttpResponseRedirect(reverse('app01:importacaoFolhaExcel'))


    return render(request, 'app01/importacaoFolhaExcel.html',
            {
                'titulo': titulo_html,
                'mensagem':mensagem,
                'municipios':municipios
            }
          )

def planilhaErrada(request):
    return render(request, 'app01/planilhaErrada.html')




def listFolhaResumo(request):

    opcao=''
    query1=None
    query2=None
    titulo='Listar soma por Secretarias/Setores'
    cursor = connection.cursor()
    id_municipio=86
    anomes='202111'
    municipio='Caridade'
    referencia='202111'
    rs=0
    lista1=[]
    lista2=[]

    total_v=0
    total_d=0
    total_r=0
    qT=0

    municipios = Municipio.objects.all().order_by('municipio')
    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

        cursor.execute("SELECT f001_quantidadeServidoresMes (%s,%s)",[anomes,id_municipio])
        qt = dictfetchall(cursor)
        #qt[0]["f001_quantidadeServidores (202111,'86')"]
        #print (qt[0]["f001_quantidadeServidores (202111,'86')"])
        #print ('valor da funcao')
        for e in qt[0].values():
            qT=e

        cursor.execute("select s.id_secretaria,s.secretaria,sum(vantagens) as vantagens, sum(descontos) as descontos\
        from v001_valoresmes v,secretarias s\
        where v.id_secretaria=s.id_secretaria\
        and v.id_municipio=%s\
        and v.anomes=%s\
        group by s.id_secretaria,s.secretaria ORDER BY s.secretaria",[id_municipio,anomes])

        query0 = dictfetchall(cursor)

        for q in query0:
            resultado=q['vantagens']-q['descontos']
            total_v+=q['vantagens']
            total_d+=q['descontos']
            total_r+=resultado


            lista1.append(
                {
                    'id_secretaria':q['id_secretaria'],
                    'secretaria':q['secretaria'],
                    'vantagens':formatMilhar(q['vantagens']),
                    'descontos':formatMilhar(q['descontos']),
                    'resultado':formatMilhar(resultado),
                }
                )

#'''''''''''''''''''''''''''''''''''''''
        
        cursor.execute("select s.id_secretaria,s.secretaria,st.setor,sum(vantagens) as vantagens, sum(descontos) as descontos\
        from v001_valoresmes v,secretarias s,setores st\
        where v.id_secretaria=s.id_secretaria\
        and s.id_secretaria=st.secretaria_id\
        and st.id_setor=v.id_setor\
        and v.id_municipio=%s\
        and v.anomes=%s\
        group by s.id_secretaria,s.secretaria,st.setor order by s.secretaria,st.setor",[id_municipio,anomes])

        query1 = dictfetchall(cursor)

        for q in query1:
            secretaria=q['secretaria']
            id_secretaria=q['id_secretaria']

            for k1 in lista1:
                if k1['id_secretaria']==id_secretaria:
                    v_dep=k1['vantagens']
                    d_dep=k1['descontos']
                    r_dep=k1['resultado']

            resultado=q['vantagens']-q['descontos']
            lista2.append(
                {
                    'secretaria':q['secretaria'],
                    'setor':q['setor'],
                    'vantagens':formatMilhar(q['vantagens']),
                    'descontos':formatMilhar(q['descontos']),
                    'resultado':formatMilhar(resultado),
                    'v_dep':v_dep,
                    'd_dep':d_dep,
                    'r_dep':r_dep

                }
                )

        cursor.close()
        del cursor

    return render(request, 'app01/listSomaPorSecSetores.html',
            {
                'titulo': titulo,
                'resumo_depsetor':lista2,
                'municipios':municipios,
                'id_municipio':id_municipio,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia,
                'qtde_funcionario':qT,
                'total_v':formatMilhar(total_v),
                'total_d':formatMilhar(total_d),
                'total_r':formatMilhar(total_r),

            }
          )



def listSomaEventos(request):

    opcao=''
    query1=None
    query2=None
    titulo='Listar Soma por Eventos'
    cursor = connection.cursor()
    id_municipio=86
    anomes=''
    municipio=''
    referencia=''
    rs=0
    lista_eventos=[]
    lista2=[]

    total_v=0
    total_d=0
    total_r=0
    qT=0

    municipios = Municipio.objects.all().order_by('municipio')
    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano


        cursor.execute("SELECT f001_quantidadeServidoresMes (%s,%s)",[anomes,id_municipio])
        qt = dictfetchall(cursor)
        for e in qt[0].values():
            qT=e

        cursor.execute("Select evento,tipo,sum(valor) as valor from v005_folhaEventos where \
            anomes=%s and id_municipio=%s group by evento,tipo order by tipo desc,evento",[anomes,id_municipio])

        query0 = dictfetchall(cursor)

        for q in query0:
            if q['tipo']=='V':
                total_v+=q['valor']
                total_r+=q['valor']
            else:
                total_d+=q['valor']
                total_r-=q['valor']

            lista_eventos.append(
                {
                    'evento':q['evento'],
                    'tipo':'('+q['tipo']+')',
                    'valor':formatMilhar(q['valor'])
                }
                )
        total_v=formatMilhar(total_v)
        total_d=formatMilhar(total_d)
        total_r=formatMilhar(total_r)

#'''''''''''''''''''''''''''''''''''''''
        
        cursor.close()
        del cursor


    return render(request, 'app01/listSomaPorEventos.html',
            {
                'titulo': titulo,
                'eventos':lista_eventos,
                'municipios':municipios,
                'id_municipio':id_municipio,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia,
                'qtde_funcionario':qT,
                'total_v':total_v,
                'total_d':total_d,
                'total_r':total_r,
                'qT':qT

            }
          )



def imprimirCSVFolha(request):

    if request.method=='POST':
        id_municipio = request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)
        cursor = connection.cursor()
        lista=[]


        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
        else:
            municipio=''
            empresa = ''
        

        obj = Folhames.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
        if obj is None:
            municipio = funcoes_gerais.strings_pesquisa(id_municipio)
            return render(request, 'app01/planilhaErrada.html',
                    {
                        'titulo': 'Impressao do Excel',
                        'municipio':municipio,
                        'anomes': str(mes)+'/'+str(ano),
                        'mensagem':'Não existe nenhum registro para essa Folha.'

                    }
                )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="folha_20210215.csv"'
        if (1==1):

            ls_eventos = set([ev.id_evento_cv for ev in  Evento.objects.filter(empresa='SS',tipo='V',cancelado='N')])

            eventos = [ev.evento for ev in Eventos_cv.objects.filter(id_evento_cv__in=ls_eventos,tipo='V').order_by('evento')]


            cursor.execute("SELECT sv.cod_servidor,sv.nome,sv.data_admissao,sec.secretaria,'setor' as setor,fn.funcao,vc.vinculo,\
            fl.carga_horaria,fl.dias,rf.ref_eventos \
            from servidores sv inner join folhames fl on fl.cod_servidor=sv.cod_servidor\
            inner join secretarias sec on sec.id_secretaria=fl.id_secretaria \
            inner join funcoes_cv fn on fn.id_funcao_cv=fl.id_funcao\
            inner join vinculos vc on vc.id_vinculo=fl.id_vinculo\
            left join refeventos rf on rf.id_municipio=fl.id_municipio and rf.cod_servidor=fl.cod_servidor and rf.anomes=fl.anomes \
            where sv.id_municipio=fl.id_municipio and fl.anomes=%s and fl.id_municipio=%s\
            order by fl.cod_servidor",[anomes,id_municipio])

            query1 = dictfetchall(cursor)

            cabecalho = funcoes_gerais.cabecalhoFolha(empresa)
            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            contador=0

            for kk in range(0,len(query1)):
                somaEventos=0
                cod_servidor = query1[kk]['cod_servidor']
                queryEventos=funcoes_gerais.eventosMes(id_municipio,anomes,cod_servidor)

                lista_ev1=[]
                lista_ev2=[]

                for qq in range(len(queryEventos)):
                    lista_ev1.append(queryEventos[qq]['evento'])
                    lista_ev2.append(queryEventos[qq]['valor'])
                dict_eventos=dict(zip(lista_ev1,lista_ev2))


                lista.append(query1[kk]['secretaria'])
                lista.append(query1[kk]['setor'])
                lista.append(query1[kk]['cod_servidor'])
                lista.append(query1[kk]['nome'])
                lista.append(query1[kk]['funcao'])
                lista.append(query1[kk]['vinculo'])
                lista.append(query1[kk]['data_admissao'])
                lista.append(query1[kk]['carga_horaria'])
                lista.append(query1[kk]['ref_eventos'])


                for qq in range(len(eventos)):
                    if eventos[qq] in lista_ev1:
                        valor=dict_eventos[eventos[qq]]
                    else:
                        valor=0
                    lista.append(valor)

                '''
                for ll in range(len(queryEventos)):
                    valor_evento = queryEventos[ll]['valor']
                    valor_str = str(valor_evento)
                    valor_str = valor_str.replace('.',',')
                    lista.append(valor_str)
                    somaEventos+=queryEventos[ll]['valor']
                '''

                #lista.append(somaEventos)


                writer.writerow(lista)
                lista=[]
            
        return response
        #titulo = 'Impressao do Excel *****'
        #municipios=Municipio.objects.all().order_by('municipio')


    else:
        titulo = 'Impressao do Excel'
        municipios=Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/gravarCSVFolha.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':''

        }
    )


def parateste(request):

    lista_grupo_eventos=listagens.listagemGrupoEventos(86)
    dict_grupo_eventos=listagens.criarDictGrupoEventos(86)


    queryP = Planilha.objects.values(
        'codigo',
        'cpf',
        'secretaria',
        'setor',
        'funcao',
        'tipo_admissao',
        'previdencia',
        'carga_horaria',
        'ref_evento',
        'classificacao',
        'evento',
        'cod_evento',
        'tipo',
        'valor_evento'
        ).all()

    for qp in range(len(queryP)):

        cod_servidor = queryP[qp]['codigo']
        evento1 = queryP[qp]['evento']

        evento1=evento1.strip()


        if evento1 in lista_grupo_eventos:
            evento = dict_grupo_eventos[evento1]
        else:
            evento = evento1            


        print (str(cod_servidor) + ' - ' + evento1 + ' - '+ evento)


        
    return render(request, 'app01/planilhaErrada.html')



def agrupareventos(request):
    sessao(request)
    titulo_html = 'Agrupar Eventos'
    current_user_id = request.user.id
    current_user_name = request.user.username


    mensagem=''
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser


        fileExcel=request.FILES['filename']
        empresa=int(request.POST['empresa'])


        retorno = cadastro_01.grupo_eventos(fileExcel,empresa,current_user_id)

        if retorno==1:
            return HttpResponseRedirect(reverse('app01:agrupar-eventos'))



    municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/agruparEventos.html',
            {
                'titulo': titulo_html,
                'usuario_id': current_user_id,
                'usuario_username': current_user_name,
                'municipios': municipios,
            }
          )

def agruparfuncoes(request):
    sessao(request)
    titulo_html = 'Agrupar Funções'
    current_user_id = request.user.id
    current_user_name = request.user.username


    mensagem=''
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser


        fileExcel=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])

        retorno = cadastro_01.grupo_funcoes(fileExcel,id_municipio,current_user_id)

        if retorno==1:
            return HttpResponseRedirect(reverse('app01:agrupar-funcoes'))



    municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/agruparFuncoes.html',
            {
                'titulo': titulo_html,
                'usuario_id': current_user_id,
                'usuario_username': current_user_name,
                'municipios': municipios,
            }
          )


def eliminarAcentos(tabela):


    if tabela=='eventos':

        obj_evs=Evento.objects.all()
        for ev in obj_evs:
            ev.evento=funcoes_gerais.to_ascii_string(ev.evento)

        Evento.objects.bulk_update(obj_evs,['evento'])

    elif tabela=='secretaria':

        obj_evs=Secretaria.objects.all()
        for ev in obj_evs:
            ev.secretaria=funcoes_gerais.to_ascii_string(ev.secretaria)

        Secretaria.objects.bulk_update(obj_evs,['secretaria'])

    elif tabela=='setor':

        obj_evs=Setor.objects.all()
        for ev in obj_evs:
            ev.setor=funcoes_gerais.to_ascii_string(ev.setor)

        Setor.objects.bulk_update(obj_evs,['setor'])

    elif tabela=='funcoes':

        obj_evs=Funcao.objects.all()
        for ev in obj_evs:
            ev.funcao=funcoes_gerais.to_ascii_string(ev.funcao)

        Funcao.objects.bulk_update(obj_evs,['funcao'])
    else:
        string=funcoes_gerais.to_ascii_string(tabela)
        print (tabela)
        print (string)
        print (tabela.encode('UTF-8'))
        print ('--------------')



def remove_combining_fluent(string: str) -> str:
    normalized = unicodedata.normalize('NFD', string)
    return ''.join(
        [l for l in normalized if not unicodedata.combining(l)]
    )











