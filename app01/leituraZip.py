# -*- coding: utf-8 -*-
import os
import sys
import datetime
import zipfile
import re
from .models import Departamento,Setor,Cargo,Vinculo,ProvDesc,Funcionario
import csv
from . import funcoes_gerais,funcoes_banco
from django.http import HttpResponse
import PyPDF2 as p2
import json



#gravarDepartamento_modelo1
#gravarSetor_modelo1
#gravarCargo_modelo1
lista_funcoes=['0160GARI','0029AUXILIAR DE SERVICOS GERA','0035AGENTE ADMINISTRATIVO','0185SECRETARIA EXECUTIVA','0002CHEFE DE GABINETE','0032MOTORISTA']
lista_vinculos=['0030ESTATUTÁRIO (SERVIDOR REG','0035 SERVIDOR PÚBLICO NÃO EFET']
lista_lotacoes=['0003GABINETE DO PREFEITO','0001GERAL','0006EEIF FRANCISCO DE PINHO P','0007CARMOZINA BITTENCOURT DE','0006EEIF FRANCISCO DE PINHO P']
lista_proventos=['0001VENCIMENTO BASE','0053FMSS','0005FÉRIAS','0110AJUDA DESLOCAMENTO','0052IRRF','0166DESC. PARC. EMPREST.CONS.BRADESCO','0061AMPLIAÇÃO DE CARGA HORARIA','0102COMPLEM. SALARIAL','0105GRATIFICACAO','0171FERIAS VENDIDAS','0111DIFERENCA SALARIAL']



def valida_zip(file_zip,string_pesquisa,referencia):

    pesquisa_municipio=re.compile(string_pesquisa)
    pesquisa_anomes=re.compile(referencia)
    pesquisa1=0
    pesquisa2=0
    print (string_pesquisa+' - '+referencia)

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        contador=0
        for filename in zip.namelist():
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')
                res1 = pesquisa_municipio.search(line)
                res2 = pesquisa_anomes.search(line)
                if res1 is not None:
                    pesquisa1=1
                if res2 is not None:
                    pesquisa2=1
                contador+=1
                if contador>7:
                    if pesquisa1==0 or pesquisa2==0:
                        zip.close()
                        return 0
                    else:
                        zip.close()
                        return 1


def validaPDF(file_zip,string_pesquisa,referencia):

    pesquisa_municipio=re.compile('PREFEITURA MUNICIPAL DE CARIDADE')
    pesquisa_anomes=re.compile('NOV de 2021')
    pesquisa1=0
    pesquisa2=0

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        contador=0
        for filename in zip.namelist():
            file = zip.open(filename)

            pdf_reader = p2.PdfFileReader(file)

            n = pdf_reader.numPages
            for i in range(0,2):
                page = pdf_reader.getPage(i)
                page_content = (page.extractText())
                setor=''
                if re.search(string_pesquisa, page_content):
                    pesquisa1=1
                if re.search(referencia, page_content):
                    pesquisa2=1
        if (pesquisa1==1 and pesquisa2==1):
            return 1
        else:
            return 0



