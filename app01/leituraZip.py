# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import re
from .models import Departamento,Setor,Cargo,Vinculo,ProvDesc,Funcionario
from . import funcoes_gerais,funcoes_banco
import PyPDF2 as p2


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