def importacaoGeral(file_zip,string_pesquisa,referencia,id_municipio):

    pesquisa_municipio=re.compile('PREFEITURA MUNICIPAL DE CARIDADE')
    pesquisa_anomes=re.compile('NOV de 2021')
    pesquisa1=0
    pesquisa2=0

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        contador=0
        for filename in zip.namelist():
            file = zip.open(filename)

            pdf_reader = p2.PdfFileReader(file)

            n = pdf_reader.numPages
            print ('numero de paginas '+str(n))
            '''
            for i in range(0,5):
                page = pdf_reader.getPage(i)
                page_content = (page.extractText())
                setor=''
                res = re.search(r'[0-9]{3,5}[A-Z]{5,12}\s[A-Z]{5,12}\s[A-Z]{5,12}', page_content)
                if res:
                    setor = res.group(0)
                    print ('Setor: '+setor)
            '''
            text=''
            string='--------------------------------------------------------------'
            string+='----------------------------------------------------------------------'

            lista_1=[]
            lista_2=[]
            ll_dep=[]
            ll_set=[]
            objs=Departamento.objects.filter(id_municipio=id_municipio)
            for obj in objs:
                ll_dep.append(obj.codigo)
            objs=Setor.objects.filter(id_municipio=id_municipio)
            for obj in objs:
                ll_set.append(obj.codigo)

            lista_final=[]
            for i in range(0,10):
                # creating a page object
                print ('volta EXTERNA' + str(i))
                pageObj = pdf_reader.getPage(i)
                # extracting text from page
                text=pageObj.extractText()
                text=re.sub(string,'??',text)
                linha = text.split('??')
                inicio_de_pagina=0
                for ll in range(0,len(linha)):
                    if inicio_de_pagina==0:
                        print ('inicio_de_pagina. '+str(inicio_de_pagina))
                    if re.search(r'RESUMO DO SETOR',linha[ll]):
                        continue
                    inicio_de_pagina+=1


                    if not re.search(r'[\d]{4}[A-Z\s]{3,10}',(linha[ll])[0:11]):
                        if not re.search(r'SETOR:',linha[ll]):
                            if not re.search(r'SEC.:',linha[ll]):
                                continue

                    if re.search(r'TOTAL DE SERVIDORES',linha[ll]):
                        continue




                    #print ('volta INTERNA '+str(i)+' - '+str(ll)+' - ' +str(len(linha)))
                    print(linha[ll])
                    print ('---------------')
                    depsetor=''

                    if ll==0:
                        if re.search(r'SETOR:',linha[ll]):
                            if re.search(r'SEC.:',linha[ll]):
                                depsetor=cod_departamentoSetor(linha[ll],ll_dep,ll_set,id_municipio)
                                continue


                                #teste_departamentoSetor(linha[ll])
                                #print('=====================================')
                                #print (depsetor['cod_depto']+';'+depsetor['depto'])
                                #print (depsetor['cod_setor']+';'+depsetor['setor'])
                                #print('=====================================')
                                #if depsetor is not None:
                                    #lista_1.append(depsetor['cod_depto']+depsetor['depto'])
                                    #lista_2.append(depsetor['cod_depto']+depsetor['cod_setor']+depsetor['setor'])
                                #print('\n')
                    else:                        
                        if ll>0:
                            lista_funcionario=cod_funcionario((linha[ll])[0:80])
                            print('///////////////////')

                            print (lista_funcionario)
                            print ('///////////////////////////')
                            #funcao=cod_funcao(linha[ll])
                            #print ('funcao: ' +funcao)
                            vinculo=cod_vinculo((linha[ll])[0:100] )
                            #print ('vinculo: ' +vinculo)
                            matricula=cod_matricula((linha[ll])[0:155])
                            #print ('matricula: ' +matricula)
                            #print('===========================')
                            #list_prov=rel_proventos(linha[ll])
                            #print (list_prov)
                            if 1==1:
                                lista_final.append({
                                    #'funcionario':lista_funcionario[0]['nome'],
                                    #'cod_funcionario':funcionario['cod_funcionario'],
                                    #'cod_funcao':funcionario['cod_funcao'],
                                    #'dep':depsetor['cod_depto']+depsetor['depto'],
                                    #'setor':depsetor['cod_setor']+depsetor['setor'],
                                    'matricula':matricula,
                                    'vinculo':vinculo
                                    #'proventos':list_prov

                                    })

    #set1=set(lista_1)
    #set2=set(lista_2)
    #gravar_departamento(set1,'departamento',id_municipio)
    #gravar_departamento(set2,'setor',id_municipio)
            #for k in range(0,len(lista_final)):
                #print (lista_final[k])
                #print ('----------------------------------------')
    print(lista_final)                



def cod_departamentoSetor(l_departamento,ll_dep,ll_set,id_municipio):
    position = l_departamento.find('PAG.:')

    dep_ok=0
    set_ok=0

    dep_desc=''
    dep_cod='000'
    set_cod='000000'
    set_desc=''


    if position>0:
        substr = l_departamento[-(len(l_departamento)-position):]        
        depset = substr.split(':')
        if len(depset)==4:
            desc_dep=depset[2][3:]
            if (desc_dep[-5:])=='SETOR':
                comp=len(desc_dep)
                dep_desc_=desc_dep[0:comp-5]
                dep_cod=depset[2][0:3]
                set_cod=depset[3][0:6]
                set_desc=depset[3][6:]
                for k in range(0,len(ll_dep)):
                    if ll_dep[k]==dep_cod:
                        dep_ok=1
                        break
                for k in range(0,len(ll_set)):
                    if ll_set[k]==set_cod:
                        set_ok=1
                        break
    if dep_ok==0:
        funcoes_banco.gravarLog('001','departamento nao cadastrado',id_municipio)
        #pass
    if set_ok==0:
        funcoes_banco.gravarLog('002','setor nao cadastrado',id_municipio)
        #pass
    return {'cod_depto':dep_cod,'depto':dep_desc,'cod_setor':set_cod,'setor':set_desc}



def cod_funcao(l_detalhe,tipo):
    for kk in range(0,len(lista_funcoes)):
        if re.search(lista_funcoes[kk],l_detalhe):
            if tipo=='funcionario':
                return l_detalhe[0:40]
            else:
                return lista_funcoes[kk]
    return ''


def cod_funcionario(l_detalhe):
    lista=[]
    for kk in range(0,len(lista_funcoes)):
        string_funcao=(lista_funcoes[kk])[0:27]
        if re.search(string_funcao,l_detalhe):
            string=re.sub(string_funcao,'$$',l_detalhe)
            string_v=string.split('$$')
            fun_cod=(string_v[0])[0:5]
            fun_nome=(string_v[0])[5:]
            cod_funcao=(string_funcao)[0:4]
            lista.append({'cod_funcionario':fun_cod,'nome':fun_nome,'cod_funcao':cod_funcao})
            return lista

    return lista



def cod_vinculo(l_detalhe):
    for kk in range(0,len(lista_vinculos)):
        string_vinculo=(lista_vinculos[kk])[0:25]
        if l_detalhe.find(string_vinculo):
            return (lista_vinculos[kk])[0:4]
    return '0000'            




def cod_matricula(l_detalhe):
    for kk in range(0,len(lista_lotacoes)):
        string_lotacao=(lista_lotacoes[kk])[0:24]
        if re.search(string_lotacao,l_detalhe):
            string = re.sub(string_lotacao,'$$',l_detalhe)
            string_v=string.split('$$')

            result = re.search(r'[$]{1}[\d]{3,8}[-]{1}[\d]{1}',string_v[1])

            if result is not None:
                return (result.group(0))[1:]
            else:
                return '000000'

def rel_proventos(l_detalhe):
    lista_prov=[]
    string = l_detalhe
    for kk in range(0,len(lista_proventos)):
        if re.search(lista_proventos[kk],string):
            string = re.sub(lista_proventos[kk],'$'+lista_proventos[kk],string)
    string = re.sub('VANTAGENS','$',string)
    lista=string.split('$')
    for k in range(1,len(lista)-1):
        cod_prov=lista[k][0:4]
        itens = (lista[k]).split()
        valor = itens[len(itens)-1]
        lista_prov.append({'cod':cod_prov,'valor':valor})
    return lista_prov


def importacaoFuncionario_modelo1(file_zip,id_municipio,anomes):
    # gravar os funcionarios
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        depto=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargo=[]
        lista_vinculo=[]
        lista_provdesc=[]


        lin_cargo=0
        lin_vinculo=0
        data=''
        #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            id_dep=funcoes_gerais.searchDepartamento(id_municipio,depto,'codigo')
                            id_set=funcoes_gerais.searchSetor(id_municipio,setor,'codigo')
                            id_cargo=funcoes_gerais.searchCargo(id_municipio,cargo,'consultar')
                            id_vinculo=funcoes_gerais.searchVinculo(id_municipio,vinculo,'consultar')
                    else:
                        if line_no==lin_vinculo+1:
                            data=line[7:17]
                            if len(data)==10:
                                ano=data[6:10]
                                dia=data[0:2]
                                mes=data[3:5]
                                data=ano+'-'+mes+'-'+dia
                            else:
                                data=''

                            ch=(line[36:39]).lstrip()
                            if ch=='':
                                ch='0'

                            funcoes_gerais.gravarFuncionario(id_municipio,codigo,nome,id_dep,id_set,id_cargo,id_vinculo,data,ch)
                            data=''


            res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
            if res:
                depto=line[0:11]
            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=line[0:3]
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        depto==''
                        setor==''

    zip.close()


def montaProventos(file_zip,codigo,depto,setor,cargo,vinculo,line_num):
    line_num=line_num-2
    ok=0
    lista=[]
    lista_completa=[]

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        for filename in zip.namelist():
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')
                if line_no==line_num:
                    if codigo!=line[0:6]:
                        break
                    else:
                        ok=1
                if line_no>=line_num+2 and ok==1:
                    if re.search(r'[A-Z]+',line) and ok==1:
                        linha = (line.rstrip('\n')).rstrip('\r')
                        if (re.search(r'[0-9]{3}\s[A-Z]',linha)  or re.search(r'1/3 FERIAS',linha)) and ok==1:
                            prov_cod=(linha[40:43]).rstrip()
                            prov_desc=(linha[44:70]).rstrip()
                            prov_valor=(linha[70:79]).lstrip()
                            desc_cod=(linha[80:83]).rstrip()
                            desc_desc=(linha[84:110]).rstrip()
                            desc_valor=(linha[111:120]).lstrip()

                            if len(prov_cod)>0 and len(prov_valor)>0:
                                dados_prov={'tipo':'V','codigo':prov_cod,'provento':prov_desc,'valor':prov_valor}
                                lista.append(dados_prov)
                            if len(desc_cod)>0 and len(desc_valor)>0:
                                dados_desc={'tipo':'D','codigo':desc_cod,'provento':desc_desc,'valor':desc_valor}
                                lista.append(dados_desc)


                        else:
                            break

            lista_completa=[{'codigo':codigo,'depto':depto,'setor':setor,'cargo':cargo,'vinculo':vinculo,'proventos':lista}] 

    return lista_completa


def gravarFolha_modelo1(file_zip,id_municipio,anomes):
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        departamento=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargo=[]
        lista_vinculo=[]
        lista_provdesc=[]
        lin_cargo=0
        lin_vinculo=0
         

        #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            #if line_no>700:
            #    break
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            lin_vinculo=0
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            id_dep=funcoes_gerais.searchDepartamento(id_municipio,departamento,'nome')
                            id_set=funcoes_gerais.searchSetor(id_municipio,setor,'nome')

                            lista_proventos.append(montaProventos(file_zip,codigo,id_dep,id_set,cargo,vinculo,line_no))

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                codigo=line[0:10]
                departamento=line[-(len(line)-12):]
                departamento=departamento[0:38]
                departamento=departamento.rstrip()

            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=(line[4:44]).rstrip()
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        departamento==''
                        setor==''

    zip.close()

    for ls in lista_proventos:
        for rel in ls:
            codigo = rel['codigo']
            depto = rel['depto']
            setor = rel['setor']
            cargo = rel['cargo']
            vinculo = rel['vinculo']
            id_cargo = funcoes_gerais.searchCargo(id_municipio,cargo,'consultar')
            if id_cargo==0:
                lista_cargo.append(cargo)
            id_vinculo = funcoes_gerais.searchVinculo(id_municipio,vinculo,'consultar')
            if id_vinculo==0:
                lista_vinculo.append(vinculo)

            provents = rel['proventos']
            
            for prov in provents:
                    #print(codigo+';'+prov['tipo']+';'+prov['codigo']+';'+prov['provento']+';'+prov['valor'])
                    #writer.writerow({"Func":codigo, "Departamento":depto, "Setor":setor, "Id_cargo":id_cargo,"Cargo":cargo, "Id_vinculo": id_vinculo,"Vinculo":vinculo ,"Tipo": prov['tipo'], "Cod": prov['codigo'],'Provento':prov['provento'],'Valor':prov['valor']})
                    id_provdesc=funcoes_gerais.searchProvDesc(id_municipio,prov['tipo'],prov['codigo'],'',True)
                    #print (str(id_municipio)+';'+str(202111)+';'+codigo+';'+str(depto)+';'+\
                        #str(setor)+';'+str(id_cargo)+';'+str(id_vinculo)+str(id_provdesc)+';'+prov['tipo']+';'+str(prov['valor']))
                    valor = prov['valor']
                    valor = valor.replace('.','')
                    valor = valor.replace(',','.')
                    valor = float(valor)
                    if len(codigo)==6:
                        obj=Funcionario.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
                        if obj is not None:
                            id_funcionario=obj.id_funcionario
                            Folha.objects.create(id_municipio=id_municipio,anomes=202111,id_funcionario=id_funcionario,\
                                id_departamento=depto,id_setor=setor,id_cargo=id_cargo,id_vinculo=id_vinculo,\
                                id_provento=id_provdesc,tipo=prov['tipo'],valor=valor)                    
'''
def gravarDepartamento_modelo1(file_zip,id_municipio):

    zip = zipfile.ZipFile(file_zip)

    kk=0
    lista_depto=[]

    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                lista_depto.append(line[0:50])
                depto=line[0:3]

            kk+=1
            #if kk>10500:
                #break
        set_depto=set(lista_depto)
        for dep in set_depto:
            codigo=dep[0:10]
            departamento=dep[-(len(dep)-12):]
            departamento=departamento.rstrip()
            search_dep=Departamento.objects.filter(id_municipio=id_municipio,departamento=departamento).first()
            if search_dep==None:
                Departamento.objects.create(id_municipio=id_municipio,codigo=codigo,departamento=departamento)
    zip.close()
'''

'''

def gravarSetor_modelo1(file_zip,id_municipio):

    depto=""
    setor=""
    funcionario=""
    lista_depto=[]
    lista_setor=[]
    lista_funcionario=[]        


    zip = zipfile.ZipFile(file_zip)

    kk=0
    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        funcionario=''
        departamento=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                if len(departamento)==0:
                    #lista_depto.append(line[0:50])
                    departamento=(line[12:50]).rstrip()
            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    if len(departamento)>0:
                        cp=len(line)-4
                        lista_setor.append(line[0:3]+';'+departamento+';'+line[4:44])
                        departamento=''

            kk+=1
            #if kk>10500:
                #break
        set_setor=set(lista_setor)
        for st in set_setor:
            dados = st.split(';')
            cod_setor=dados[0]
            departamento=dados[1]
            setor=dados[2]
            setor=(setor).rstrip()

            obj_dep=Departamento.objects.filter(id_municipio=id_municipio,departamento=departamento).first()
            if obj_dep is None:
                id_depto=0
            else:
                id_depto=obj_dep.id_departamento


            search_dep=Setor.objects.filter(id_departamento=id_depto,id_municipio=id_municipio,setor=setor).first()
            if search_dep is None:
                Setor.objects.create(id_departamento=id_depto,id_municipio=id_municipio,setor=setor,codigo=cod_setor)
    zip.close()

'''
'''
def gravarCargo_modelo1(file_zip,id_municipio):
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        depto=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargos=[]
        lista_vinculo=[]
        lista_provdesc=[]
        lista1=[]
        lista2=[]


        lin_cargo=0
        lin_vinculo=0
         

        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            lin_vinculo=0
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            #id_dep=funcoes_gerais.searchDepartamento(id_municipio,depto)
                            #id_set=funcoes_gerais.searchSetor(id_municipio,setor)

                            #lista_proventos.append(montaProventos(file_zip,codigo,depto,setor,cargo,vinculo,line_no))
                            lista_cargos.append({'cargo':cargo,'vinculo':vinculo})


            res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
            if res:
                depto=line[0:3]
            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=line[0:3]
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        depto==''
                        setor==''

    zip.close()
    for ls in lista_cargos:
        cargo=ls['cargo']
        vinculo=ls['vinculo']
    
        cargo = cargo.rstrip()
        vinculo = vinculo.rstrip()

        id_cargo = funcoes_gerais.searchCargo(id_municipio,cargo)
        if id_cargo==0:
            lista1.append(cargo)
        id_vinculo = funcoes_gerais.searchVinculo(id_municipio,vinculo)
        if id_vinculo==0:
            lista2.append(vinculo)
    set_cargo=set(lista1)
    set_vinculo=set(lista2)
    for st in set_cargo:
        print ("cargo: "+st)
    for st in set_vinculo:
        print ("vinculo: "+st)





def pesquisa(linha):
    lista=[]
    objs=ProvDesc.objects.all()
    for obj in objs:
        lista.append(obj.descricao)
    for l in lista:
        if re.search(r'[0-9]{3}\s[A-Z]',linha) and ok==1:
'''




'''
def folhacsv_modelo1(request, id_municipio,anomes):


    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="processo.csv"'

    cursor = connection.cursor()

    cursor.execute("SELECT v.id_departamento,d.departamento,p.codigo,p.descricao,SUM(vantagem) as vantagem, SUM(desconto) AS desconto FROM v003_proventos v,provdesc p,departamento d WHERE v.id_departamento=d.id_departamento AND  v.id_provento=p.id_provdesc AND v.id_municipio=%s AND v.anomes=%s  GROUP BY v.id_departamento,d.departamento,p.codigo,p.descricao ORDER BY d.departamento", [id_municipio,anomes])                        

    row = cursor.fetchone() 

    print ("id_municipio "+str(id_municipio)+ '  anomes '+anomes)
    writer = csv.writer(response, delimiter=';')
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow((
    'departamento',
    'descricao'
    ))

    contador=0
    while row and contador<25:
        contador=contador+1

        writer.writerow((
        row[1],
        row[3]
        ))
        row = cursor.fetchone() 
    cursor.close()
    del cursor
    connection.close()
                
    return response
'''




'''

def gravarPovDesc_modelo1(file_zip,id_municipio,anomes):
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        departamento=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargo=[]
        lista_vinculo=[]
        lista_provdesc=[]
        lin_cargo=0
        lin_vinculo=0
         

        #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            #if line_no>700:
            #    break
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            lin_vinculo=0
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            id_dep=0 #funcoes_gerais.searchDepartamento(id_municipio,departamento,'nome')
                            id_set=0 #funcoes_gerais.searchSetor(id_municipio,setor,'nome')
                            #if id_dep==0:
                                #print ('depto: '+departamento)
                            #if id_set==0:
                                #print ('setor: '+setor)


                            lista_proventos.append(montaProventos(file_zip,codigo,id_dep,id_set,cargo,vinculo,line_no))

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                codigo=line[0:10]
                departamento=line[-(len(line)-12):]
                departamento=departamento[0:38]
                departamento=departamento.rstrip()

            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=(line[4:44]).rstrip()
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        departamento==''
                        setor==''

    zip.close()

    for ls in lista_proventos:
        for rel in ls:
            codigo = rel['codigo']
            depto = rel['depto']
            setor = rel['setor']
            cargo = rel['cargo']
            vinculo = rel['vinculo']

            provents = rel['proventos']
            
            for prov in provents:
                #print(prov)
                funcoes_gerais.searchProvDesc(id_municipio,prov['tipo'],prov['codigo'],prov['provento'],True)
                    #print(codigo+';'+prov['tipo']+';'+prov['codigo']+';'+prov['provento']+';'+prov['valor'])
                    #writer.writerow({"Func":codigo, "Departamento":depto, "Setor":setor, "Id_cargo":id_cargo,"Cargo":cargo, "Id_vinculo": id_vinculo,"Vinculo":vinculo ,"Tipo": prov['tipo'], "Cod": prov['codigo'],'Provento':prov['provento'],'Valor':prov['valor']})
                    #id_provdesc=funcoes_gerais.searchProvDesc(id_municipio,prov['tipo'],prov['codigo'],'',True)



'''



def importacaoGeral_modelo1(file_zip,id_municipio,anomes):

    zip = zipfile.ZipFile(file_zip)

    kk=0
    lista_depto=[]
    lista_setor=[]
    lista_cargos=[]
    lin_cargo=0
    lin_vinculo=0
    l_cargo=[]
    l_vinculo=[]

    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                lista_depto.append(line[0:50])
                depto=line[0:11]

            else: 
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    if len(depto)>0:
                        lista_setor.append(line[0:3]+';'+depto+';'+line[4:44])
                        depto=''
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                    else:
                        if lin_cargo==line_no:
                            if re.search(r'\s{7}[A-Z]+',line):
                                cargo=(line[7:40]).rstrip()
                                lin_cargo=0
                                lin_vinculo=line_no+1
                                l_cargo.append(cargo)
                        else:
                            if lin_vinculo==line_no:
                                if re.search(r'\s{7}[A-Z]+',line):
                                    vinculo=(line[7:40]).rstrip()
                                    lin_vinculo=0
                                    codigo=funcionario[0:6]
                                    nome=funcionario[-53:]
                                    l_vinculo.append(vinculo)


            kk+=1
        set_depto=set(lista_depto)
        set_setor=set(lista_setor) 
        for dep in set_depto:
            codigo=dep[0:11]
            departamento=dep[-(len(dep)-12):]
            departamento=departamento.rstrip()

            obj_dep=Departamento.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
            if obj_dep is None:
                Departamento.objects.create(id_municipio=id_municipio,codigo=codigo,departamento=departamento)
        for setor in set_setor:
            itens=setor.split(';')
            cod_setor=itens[0]
            cod_depto=itens[1]
            setor=itens[2].rstrip()
            #print (cod_depto +' - '+cod_setor+' - '+setor)
            obj_setor=Setor.objects.filter(id_municipio=id_municipio,codigo=cod_setor).first()
            if obj_setor is None:
                obj_dep=Departamento.objects.filter(id_municipio=id_municipio,codigo=cod_depto).first()
                if obj_dep is not None:
                    id_dep=obj_dep.id_departamento
                    Setor.objects.create(id_municipio=id_municipio,id_departamento=id_dep,setor=setor,codigo=cod_setor)


        s_cargo=set(l_cargo)
        s_vinculo=set(l_vinculo)

        for ls in s_cargo:
            cargo=ls
            cargo = cargo.rstrip()
            id_cargo = funcoes_gerais.searchCargo(id_municipio,cargo,'incluir')
        for ls in s_vinculo:
            vinculo=ls
            vinculo = vinculo.rstrip()
            id_vinculo = funcoes_gerais.searchVinculo(id_municipio,vinculo,'incluir')

    zip.close()



def importacaoProventos_modelo1(file_zip,id_municipio,anomes):

    zip = zipfile.ZipFile(file_zip)

    kk=0
    lista_proventos=[]
    line_resumo=0

    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'RESUMO GERAL DA FOLHA', line):
                line_resumo=line_no
            else:
                if line_no>line_resumo and line_resumo>20:
                    if re.search(r'[\s]{30,40}\s[0-9]{3}\s', line):
                        linha=(line[32:70]).rstrip()
                        lista_proventos.append(linha)
            if len(lista_proventos)>10:
                if re.search(r'[-]{10,20}\s', line):
                    break

    zip.close()
    for lp in lista_proventos:
        prov_cod = lp[0:3]
        prov_desc = lp[-(len(lp)-3):]
        prov_desc=(prov_desc).rstrip()
        prov_desc=(prov_desc).lstrip()

        if int(prov_cod)<500:
            tipo='V'
        else:
            tipo='D'
        id = funcoes_gerais.searchProvDesc(id_municipio,tipo,prov_cod,prov_desc,True)




def importacaoGeral_modelo2(file_zip,id_municipio,anomes):

    zip = zipfile.ZipFile(file_zip)

    kk=0
    lista_depto=[]
    lista_setor=[]
    lista_cargos=[]
    lin_cargo=0
    lin_vinculo=0
    l_cargo=[]
    l_vinculo=[]

    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                lista_depto.append(line[0:50])
                depto=line[0:11]

            else: 
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    if len(depto)>0:
                        lista_setor.append(line[0:3]+';'+depto+';'+line[4:44])
                        depto=''
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                    else:
                        if lin_cargo==line_no:
                            if re.search(r'\s{7}[A-Z]+',line):
                                cargo=(line[7:40]).rstrip()
                                lin_cargo=0
                                lin_vinculo=line_no+1
                                l_cargo.append(cargo)
                        else:
                            if lin_vinculo==line_no:
                                if re.search(r'\s{7}[A-Z]+',line):
                                    vinculo=(line[7:40]).rstrip()
                                    lin_vinculo=0
                                    codigo=funcionario[0:6]
                                    nome=funcionario[-53:]
                                    l_vinculo.append(vinculo)


            kk+=1
        set_depto=set(lista_depto)
        set_setor=set(lista_setor) 
        for dep in set_depto:
            codigo=dep[0:11]
            departamento=dep[-(len(dep)-12):]
            departamento=departamento.rstrip()

            obj_dep=Departamento.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
            if obj_dep is None:
                Departamento.objects.create(id_municipio=id_municipio,codigo=codigo,departamento=departamento)
        for setor in set_setor:
            itens=setor.split(';')
            cod_setor=itens[0]
            cod_depto=itens[1]
            setor=itens[2].rstrip()
            #print (cod_depto +' - '+cod_setor+' - '+setor)
            obj_setor=Setor.objects.filter(id_municipio=id_municipio,codigo=cod_setor).first()
            if obj_setor is None:
                obj_dep=Departamento.objects.filter(id_municipio=id_municipio,codigo=cod_depto).first()
                if obj_dep is not None:
                    id_dep=obj_dep.id_departamento
                    Setor.objects.create(id_municipio=id_municipio,id_departamento=id_dep,setor=setor,codigo=cod_setor)


        s_cargo=set(l_cargo)
        s_vinculo=set(l_vinculo)

        for ls in s_cargo:
            cargo=ls
            cargo = cargo.rstrip()
            id_cargo = funcoes_gerais.searchCargo(id_municipio,cargo,'incluir')
        for ls in s_vinculo:
            vinculo=ls
            vinculo = vinculo.rstrip()
            id_vinculo = funcoes_gerais.searchVinculo(id_municipio,vinculo,'incluir')

    zip.close()


def importacaoProventos_modelo2(file_zip,id_municipio,anomes):

    zip = zipfile.ZipFile(file_zip)

    kk=0
    lista_proventos=[]
    line_resumo=0

    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'RESUMO GERAL DA FOLHA', line):
                line_resumo=line_no
            else:
                if line_no>line_resumo and line_resumo>20:
                    if re.search(r'[\s]{30,40}\s[0-9]{3}\s', line):
                        linha=(line[32:70]).rstrip()
                        lista_proventos.append(linha)
            if len(lista_proventos)>10:
                if re.search(r'[-]{10,20}\s', line):
                    break

    zip.close()
    for lp in lista_proventos:
        prov_cod = lp[0:3]
        prov_desc = lp[-(len(lp)-3):]
        prov_desc=(prov_desc).rstrip()
        prov_desc=(prov_desc).lstrip()

        if int(prov_cod)<500:
            tipo='V'
        else:
            tipo='D'
        id = funcoes_gerais.searchProvDesc(id_municipio,tipo,prov_cod,prov_desc,True)



def importacaoFuncionario_modelo2(file_zip,id_municipio,anomes):
    # gravar os funcionarios
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        depto=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargo=[]
        lista_vinculo=[]
        lista_provdesc=[]


        lin_cargo=0
        lin_vinculo=0
        data=''
        #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            id_dep=funcoes_gerais.searchDepartamento(id_municipio,depto,'codigo')
                            id_set=funcoes_gerais.searchSetor(id_municipio,setor,'codigo')
                            id_cargo=funcoes_gerais.searchCargo(id_municipio,cargo,'consultar')
                            id_vinculo=funcoes_gerais.searchVinculo(id_municipio,vinculo,'consultar')
                    else:
                        if line_no==lin_vinculo+1:
                            data=line[7:17]
                            if len(data)==10:
                                ano=data[6:10]
                                dia=data[0:2]
                                mes=data[3:5]
                                data=ano+'-'+mes+'-'+dia
                            else:
                                data=''

                            ch=(line[36:39]).lstrip()
                            if ch=='':
                                ch='0'

                            funcoes_gerais.gravarFuncionario(id_municipio,codigo,nome,id_dep,id_set,id_cargo,id_vinculo,data,ch)
                            data=''


            res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
            if res:
                depto=line[0:11]
            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=line[0:3]
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        depto==''
                        setor==''

    zip.close()





def gravar_departamento(lista_ds,tipo,id_municipio):
    if tipo=='departamento':
        for string in lista_ds:
            cod=string[0:3]
            desc=string[3:]
            objs = Departamento.objects.filter(id_municipio=id_municipio,codigo=cod).first()
            if objs is None:
                Departamento.objects.create(id_municipio=id_municipio,codigo=cod,departamento=desc)
    if tipo=='setor':
        for string in lista_ds:
            coddep=string[0:3]
            codset=string[3:9]
            desc=string[9:]

            objs = Departamento.objects.filter(id_municipio=id_municipio,codigo=coddep).first()
            if objs is not None:
                id_departamento=objs.id_departamento
                objs = Setor.objects.filter(id_municipio=id_municipio,codigo=codset,id_departamento=id_departamento).first()
                if objs is None:
                    Setor.objects.create(id_municipio=id_municipio,codigo=codset,setor=desc,id_departamento=id_departamento)













